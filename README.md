# dotfiles

我的 macOS 开发环境配置。写给三年后的自己。

## 新机器上怎么用

```bash
git clone https://github.com/<你的用户名>/dotfiles.git ~/dotfiles
~/dotfiles/install.sh
```

脚本会：建软链接（原有文件先备份到 `~/.dotfiles-backup/`）→ 装 Homebrew（如缺）→ 按 `Brewfile` 装齐工具。
可以重复执行，不会越跑越乱。

## 目录

| 路径 | 链接到 | 装什么 |
|---|---|---|
| `zsh/zprofile` | `~/.zprofile` | PATH、环境变量（登录时执行一次） |
| `zsh/zshrc` | `~/.zshrc` | 别名、补全、历史（每个 shell 都执行） |
| `git/gitconfig` | `~/.gitconfig` | git 全局配置 |
| `tmux/tmux.conf` | `~/.tmux.conf` | tmux 键位 |
| `vscode/settings.json` | `~/Library/Application Support/Code/User/settings.json` | 编辑器配置 |
| `Brewfile` | — | 工具 **与 VS Code 扩展** 清单，`brew bundle` 用 |

## 为什么用软链接而不是复制

只存在一份文件。改配置就是改仓库里的文件，直接产生 `git diff`，
不存在"改完忘了同步回仓库"这种问题。单一事实来源。

## 加了新工具怎么办

```bash
brew install <工具>
cd ~/dotfiles
brew bundle dump --force
git diff Brewfile      # 必看：确认只有新增，没有意外删除
git add -p && git commit
```

`git diff` 那步不能省。`brew bundle dump` 若在 `code` 不在 PATH 的 shell 里执行，
会静默删掉全部 `vscode "…"` 行，而你要到换机器还原时才会发现扩展全没了。

## 待办

- [ ] `git/gitconfig` 里的 `url.insteadOf` 把 SSH 改写成 HTTPS，是早期为绕过
      SSH 连不上 GitHub 加的。将来配好 SSH key 后要删掉，否则 SSH 配了也不生效。
- [ ] 还没配提示符（starship？）。等用顺手了再说，别一上来堆插件。
