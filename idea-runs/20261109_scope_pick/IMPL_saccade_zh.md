# SaccadeKV 实现方案

> 配合 `METHOD_saccade_zh.md` 阅读。分两步走：
> - 先在 HF transformers 上做单请求原型，跑准确率实验 E0–E3；
> - 再在 vLLM 上做系统版，跑显存打满时的吞吐实验 E4–E5。

---

## 0. 先选模型

**原型阶段用 DeepEyes-7B**，它基于 Qwen2.5-VL-7B，原因有两个：
- 它本身就会发 zoom 工具调用，模型输出一个 bbox，不用我们教它"什么时候看、看哪里"；
- Qwen2.5-VL 结构比 Qwen3-VL 简单，没有 DeepStack。

Qwen3-VL-8B-Thinking 放在第二阶段，要多处理一步 DeepStack（见 §6）。

**Qwen2.5-VL 的几个关键事实**（写代码前对照 HF 源码确认一遍）：
- **视觉 token 尺寸**：ViT 的 patch 是 14 px，2×2 合并后 1 个视觉 token 对应 28×28 px。图像先被缩放到 28 的倍数。
- **图像怎么进 LLM**：输入里有一串 `<|image_pad|>` 占位符，ViT 输出的视觉 embedding 按顺序替换掉它们，然后整条序列一起进 LLM。
- **位置编码**：用 M-RoPE，每个 token 有 3 个位置分量 (t, h, w)。
  - 文本 token 三个分量相同，就是普通的 1D 位置；
  - 图像 token 的 h、w 是它在网格里的行号和列号，加上图像起始偏移；
  - 图像后面的文本，位置从"图像里最大的位置 + 1"接着往下数。
  - HF 里这些由 `get_rope_index()` 算出，形状是 `(3, batch, seq_len)`。
- **KV 缓存**：每层的 K/V 张量形状为 `[batch, kv_heads, seq_len, head_dim]`，K 存的是已经旋转过的（post-RoPE）。

---

## 1. 两个让实现变简单的观察

### 观察 1："原地"只是逻辑上的，物理上不用插到中间
注意力是对缓存里所有 key 求 softmax，**和它们在张量里的物理顺序无关**。真正决定计算结果的只有两样：
- 每个 key 的 RoPE 位置；
- 哪些 key 可见（mask）。

所以实现时：
- 新的高清 token 的 KV 物理上放在哪里都行，比如直接拼到张量末尾，只要它的 RoPE 位置是 R 那块的坐标；
- "遮蔽底图 token"等价于把它们从缓存张量里**物理删掉**；
- 退回时，再从备份里把它们拼回来。

这样 decode 时用标准的因果注意力就行，**不用写任何自定义 mask**。

### 观察 2：坐标系固定在原生网格上，文本位置永远不变
图像的所有 token，不管哪个层级，都用"原生分辨率网格"的坐标；图像后面文本的起始位置也按原生网格的尺寸算。

这样一来，扫视前后图像块的坐标范围不变，**问题和思维链的位置一个都不用改**，它们的 KV 可以原样保留。

---

## 2. 数据结构

```python
class VisualMemory:
    tiles: dict[(i, j)] -> level        # 每个 tile 当前的层级：0=底图, 1=原生, 2=2倍
    base_emb:  Tensor[n_base, d]        # 底图视觉 embedding（ViT 输出），常驻
    base_pos:  Tensor[3, n_base]        # 底图 token 的 (t,h,w) 坐标（原生网格单位）
    fovea: list[Fixation]               # 缓冲区里的注视，按时间排序（LRU）
    F: int                              # 缓冲区容量（token 数）

class Fixation:
    tiles: list[(i, j)]                 # 覆盖的 tile
    level: int
    emb:  Tensor[n_tok, d]              # 高清视觉 embedding
    pos:  Tensor[3, n_tok]              # 子网格坐标
    last_used: int                      # 最近一次被看的步数
```

