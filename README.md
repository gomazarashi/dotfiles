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
- `readonly_Documents/PowerShell/Microsoft.PowerShell_profile.ps1.tmpl` → `$HOME\Documents\PowerShell\Microsoft.PowerShell_profile.ps1` (Windows のみ)
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

## 新しいマシンのセットアップ

1. chezmoi を導入する

```sh
# Ubuntu
sh -c "$(curl -fsLS https://get.chezmoi.io)" -- -b "$HOME/.local/bin"
```

```powershell
# Windows
scoop install chezmoi
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

適用前には `chezmoi diff` と `chezmoi apply --dry-run --verbose` で差分を確認する。これらの出力にはローカルの実値が含まれるため公開しない。この設定のファイルだけを適用する場合は `chezmoi apply ~/.gitconfig ~/.gitconfig-alternate` を使う。無効化後も既存の alternate ファイルは残るが、通常設定からは読み込まれない。

テンプレートの切り替えは `python tests/check_alternate_git.py` で検証できる (Python / chezmoi / Git が必要)。検証には仮の値と一時ディレクトリだけを使う。

### PowerShell の GitHub CLI 認証

Git の identity・SSH 鍵と GitHub CLI の認証は別に設定する。特定のリポジトリで別の GitHub CLI アカウントを使う場合は、同じ Git 管理外の `~/.config/chezmoi/chezmoi.toml` に次を追加する。実際のディレクトリやアカウント名はこのローカルファイルだけに記載し、`chezmoi add` しない。

```toml
[data.alternateGh]
enabled = true
repository = 'C:\path\to\repository'
configDirectory = 'C:\path\to\separate-gh-config'
account = "your-other-account"
```

`repository` は対象リポジトリのルートへの絶対パス、`configDirectory` は別アカウントの認証を保存する絶対パス。有効化時は3項目すべて必要で、未設定または `enabled = false` なら `gh` 関数を配置しない。適用後に新しい PowerShell を開くと反映される。対象リポジトリでは `GH_TOKEN` / `GITHUB_TOKEN` の併用を拒否し、認証設定とヘルプ以外の操作ではアカウントを確認する。

このテンプレートは `python tests/check_gh_profile.py` で検証できる (Python / chezmoi / PowerShell が必要)。ローカルの実値が入るのは適用先のプロファイルであり、ソースには入らない。

## Git のローカル設定

`~/.gitconfig` は通常アカウントの名前・メールを含む共通設定を管理し、最後に `~/.gitconfig-local` を読み込む。`safe.directory` などのマシン固有値はローカル側に置く。ローカル側に書いた値は共通設定より優先されるため、特定のマシンだけ名前・メールを変えることもできる。別アカウントの条件付き設定では、既存の `~/.gitconfig-alternate` に続けて、管理外の `~/.gitconfig-alternate-local` を読み込む。同じ単一値のキーは後者を優先する。

```sh
git config --file ~/.gitconfig-local --add safe.directory /absolute/path/to/repo
```

`git config --global` は管理対象の `~/.gitconfig` に書き込むため、ローカル変更には上記の `--file` を使う。ローカルファイルは各マシンで用意し、`chezmoi add` しない。このリポジトリでは誤追加を防ぐため対応するファイル名を Git の ignore 対象にしている。`private_` は権限指定であり、Git の追跡を防ぐものではない。

## 共通 Agent Skills

Skill は dotfiles では管理せず、`npx skills` で各マシンに直接導入する。使用中の Skill と導入・更新のコマンドは [docs/skills.md](docs/skills.md) を参照。

## Codex

- `~/.codex/config.toml` は `home/dot_codex/modify_private_config.toml` (modify_ テンプレート、`private_` で権限 600 を維持) で管理する。`home/.chezmoitemplates/codex/config.toml` が portable な設定で、`chezmoi apply` はそこに書かれたキーだけを上書きする。Codex が自動生成した state (`[projects.*]` の trust、`mcp_servers`、`notify`、`marketplaces`、`plugins` など) は TOML マージで保持される。
- portable 設定を変えるときは `home/.chezmoitemplates/codex/config.toml` を編集して apply する。`~/.codex/config.toml` を直接編集しても次の apply で元に戻る。
- マシン固有の上書きは `~/.codex/local.config.toml` (Git 管理外) に書く。読み込ませるには `codex --profile local` を付ける。`--profile` は runtime 系コマンド専用 (`codex` / `exec` / `review` / `resume` / `mcp` など) で、`codex login` / `doctor` / `plugin` / `features` などには付けない。
- apply のたびに `config.toml` は TOML として正規化される (コメント・キー順・空行は保存されない)。
- merge 方式のため、portable 設定からキーを削除しただけでは `~/.codex/config.toml` から消えない場合がある。完全に削除したい場合は target 側のキーを明示的に削除する。

## Claude Code

- `~/.claude/settings.json` は `home/dot_claude/modify_settings.json` (modify_ テンプレート) で管理する。Codex と同じく、Claude Code が `/model` や `/config` で書いた内容を保持したまま、管理するキーだけを反映する。
- `home/.chezmoitemplates/claude/settings.json` のキーは `chezmoi apply` のたびに上書きする。
- `home/.chezmoitemplates/claude/defaults.json` (`model` / `effortLevel` / `theme`) は未設定のときだけ入れる初期値。`/model` などで変えた値は apply しても戻らない。
- 管理外のキーはそのまま残る。テンプレートからキーを消しても、すでに配置したファイルからは消えない。
- プロジェクト固有の設定 (信頼するリポジトリなど) はここに書かず、そのプロジェクトの `.claude/settings.local.json` に置く。

## OpenCode / DCP

OpenCode v2 を使用し、[v2 ネイティブ形式](https://opencode.ai/v2/docs/migrate-v1)で設定する。

> 2026-11-14 から試験中で、DCP を外して本体の自動 compaction に任せている。v1 では自動 compaction の動作に不安があったため、v2 で問題が出ないか確認する。問題がなければ、DCP の設定 (`opencode.jsonc` のコメント行と `dcp.jsonc`) とこの README の DCP の記述を削除する。問題が出た場合は `opencode.jsonc` の DCP のコメントを外し、`compaction.auto` を `false` に戻す。DCP を使うときは **3.2.0** に固定する。

### Ubuntu 24.04

```sh
curl -fsSL https://opencode.ai/v2/install | bash -s -- --no-modify-path
```

配置先は `~/.opencode/bin`。PATH は `~/.config/shell/path.sh` で管理する。パッケージ管理で導入した v1 は、設定をバックアップして削除してから実行する。curl で導入した v1 は上書きされる。

### Windows

[Scoop versions](https://github.com/ScoopInstaller/Versions/blob/master/bucket/opencode2.json) から導入する。

```powershell
scoop bucket add versions  # 未追加の場合
scoop install versions/opencode2
```

旧版がある場合は `~/.config/opencode` をバックアップし、`scoop uninstall opencode` または `scoop uninstall opencode2` で削除してから導入する。他の方式で導入した旧版はその方式で削除する。v1 に戻す場合は `scoop install versions/opencode1` を使う。

Scoop は非公式の導入方法で、公式は Windows のパッケージマネージャーに対応していない。公式の導入方法は [Windows standalone バイナリ](https://opencode.ai/v2/docs/) のみ。

### 設定

- モデル・権限・共有・compaction は `opencode.jsonc`、DCP は `dcp.jsonc` を参照する (各項目にコメントがある)。既定モデルを使うには Go の認証が必要。
- 本体は `update: "notify"` で更新を通知するだけで、自動インストールはしない。
- 試験中は本体の自動 compaction を有効にしている (`compaction.auto: true`)。手動の圧縮は `/compact` で、モデルへのリクエストを伴う。
- DCP を戻した場合は、本体の自動 compaction を無効にして DCP に任せる。DCP は初回に自動取得し、バージョン固定と `autoUpdate: false` で更新を止める。手動の圧縮には `/dcp-compress [focus]` を使う。
- Skills の配置・自動検出は [docs/skills.md](docs/skills.md) を参照。

### 手動更新

Ubuntu は `opencode upgrade` で最新版、`opencode upgrade <version>` で指定版へ更新する。Windows では Scoop に対応していない本体の更新コマンドを使わず、任意のタイミングで versions bucket の版へ更新する。

```powershell
scoop update              # bucket の更新のみ
scoop update opencode2    # 実行中の opencode を終了してから実行する
```

実行中の `opencode` があると Scoop は更新をスキップする。アンインストールして入れ直す必要はない。

両 OS の版をそろえる場合は bucket のバージョンを確認し、Ubuntu でも同じ版を指定する。更新後は `opencode --version` を確認し、OpenCode を再起動する。DCP を戻して更新する場合は `opencode.jsonc` の固定バージョンを変更する。

### 確認

chezmoi 適用後は OpenCode を再起動する。

```sh
opencode --version
opencode debug paths
opencode debug config
opencode models --standalone
```

DCP を戻した場合の確認には OpenCode 内の `/dcp` を使う。v2.3.0 では DCP が有効でも `opencode plugin list` が「No plugins found」を返すことがある。

旧版が起動する場合は、Ubuntu では `type -a opencode`、Windows では `Get-Command opencode -All` で実行パスを確認する。診断出力はそのまま公開しない。初回取得中に `Location plugins did not finish activating` と表示された場合は、取得完了後に再試行する。
