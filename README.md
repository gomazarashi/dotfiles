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
- 同じ内容を複数の配置先で使う場合は `.chezmoitemplates/` に 1 つだけ置き、各ファイルから `includeTemplate` で参照する (Zed がこの方式)
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
| `dot_config/zed/settings.json.tmpl` | `~/.config/zed/settings.json` |
| `dot_gitconfig.tmpl` | `~/.gitconfig` |
| `private_dot_gitconfig-alternate.tmpl` | `~/.gitconfig-alternate` (ローカル設定が有効な場合のみ) |
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
| `AppData/Roaming/Zed/settings.json.tmpl` | `%APPDATA%\Zed\settings.json` |
| `readonly_Documents/PowerShell/Microsoft.PowerShell_profile.ps1` | `%USERPROFILE%\Documents\PowerShell\Microsoft.PowerShell_profile.ps1` |
| `dot_gitconfig.tmpl` | `%USERPROFILE%\.gitconfig` |
| `private_dot_gitconfig-alternate.tmpl` | `%USERPROFILE%\.gitconfig-alternate` (ローカル設定が有効な場合のみ) |
| `dot_config/git/attributes` | `%USERPROFILE%\.config\git\attributes` |
| `dot_config/git/ignore` | `%USERPROFILE%\.config\git\ignore` |

OS 専用ファイルは `.chezmoiignore` の template 条件で制御する (Linux 専用: `.bashrc` / `.profile` / `.config/{ghostty,nix,shell,tmux,zed}`、Windows 専用: `AppData/**` / `Documents/**`)。

## ディレクトリ別の Git アカウント

通常の Git identity はそのまま維持し、ローカル設定で指定したディレクトリ以下だけ `includeIf` で `~/.gitconfig-alternate` を読み込む。Git の名前・メールアドレスと、SSH 認証に使う鍵を切り替える。

各マシンの `~/.config/chezmoi/chezmoi.toml` に、既存の `sourceDir` 等を残したまま次の設定を追加する。値は各マシンに合わせて置き換える。このファイルや SSH 秘密鍵はリポジトリで管理しない。

```toml
[data.alternateGit]
enabled = true
directory = "/absolute/path/to/repositories"
name = "Your commit name"
email = "you@example.com"
sshKey = "/absolute/path/to/private-key"
```

Windows のパスは `C:/path/to/repositories` のように `/` を使うか、TOML の単一引用符で囲む。ディレクトリ・鍵のパスには絶対パスを指定する。Ubuntu / Windows とも同じ仕組みで、設定未登録または `enabled = false` のマシンでは切り替えを行わない。

鍵を別アカウントに登録し、対象リポジトリの GitHub remote に SSH URL を使用する。HTTPS URL では `core.sshCommand` による鍵の切り替えは働かない。リポジトリ固有の Git 設定や環境変数による上書きは、この設定より優先される。

適用前には `chezmoi diff` と `chezmoi apply --dry-run --verbose` を確認する。これらの出力にはローカルの実値が含まれるため公開しない。今回のファイルだけを適用する場合は `chezmoi apply ~/.gitconfig ~/.gitconfig-alternate` を使う。無効化後も既存の alternate ファイルは残るが、通常設定からは読み込まれない。

テンプレートの切り替えは `python tests/check_alternate_git.py` で検証できる (Python / chezmoi / Git が必要)。検証には仮の値と一時ディレクトリだけを使う。


## 共通 Agent Skills

Codex / Claude Code / OpenCode v2 のグローバル Skill は [`npx skills`](https://github.com/vercel-labs/skills) で管理する。Skill の本文は dotfiles に置かない。取得元の一覧だけを `home/.chezmoidata/skills.yaml` に持ち、`chezmoi apply` 時に `home/.chezmoiscripts/` のスクリプトが導入する (Windows は `.ps1`、Ubuntu は `.sh`)。

```yaml
skills:
  - repo: DietrichGebert/ponytail   # ponytail / -review / -audit / -debt / -gain / -help
  - repo: nanaism/yomiyasu
```

導入は `-g -a claude-code -a codex --copy` で行う。実ファイルを `~/.claude/skills/` と `~/.agents/skills/` に置き、Windows でも symlink 権限を要しない。OpenCode v2 は `opencode.jsonc` の `skills: ["~/.agents/skills"]` で `~/.agents/skills` を参照するため、`-a opencode` は付けない (`~/.config/opencode/skills/` に入れると二重に見える)。各マシンの導入状態は `~/.agents/.skill-lock.json` に記録され、Git には入らない。

| ツール | 配置先 | 呼び出し |
|---|---|---|
| Codex | `~/.agents/skills/` | `$ponytail`、`$yomiyasu` |
| Claude Code | `~/.claude/skills/` | `/ponytail`、`/yomiyasu` |
| OpenCode v2 | `~/.agents/skills/` を `skills` 設定で参照 | `@ponytail`、`@yomiyasu` |

### Skill の追加

`skills.yaml` に取得元を1行足して `chezmoi apply` する。一覧が変わったときだけスクリプトが走る。リポジトリ内の Skill は全件導入する (`--skill '*'`)。一部だけ必要な場合は、スクリプトの `--skill` を調整する。

### 更新

```sh
npx skills update -g -y   # 全 Skill を upstream の最新へ
npx skills ls -g          # 導入状況の確認
```

更新はハッシュの差分で判定される。導入を指定バージョンに固定したい場合は、取得元にタグや commit を指定する。導入前に内容を確認するときは `npx skills add <repo> -l` で Skill 名を見る。Skill は agent の権限で動くため、新しい取得元を足すときは内容を確認する。

### 削除

`skills.yaml` から消しただけでは各マシンの配置は消えない。`npx skills remove -g <name>` で削除する。

### 管理外

`~/.claude/skills/synced/` (アカウント同期)、`~/.codex/skills/.system/` (Codex 標準)、プラグイン同梱の Skill (drawio など) はこの仕組みの対象外。Cowork / Claude のクラウドセッションはローカル配置を読まない。

配置先の根拠: [Codex](https://learn.chatgpt.com/docs/build-skills)、[Claude Code](https://code.claude.com/docs/en/skills)、[OpenCode v2](https://opencode.ai/v2/docs/skills)。

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
- DCP 圧縮は自動許可 (`dcp.jsonc` の `permission: allow`)。native compaction は無効 (`auto: false`。v2 で未対応の `prune` は指定しない)
- DCP を止めるには plugin 配列から削除する
- OpenCode v2 を使用。コマンドは `opencode` のまま、DCP 3.2.0 を利用する。Ponytail などの Skill は「共通 Agent Skills」で導入する。モデルと権限は v2 が読み込める既存形式を維持する (参照: [v2 移行ガイド](https://opencode.ai/v2/docs/migrate-v1))。
- Windows の導入: `scoop bucket add versions` → 既存 v1 の設定をバックアップ → `scoop uninstall opencode` → `scoop install versions/opencode2`。実機では2.0.26を確認済み。コマンド名は `opencode`。Scoop の [opencode2 manifest](https://github.com/ScoopInstaller/Versions/blob/master/bucket/opencode2.json) がバイナリとハッシュを管理する。
- Linux の導入: `curl -fsSL https://opencode.ai/v2/install | bash -s -- --version 2.0.26 --no-modify-path`。PATH は dotfiles で管理しているため installer では変更しない。