缓存分段（物理顺序）：

```
[ 系统提示 | 图像块（混合分辨率） | 问题 | 思维链 ... ]
   sys_len     img_len（会变）       q_len    不断增长
```

---

## 3. 原型流程（HF，单请求）

### Step 1：编码底图
1. 原图按原生分辨率算出网格大小 H×W（单位：28 px 的 token）。
2. 把图缩小一半，过 ViT，得到 (H/2)×(W/2) 个底图 token 的 embedding。
3. 底图 token (i, j) 的坐标设为原生网格上的中心点：`h = i*2 + 0.5`，`w = j*2 + 0.5`，`t = 0`，再加上图像起始偏移。
4. 图像后面文本的起始位置 = 偏移 + max(H, W)，**按原生网格算，不是按底图算**。

### Step 2：首次 prefill
- 序列 = 系统提示 + 底图 embedding（替换占位符）+ 问题。
- 自己构造 `position_ids`，不调用 `get_rope_index()`，传入 float 张量。
- 前向一次得到缓存，记下三段的长度 `sys_len / img_len / q_len`。

### Step 3：正常解码，直到模型发出 zoom
- 正常 `generate` 或手写 decode 循环。
- 检测到工具调用结束标记时停下，解析出 bbox。DeepEyes 的工具调用格式以它的代码仓库为准。

### Step 4：一次扫视
```python
def saccade(bbox, cache, mem, step):
    # a. bbox 对齐到 tile 边界（1 个 tile = 1 个底图 token = 56×56 px）
    tiles = snap_to_tiles(bbox)

    # b. 从原图裁出这块区域，按原生分辨率过 ViT
    crop = original_image.crop(tiles_to_pixels(tiles))
    emb = vit(resize_to_multiple_of_28(crop))          # 每个 tile 得到 2×2 = 4 个 token
    pos = subgrid_coords(tiles, level=1)               # 原生网格的整数坐标
    fix = Fixation(tiles, level=1, emb=emb, pos=pos, last_used=step)

    # c. 放进缓冲区，超过容量就按 LRU 退回最早的注视
    mem.fovea.append(fix)
    while sum(f.n_tok for f in mem.fovea) > mem.F:
        mem.fovea.pop(0)                               # 被退回的 tile 重新用底图 token

    # d. 精确模式：按光栅顺序重建混合分辨率图像块，连同问题一起重新 prefill
    img_emb, img_pos = mem.assemble_raster()           # 每个 tile 用当前层级的 token
    new_kv = model.prefill(
        inputs_embeds = cat(img_emb, question_emb),
        position_ids  = cat(img_pos, question_pos),    # 问题的位置不变（观察 2）
        past = cache[:sys_len])                        # 只在系统提示的 KV 之上
    # e. 拼回：系统提示 + 新的图像块和问题 + 原来的思维链
    cache = cat(cache[:sys_len], new_kv, cache[sys_len+img_len+q_len:])
    return cache
```

- **快速模式**把 d、e 换成两步：
  - 以"系统提示 + 底图中 R 以外的 token"作为临时缓存，只对新 token 做前向，得到它们的 KV；
  - 从缓存里删掉 R 的底图 token，把新 KV 拼到末尾。
- **光栅顺序**：先按 tile 的行列顺序遍历；tile 内部再按它自己的行列顺序排。

### Step 5：继续推理
- DeepEyes 训练时，工具返回的是"一张新图"。SaccadeKV 不追加新图，所以要在上下文里追加一小段**文本观察**，例如"已放大区域 [x1,y1,x2,y2]"，告诉模型视觉记忆已经更新。
- 然后接着解码，回到 Step 3。

### Step 6：记录
每道题记录：
- 准确率、注视次数、每次 bbox、输出长度；
- 视觉 KV 峰值（token 数 × 144 KiB 换算成字节）；
- 是否卡住或重复。

---

