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

- `dot_bashrc` → `~/.bashrc` (`dot_` は先頭の `.`)
- `dot_config/opencode/opencode.jsonc` → `~/.config/opencode/opencode.jsonc` (ディレクトリ構造はそのまま対応する)
- `AppData/Roaming/Zed/settings.json.tmpl` → `%APPDATA%\Zed\settings.json` (Windows のみ)
- `readonly_Documents/PowerShell/Microsoft.PowerShell_profile.ps1` → `$HOME\Documents\PowerShell\Microsoft.PowerShell_profile.ps1` (Windows のみ)
- `dot_codex/modify_private_config.toml` → `~/.codex/config.toml` (特殊。下の「Codex」を参照)
- `.tmpl` が付いたファイルは**テンプレート**。`{{ ... }}` が展開されてから配置される
- 同じ内容を複数の配置先で使う場合は `.chezmoitemplates/` に 1 つだけ置き、各ファイルから `includeTemplate` で参照する (Zed がこの方式)
- **新しいファイルを管理対象に追加する**: `chezmoi add ~/.config/foo/bar.conf` を実行すると `home/dot_config/foo/bar.conf` が作られる。OS 専用のファイルなら `.chezmoiignore` に条件を追記して他の OS では配置しないようにする

### 2. 差分を確認する (必須)

```sh
chezmoi diff
chezmoi apply --dry-run --verbose
```

確認するポイントは次のとおり。

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

- `chezmoi doctor`: 環境と設定の診断
- `chezmoi managed`: 管理対象の target 一覧
- `chezmoi ignored`: この OS では配置しない target 一覧
- `chezmoi status`: 差分の 1 行サマリ
- `chezmoi diff`: 差分の中身
- `chezmoi apply --dry-run --verbose`: 適用内容のプレビュー (変更しない)

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

## OS 別の配置

- 配置先の一覧は `chezmoi managed` で確認する。OS 専用ファイルは `.chezmoiignore` の template 条件で制御する。
- Linux 専用: `.bashrc` / `.profile` / `.config/{ghostty,nix,shell,tmux,zed}`
- Windows 専用: `AppData/**` / `Documents/**` (Zed は `%APPDATA%\Zed\settings.json`)
- `.config/shell/path.sh` は PATH 設定で、`.bashrc` / `.profile` の両方から読み込む。
- `private_dot_gitconfig-alternate.tmpl` はローカル設定が有効な場合のみ配置する。

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

適用前には `chezmoi diff` と `chezmoi apply --dry-run --verbose` を確認する。これらの出力にはローカルの実値が含まれるため公開しない。この設定のファイルだけを適用する場合は `chezmoi apply ~/.gitconfig ~/.gitconfig-alternate` を使う。無効化後も既存の alternate ファイルは残るが、通常設定からは読み込まれない。

テンプレートの切り替えは `python tests/check_alternate_git.py` で検証できる (Python / chezmoi / Git が必要)。検証には仮の値と一時ディレクトリだけを使う。

## 共通 Agent Skills

Skill は dotfiles では管理せず、`npx skills` で各マシンに直接導入する。使用中の Skill と導入・更新のコマンドは [docs/skills.md](docs/skills.md) を参照。

## Codex

