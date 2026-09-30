# dotfiles

個人用。Ubuntu 24.04 / Windows を [chezmoi](https://www.chezmoi.io/) で管理する。

- **source state** (設定の元データ) はこのリポジトリの `home/` 以下 (`.chezmoiroot` で指定)
- **target** (実際に配置される `$HOME` 側のファイル) へは symlink/hardlink ではなく実ファイルをコピーする

## 設定を変更してマシンに適用する

流れは次のとおり。

1. source state (`home/` 以下) を編集する
2. `chezmoi diff` と `chezmoi apply --dry-run --verbose` で差分を確認する
3. `chezmoi apply` で `$HOME` に適用する
4. 他のマシンへ反映する場合は commit / push し、各マシンで `chezmoi update` する

> **重要**: `$HOME` 側のファイル (`~/.bashrc` など) を直接編集しない。次に `chezmoi apply` したときに上書きされる。変更は必ず source state に書く。

### 1. source state を編集する

**方法A: chezmoi のコマンドで開く**

```sh
chezmoi edit ~/.bashrc   # source 側 (home/dot_bashrc) がエディタで開く
chezmoi cd               # source ディレクトリでシェルを開く
```

**方法B: リポジトリのファイルを直接編集する**

`~/.dotfiles/home/` 以下のファイル名が配置先を表す。

| source の名前の例 | 配置先 (target) | 意味 |
|---|---|---|
| `dot_bashrc` | `~/.bashrc` | `dot_` は先頭の `.` |
| `dot_config/opencode/opencode.jsonc` | `~/.config/opencode/opencode.jsonc` | ディレクトリ構造がそのまま対応する |
| `AppData/Roaming/Zed/settings.json.tmpl` | `%APPDATA%\Zed\settings.json` | Windows のみ |
| `readonly_Documents/PowerShell/Microsoft.PowerShell_profile.ps1` | `$HOME\Documents\PowerShell\Microsoft.PowerShell_profile.ps1` | Windows のみ |
| `dot_codex/modify_private_config.toml` | `~/.codex/config.toml` | 特殊 (下の「Codex」を参照) |

- `.tmpl` が付いたファイルは**テンプレート**。`{{ ... }}` が展開されてから配置される
- 同じ内容を複数の配置先で使う場合は `.chezmoitemplates/` に 1 つだけ置き、各ファイルから `includeTemplate` で参照する (Ponytail / Zed がこの方式)
- **新しいファイルを管理対象に追加する**: `chezmoi add ~/.config/foo/bar.conf` を実行すると `home/dot_config/foo/bar.conf` が作られる。OS 専用のファイルなら `.chezmoiignore` に条件を追記して他の OS では配置しないようにする

### 2. 差分を確認する (必須)

```sh
chezmoi diff
chezmoi apply --dry-run --verbose
```

確認するポイント:

- Codex が自動生成した state (`[projects.*]` の trust など) が消えていないか
- 意図しないファイルの削除がないか
- OS 混在の配置 (Linux 用が Windows に、またはその逆) がないか
- secret / token / credential が差分に含まれていないか

### 3. 適用する

```sh
chezmoi apply            # すべて適用
chezmoi apply ~/.bashrc  # 1 ファイルだけ適用
```

### 4. 他のマシンへ反映する

```sh
# 変更したマシン
git -C ~/.dotfiles add -A
git -C ~/.dotfiles commit -m "..."
git -C ~/.dotfiles push

# 反映先のマシン
chezmoi update           # source repo の git pull + chezmoi apply
```

`git pull` を手動で行った場合は `chezmoi apply` を実行する。

### 状態の確認に使うコマンド

| コマンド | 意味 |
|---|---|
| `chezmoi doctor` | 環境と設定の診断 |
| `chezmoi managed` | 管理対象の target 一覧 |
| `chezmoi ignored` | この OS では配置しない target 一覧 |
| `chezmoi status` | 差分の 1 行サマリ |
| `chezmoi diff` | 差分の中身 |
| `chezmoi apply --dry-run --verbose` | 適用内容のプレビュー (変更しない) |

## 新しいマシンのセットアップ

1. chezmoi を導入する

```sh
# Ubuntu
sh -c "$(curl -fsLS https://get.chezmoi.io)" -- -b "$HOME/.local/bin"
```

```powershell
# Windows
scoop install chezmoi            # 通常の PowerShell で可
# または
winget install twpayne.chezmoi   # 管理者権限不要
# または
choco install chezmoi            # 管理者権限のシェルで実行
```

2. source state の場所を chezmoi に教える (`~/.config/chezmoi/chezmoi.toml`)

```toml
sourceDir = "~/.dotfiles"
```

3. リポジトリを clone して適用する

```sh
git clone git@github.com:gomazarashi/dotfiles.git ~/.dotfiles
chezmoi diff
chezmoi apply
```

## 配置対応表

`home/` 以下のファイルと配置先の対応。`dot_` は先頭の `.` を表す。

### Ubuntu

| source (`home/` 以下) | target |
|---|---|
| `dot_codex/modify_private_config.toml` + `.chezmoitemplates/codex/config.toml` | `~/.codex/config.toml` |
| `dot_codex/AGENTS.md` | `~/.codex/AGENTS.md` |
| `dot_config/opencode/opencode.jsonc` | `~/.config/opencode/opencode.jsonc` |
| `dot_config/opencode/dcp.jsonc` | `~/.config/opencode/dcp.jsonc` |
| `dot_config/opencode/AGENTS.md` | `~/.config/opencode/AGENTS.md` |
| `dot_config/ponytail/config.json.tmpl` | `~/.config/ponytail/config.json` |
| `dot_config/zed/settings.json.tmpl` | `~/.config/zed/settings.json` |
| `dot_gitconfig` | `~/.gitconfig` |
| `dot_config/git/attributes` | `~/.config/git/attributes` |
| `dot_config/git/ignore` | `~/.config/git/ignore` |
| `dot_bashrc` | `~/.bashrc` |
| `dot_profile` | `~/.profile` |
| `dot_config/shell/path.sh` | `~/.config/shell/path.sh` (PATH 設定。`.bashrc` / `.profile` の両方から読み込む) |
| `dot_config/tmux/tmux.conf` | `~/.config/tmux/tmux.conf` |
| `dot_config/ghostty/config` | `~/.config/ghostty/config` |
| `dot_config/nix/nix.conf` | `~/.config/nix/nix.conf` |

### Windows

| source (`home/` 以下) | target |
|---|---|
| `dot_codex/modify_private_config.toml` + `.chezmoitemplates/codex/config.toml` | `%USERPROFILE%\.codex\config.toml` |
| `dot_codex/AGENTS.md` | `%USERPROFILE%\.codex\AGENTS.md` |
| `dot_config/opencode/opencode.jsonc` | `%USERPROFILE%\.config\opencode\opencode.jsonc` |
| `dot_config/opencode/dcp.jsonc` | `%USERPROFILE%\.config\opencode\dcp.jsonc` |
| `dot_config/opencode/AGENTS.md` | `%USERPROFILE%\.config\opencode\AGENTS.md` |
| `bin/opencode-full.ps1` | `%USERPROFILE%\bin\opencode-full.ps1` |
| `AppData/Roaming/ponytail/config.json.tmpl` | `%APPDATA%\ponytail\config.json` |
| `AppData/Roaming/Zed/settings.json.tmpl` | `%APPDATA%\Zed\settings.json` |
| `readonly_Documents/PowerShell/Microsoft.PowerShell_profile.ps1` | `%USERPROFILE%\Documents\PowerShell\Microsoft.PowerShell_profile.ps1` |
| `dot_gitconfig` | `%USERPROFILE%\.gitconfig` |
| `dot_config/git/attributes` | `%USERPROFILE%\.config\git\attributes` |
| `dot_config/git/ignore` | `%USERPROFILE%\.config\git\ignore` |

OS 専用ファイルは `.chezmoiignore` の template 条件で制御する (Linux 専用: `.bashrc` / `.profile` / `.config/{ghostty,nix,ponytail,shell,tmux,zed}`、Windows 専用: `bin/opencode-full.ps1` / `AppData/**` / `Documents/**`)。

## Codex

- `~/.codex/config.toml` は `home/dot_codex/modify_private_config.toml` (modify_ テンプレート、`private_` で権限 600 を維持) で管理する。`home/.chezmoitemplates/codex/config.toml` が portable な設定で、`chezmoi apply` はそこに書かれたキーだけを上書きする。Codex が自動生成した state (`[projects.*]` の trust、`mcp_servers`、`notify`、`marketplaces`、`plugins` など) は TOML マージで保持される。
- portable 設定を変えるときは `home/.chezmoitemplates/codex/config.toml` を編集して apply する。`~/.codex/config.toml` を直接編集しても次の apply で元に戻る。
- マシン固有の上書きは `~/.codex/local.config.toml` (Git 管理外) に書く。読み込ませるには `codex --profile local` を付ける。`--profile` は runtime 系コマンド専用 (`codex` / `exec` / `review` / `resume` / `mcp` など) で、`codex login` / `doctor` / `plugin` / `features` などには付けない。
- apply のたびに `config.toml` は TOML として正規化される (コメント・キー順・空行は保存されない)。
- merge 方式のため、portable 設定からキーを削除しただけでは `~/.codex/config.toml` から消えない場合がある。完全に削除したい場合は target 側のキーを明示的に削除する。
- Codex が state を書き込んでもリポジトリは dirty にならない (実ファイルのため)。upstream [openai/codex#14601](https://github.com/openai/codex/issues/14601) は未解決。

## OpenCode / DCP

- plugin は version pin (`opencode.jsonc`)。起動時に自動 install される
- 既定モデル: `opencode-go/deepseek-v4.1-flash`
- DCP 圧縮は自動許可 (`dcp.jsonc` の `permission: allow`)。native compaction は無効 (`auto/prune: false`)
- DCP を止めるには plugin 配列から削除 (`--pure` で一時全無効化も可)

## Ponytail

- Codex では OFF (`defaultMode: off`)、OpenCode では wrapper 経由で FULL (`PONYTAIL_DEFAULT_MODE=full` をプロセス限定で適用)

```sh
opencode-full  # Linux (alias。実体は PONYTAIL_DEFAULT_MODE=full opencode)
```

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "$HOME\bin\opencode-full.ps1"  # Windows
```

- 新規環境の Codex 導入: `codex plugin marketplace add DietrichGebert/ponytail` → `codex plugin add ponytail@ponytail` → `/hooks` で lifecycle hook を手動 trust