## 4. 实验 E1 的实现（最先跑，不需要解码中扫视）

E1 只回答一个问题：**模型能不能读懂混合分辨率的图**。

- 用 V* 的标注框直接构造混合分辨率图像块：底图，加上标注框内的原生 token。
- 一次 prefill 就能出答案，复用 Step 1、2 和 `assemble_raster()`。
- 一共 5 组对比：
  1. 原生分辨率；
  2. 整图缩小；
  3. 底图 + 追加裁剪图（用模型原本的图像格式）；
  4. 混合分辨率（本方法的静态版）；
  5. 4 的坐标换成"直接放末尾"（消融连续坐标）。

**工作量**：Step 1、2 和 `assemble_raster()`，约 200 行，2–3 天能跑出第一批数字。

---

## 5. 如果模型读不懂混合分辨率：LoRA 适配器
- **数据**：从高清图数据集（如 V* 训练集、SA-1B 子集）随机采样图像，随机选 1–4 个框，构造混合分辨率输入。
- **目标**：同一模型在原生全分辨率输入下回答同一问题，以它的输出分布为老师，对学生做 KL 自蒸馏。
- **训练**：只在 LLM 的注意力层上加 LoRA（rank 16–64），ViT 冻结。约 5–10 万条样本，8×H200 上 1–2 天。

---

## 6. Qwen3-VL 的额外处理
- 视觉 token 是 32×32 px：ViT patch 16，2×2 合并。
- **DeepStack**：ViT 多个中间层的特征，会加到 LLM 前几层视觉 token 的 hidden state 上。扫视时，对裁剪图同样取出这些中间层特征，和新 token 一起传进去。HF 里对应 `deepstack_visual_embeds` 和视觉位置 mask 这两个输入。
- M-RoPE 是交错排布的 (t, h, w)，坐标的构造方法不变。

---

## 7. 系统版：vLLM（E4、E5）

需要改三处。

1. **视觉 token 的位置**
   - vLLM 的 RoPE 用预先算好的 cos/sin 表，**按整数位置查表**，所以不支持小数坐标。两个办法：
     - **只用 L0 + L1 两级**：底图 token 取原生网格的整数坐标（例如左上角 `2i, 2j`），全是整数，不用改 kernel。推荐先这样做。
     - 需要 L2 时：对视觉 token 在线计算 cos/sin，改动很小。
   - 首次 prefill 时，用我们自己的坐标覆盖 vLLM 算出的 mrope 位置。
2. **扫视时的局部 prefill**
   - 在调度器里加一种请求状态"扫视中"：暂停该请求的解码，提交一个只包含"图像块 + 问题"的局部 prefill，挂在系统提示的 KV 块之后，结果写进新分配的 KV 块。
3. **块表替换**
   - 局部 prefill 完成后，把该请求块表里"图像块 + 问题"那几块换成新块，旧块释放；思维链的块不动。
   - 因为图像块长度会变，让图像块单独占若干个块，块内末尾可以留空，问题段从新块开始。这样替换时不会和思维链共用块。

**显存**：每个请求的视觉 KV 上限 = 底图 + F，可以按这个上限做准入控制，batch 大小稳定。

**先做的简化版**：用 vLLM 跑追加式基线；SaccadeKV 的吞吐先按 HF 原型测出的注视次数和 token 数做解析估算。等方法定型，再实现上面三处改动做实测。

---

## 8. 工作量估计
| 模块 | 代码量 | 时间 |
|---|---|---|
| 坐标构造 + 混合分辨率组装 + E1 | ~200 行 | 1 周 |
| 解码中扫视（精确 / 快速两种模式）+ DeepEyes 工具解析 + E3 | ~400 行 | 1–2 周 |
| LoRA 自蒸馏（如需要） | ~300 行 | 1 周 |
| Qwen3-VL 适配（DeepStack） | ~100 行 | 2–3 天 |
| vLLM 系统版 | ~800 行 | 3–4 周 |