- `~/.codex/config.toml` は `home/dot_codex/modify_private_config.toml` (modify_ テンプレート、`private_` で権限 600 を維持) で管理する。`home/.chezmoitemplates/codex/config.toml` が portable な設定で、`chezmoi apply` はそこに書かれたキーだけを上書きする。Codex が自動生成した state (`[projects.*]` の trust、`mcp_servers`、`notify`、`marketplaces`、`plugins` など) は TOML マージで保持される。
- portable 設定を変えるときは `home/.chezmoitemplates/codex/config.toml` を編集して apply する。`~/.codex/config.toml` を直接編集しても次の apply で元に戻る。
- マシン固有の上書きは `~/.codex/local.config.toml` (Git 管理外) に書く。読み込ませるには `codex --profile local` を付ける。`--profile` は runtime 系コマンド専用 (`codex` / `exec` / `review` / `resume` / `mcp` など) で、`codex login` / `doctor` / `plugin` / `features` などには付けない。
- apply のたびに `config.toml` は TOML として正規化される (コメント・キー順・空行は保存されない)。
- merge 方式のため、portable 設定からキーを削除しただけでは `~/.codex/config.toml` から消えない場合がある。完全に削除したい場合は target 側のキーを明示的に削除する。
- Codex が state を書き込んでもリポジトリは dirty にならない (実ファイルのため)。upstream [openai/codex#14601](https://github.com/openai/codex/issues/14601) は未解決。

## Claude Code

- `~/.claude/settings.json` は `home/dot_claude/modify_settings.json` (modify_ テンプレート) で管理する。Codex と同じく、Claude Code が `/model` や `/config` で書いた内容を保持したまま、管理するキーだけを反映する。
- `home/.chezmoitemplates/claude/settings.json` のキーは `chezmoi apply` のたびに上書きする。`autoMode` は Linux のみ。
- `home/.chezmoitemplates/claude/defaults.json` (`model` / `effortLevel` / `theme`) は未設定のときだけ入れる初期値。`/model` などで変えた値は apply しても戻らない。
- 管理外のキーはそのまま残る。テンプレートからキーを消しても、すでに配置したファイルからは消えない。
- プロジェクト固有の設定 (信頼するリポジトリなど) はここに書かず、そのプロジェクトの `.claude/settings.local.json` に置く。`autoMode` は共有の `.claude/settings.json` からは読まれない。

## OpenCode / DCP

OpenCode v2 を使用し、DCP は **3.2.0** に固定する。[v2 ネイティブ形式](https://opencode.ai/v2/docs/migrate-v1)で設定する。

### Ubuntu 24.04

```sh
curl -fsSL https://opencode.ai/v2/install | bash -s -- --no-modify-path
```

配置先は `~/.opencode/bin`。PATH は `~/.config/shell/path.sh` で管理する。パッケージ管理で導入した v1 は、設定をバックアップして削除してから実行する。curl 導入の v1 は上書きされる。

### Windows

[Scoop versions](https://github.com/ScoopInstaller/Versions/blob/master/bucket/opencode2.json) から導入する。

```powershell
scoop bucket add versions  # 未追加の場合
scoop install versions/opencode2
scoop hold opencode2
```

旧版がある場合は `~/.config/opencode` をバックアップし、`scoop uninstall opencode` または `scoop uninstall opencode2` で削除してから導入する。他方式の旧版もその方式で削除する。Scoop は公式サポート対象外。公式の代替は [Windows standalone バイナリ](https://opencode.ai/v2/docs/)。

### 設定

- 本体は `update: "notify"` で更新を通知し、自動インストールはしない。Windows は `scoop hold` で一括更新からも除外する。
- 既定モデルは `opencode-go/deepseek-v4.1-flash`、`settings.reasoningEffort: "max"`。明示的な variant やプロジェクト設定は既定値を上書きする。Go の認証が必要。
- worktree 内編集と Web 調査は許可する。外部ディレクトリと Shell は確認対象。Shell の例外は既存の `pwd` / `ls` / Git 調査パターンのみ。権限は最後に一致したルールを優先する。
- `share: "disabled"` でセッションの共有を無効にする。
- Skills の配置・自動検出は [docs/skills.md](docs/skills.md) を参照。
- DCP は初回に自動取得し、バージョン固定と `autoUpdate: false` で更新を止める。range 圧縮は自動許可、閾値は 35% / 60%。ユーザーメッセージと指定ファイルを保護し、8 turn の保護・エラー入力整理・重複排除を行う。詳細は `dcp.jsonc` を参照。
- 本体の自動 compaction は無効。手動は `/compact`、DCP の手動圧縮は `/dcp-compress [focus]`。どちらもモデルへのリクエストを伴う。

### 手動更新

Ubuntu は `opencode upgrade` で最新版、`opencode upgrade <version>` で指定版へ更新する。Windows は Scoop 非対応の本体更新コマンドを使わず、任意のタイミングで versions bucket の版へ入れ替える。

```powershell
scoop bucket add versions  # 未追加の場合
scoop update              # bucket の更新のみ
scoop unhold opencode2
scoop uninstall opencode2
scoop install versions/opencode2
scoop hold opencode2
```

両 OS の版をそろえる場合は bucket のバージョンを確認し、Ubuntu でも同じ版を指定する。更新後は `opencode --version` を確認し、OpenCode を再起動する。DCP の更新は `opencode.jsonc` の固定バージョンを変更する。

### 確認

chezmoi 適用後は OpenCode を再起動する。

```sh
opencode --version
opencode debug paths
opencode debug config
opencode models --standalone
opencode plugin list
```

旧版が起動する場合は、Ubuntu では `type -a opencode`、Windows では `Get-Command opencode -All` で実行パスを確認する。`debug config` で上書き元・モデル・権限を確認し、診断出力はそのまま公開しない。初回取得中の `Location plugins did not finish activating` は取得完了後に再試行する。`plugin list` で DCP、認証後の TUI でモデルと effort を確認する。
