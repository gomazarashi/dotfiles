# ~/.config/shell/path.sh
# ~/.profile と ~/.bashrc の両方から読み込む PATH 設定 (POSIX sh)。
# 何度読み込んでも重複せず、同じ順序になる (先頭に追加したあと、PATH 全体で最初の出現だけを残す)。
#
# 優先順位 (上ほど優先):
#   1. ユーザーのツール (~/.local/bin, ~/bin, bun, cargo, deno, juliaup, opencode)
#   2. Ubuntu のシステムディレクトリ
#   3. Nix (/etc/bash.bashrc の nix-daemon.sh が先頭に追加したものを後ろへ回す)
# Ubuntu toolchain を Nix より優先するのは、R パッケージのビルドで
# Ubuntu の R と Nix の make/glibc が混ざるのを避けるため。

export BUN_INSTALL="$HOME/.bun"

# 優先度の低い順に先頭へ追加する
for _dotfiles_d in \
    /snap/bin \
    /bin \
    /sbin \
    /usr/bin \
    /usr/sbin \
    /usr/local/bin \
    /usr/local/sbin \
    "$HOME/.opencode/bin" \
    "$HOME/.juliaup/bin" \
    "$HOME/.deno/bin" \
    "$HOME/.cargo/bin" \
    "$BUN_INSTALL/bin" \
    "$HOME/bin" \
    "$HOME/.local/bin"
do
    [ -d "$_dotfiles_d" ] && PATH="$_dotfiles_d${PATH:+:$PATH}"
done

# 重複を除去する (最初の出現を残す)。空要素 (カレントディレクトリ扱い) も除く
_dotfiles_rest="$PATH:"
PATH=
while [ -n "$_dotfiles_rest" ]; do
    _dotfiles_d=${_dotfiles_rest%%:*}
    _dotfiles_rest=${_dotfiles_rest#*:}
    [ -n "$_dotfiles_d" ] || continue
    case ":$PATH:" in
        *":$_dotfiles_d:"*) ;;
        *) PATH="${PATH:+$PATH:}$_dotfiles_d" ;;
    esac
done
export PATH

unset _dotfiles_d _dotfiles_rest
