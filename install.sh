#!/usr/bin/env bash
# 在一台新机器上还原开发环境。
# 用法：git clone <repo> ~/dotfiles && ~/dotfiles/install.sh
#
# 这个脚本是幂等的：重复执行结果相同，不会越跑越乱。

set -euo pipefail
# -e  任何命令失败立即退出（默认是继续往下跑，会造成"错了但还在干活"）
# -u  用到未定义变量就报错（拼错变量名不再静默变成空字符串）
# -o pipefail  管道里任何一环失败都算失败（默认只看最后一个命令）
# 这三行是 shell 脚本的安全带，所有正经脚本都该有。

DOTFILES="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKUP="$HOME/.dotfiles-backup/$(date +%Y%m%d-%H%M%S)"

link() {
  local src="$DOTFILES/$1"
  local dst="$HOME/$2"

  # 已经是指向正确位置的软链接 → 什么都不做（幂等的关键）
  if [ -L "$dst" ] && [ "$(readlink "$dst")" = "$src" ]; then
    echo "  已就位  $2"
    return
  fi

  # 存在但不是我们的链接 → 先备份，绝不静默覆盖别人的东西
  if [ -e "$dst" ] || [ -L "$dst" ]; then
    mkdir -p "$BACKUP"
    mv "$dst" "$BACKUP/"
    echo "  已备份  $2 → $BACKUP/"
  fi

  mkdir -p "$(dirname "$dst")"   # VS Code 那类深层路径，目标目录可能还不存在
  ln -s "$src" "$dst"
  echo "  已链接  $2"
}

echo "==> 建立软链接"
link zsh/zshrc      .zshrc
link zsh/zprofile   .zprofile
link git/gitconfig  .gitconfig
link tmux/tmux.conf .tmux.conf
link vscode/settings.json "Library/Application Support/Code/User/settings.json"

echo "==> 安装 Homebrew 与工具"
if ! command -v brew >/dev/null 2>&1; then
  echo "  未检测到 Homebrew，正在安装…"
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  eval "$(/opt/homebrew/bin/brew shellenv)"
fi
brew bundle --file="$DOTFILES/Brewfile"

echo "==> 安装 VS Code 扩展"
if command -v code >/dev/null 2>&1; then
  # grep -v '^#' 去掉注释行，grep -v '^$' 去掉空行
  grep -v '^#' "$DOTFILES/vscode/extensions.txt" | grep -v '^$' | while read -r ext; do
    code --install-extension "$ext" --force
  done
else
  echo "  未找到 code 命令，跳过。（VS Code 里 Cmd+Shift+P → Install 'code' command）"
fi

echo
echo "完成。开一个新终端窗口，或执行：source ~/.zprofile && source ~/.zshrc"
