# dotfiles

Ubuntu 24.04 と Windows の個人設定を [chezmoi](https://www.chezmoi.io/) で管理する。

- **source state** (設定の元データ) はこのリポジトリの `home/` 以下 (`.chezmoiroot` で指定)
- **target** (実際に配置される `$HOME` 側のファイル) へは symlink/hardlink ではなく実ファイルをコピーする
- 秘密情報やマシン固有のローカル設定 (`~/.config/chezmoi/chezmoi.toml`、SSH 秘密鍵、`*-local`、`local.config.toml` など) は Git で管理しない (`chezmoi add` しない)。`private_` は権限指定であり、Git の追跡を防ぐものではない

## 設定の変更と適用

1. source state (`home/` 以下) を編集する
2. `chezmoi diff` と `chezmoi apply --dry-run --verbose` で差分を確認する
3. `chezmoi apply` で `$HOME` に適用する
4. 他のマシンへ反映する場合は commit / push し、各マシンで `chezmoi update` する

> **重要**: `$HOME` 側のファイル (`~/.bashrc` など) を直接編集しても、次の `chezmoi apply` で上書きされる。変更は必ず source state に書く。

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
- `dot_codex/modify_private_config.toml` → `~/.codex/config.toml` (マージ方式。下の「Codex / Claude Code」を参照)
- `.tmpl` はテンプレート (`{{ ... }}` を展開して配置)。複数の配置先で共有する内容は `.chezmoitemplates/` に置き、`includeTemplate` で参照する (Zed など)
- 新規ファイルの追加は `chezmoi add ~/.config/foo/bar.conf` (`home/dot_config/foo/bar.conf` が作られる)。OS 専用なら `.chezmoiignore` に条件を追記する

### 2. 差分を確認する (必須)

```sh
chezmoi diff
chezmoi apply --dry-run --verbose
```

- Codex や Claude Code が自動生成した state (`[projects.*]` の trust など) が消えていないか
- 意図しないファイル削除や OS 混在の配置 (Linux 用が Windows に出るなど) がないか
- secret / token / credential が含まれていないか (差分出力にはローカルの実値が含まれるため公開しない)

### 3. 適用する

```sh
chezmoi apply            # すべて適用
chezmoi apply ~/.bashrc  # 指定ファイルだけ適用
```

### 4. 他のマシンへ反映する

```sh
# 変更したマシン
git -C ~/.dotfiles add -A
git -C ~/.dotfiles commit -m "..."
git -C ~/.dotfiles push

# 反映先のマシン
chezmoi update           # git pull + chezmoi apply (手動で git pull した場合は chezmoi apply)
```

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

2. `~/.config/chezmoi/chezmoi.toml` に source state の場所を設定する

```toml
sourceDir = "~/.dotfiles"
```

3. リポジトリを clone し、差分を確認して適用する

```sh
git clone git@github.com:gomazarashi/dotfiles.git ~/.dotfiles
chezmoi diff
chezmoi apply
```

## OS 別の配置

配置先の一覧は `chezmoi managed` で確認できる。OS 専用ファイルは `.chezmoiignore` のテンプレート条件で制御する。

- Linux 専用: `.bashrc` / `.profile` / `.config/{ghostty,nix,shell,tmux,zed}` (`.config/shell/path.sh` は PATH 設定で `.bashrc` と `.profile` の両方から読み込む)
- Windows 専用: `AppData/**` / `Documents/**` (Zed は `%APPDATA%\Zed\settings.json`)
- 条件付き配置: `private_dot_gitconfig-alternate.tmpl` はローカル設定で有効な場合のみ配置する

## Git と GitHub CLI の設定

### Git のローカル設定

`~/.gitconfig` は共通設定を管理し、最後に管理外の `~/.gitconfig-local` を読み込む。別アカウント用の `~/.gitconfig-alternate` も同様に `~/.gitconfig-alternate-local` を続けて読み込む。後に読み込むローカル側が優先されるため、`safe.directory` などのマシン固有値やマシン別の名前・メールの上書きに使う。

```sh
git config --file ~/.gitconfig-local --add safe.directory /absolute/path/to/repo
```

`git config --global` は管理対象の `~/.gitconfig` に書き込むため、ローカル変更には `--file` を使う。誤追加防止のため、対応するローカルファイル名は `.gitignore` に登録している。

### ディレクトリ別の Git アカウント

通常の Git identity は維持したまま、指定ディレクトリ以下だけ `includeIf` で `~/.gitconfig-alternate` を読み込み、Git の名前・メールアドレスと SSH 鍵を切り替える。

各マシンの `~/.config/chezmoi/chezmoi.toml` に、`sourceDir` 等を残したまま次を追記する (Ubuntu / Windows 共通)。

```toml
[data.alternateGit]
enabled = true
directory = "/absolute/path/to/repositories"
name = "Your commit name"
email = "you@example.com"
sshKey = "/absolute/path/to/private-key"
```

- `directory` と `sshKey` は絶対パスで指定する。Windows では `C:/path/to/repositories` のように `/` を使うか、TOML の単一引用符で囲む。
- SSH 鍵を別アカウントに登録し、対象リポジトリの GitHub remote に SSH URL を使う。HTTPS URL では `core.sshCommand` による鍵の切り替えは働かない。リポジトリ固有の Git 設定や環境変数はこの設定より優先される。
- 未設定または `enabled = false` の場合は切り替えない。無効化後も既存の `~/.gitconfig-alternate` は残るが、`~/.gitconfig` からは読み込まれなくなる。
- この設定だけを適用する場合は `chezmoi apply ~/.gitconfig ~/.gitconfig-alternate` を使う。
- 検証コマンド: `python tests/check_alternate_git.py` (Python / chezmoi / Git が必要。仮の値と一時ディレクトリのみで検証する)

### PowerShell の GitHub CLI 認証

Git の identity・SSH 鍵と GitHub CLI (`gh`) の認証は別管理になる。特定のリポジトリで別の GitHub CLI アカウントを使う場合は、`~/.config/chezmoi/chezmoi.toml` に次を追記する (ローカルの実値は適用先のプロファイルに展開され、source には入らない)。

```toml
[data.alternateGh]
enabled = true
repository = 'C:\path\to\repository'
configDirectory = 'C:\path\to\separate-gh-config'
account = "your-other-account"
```

- `repository` (対象リポジトリのルート) と `configDirectory` (別アカウントの認証保存先) は絶対パスで指定する。有効化時は 3 項目すべて必須。
- 未設定または `enabled = false` なら `gh` 関数を配置しない。適用後に新しい PowerShell を開くと反映される。
- 対象リポジトリでは `GH_TOKEN` / `GITHUB_TOKEN` の併用を拒否し、認証設定とヘルプ以外の操作ではアカウントを確認する。
- 検証コマンド: `python tests/check_gh_profile.py` (Python / chezmoi / PowerShell が必要)

## 共通 Agent Skills

Skill は dotfiles では管理せず、`npx skills` で各マシンに直接導入する。使用中の Skill と導入・更新・削除の手順は [docs/skills.md](docs/skills.md) を参照。

## Codex / Claude Code

どちらも `modify_` テンプレートで管理し、ツール側が実行時に書き込む state を保持したまま、管理対象のキーだけを上書きする。

マージ方式のため、テンプレートからキーを削除しても target 側に残る場合がある。完全に消す場合は target 側からも明示的に削除する。

### Codex

- `~/.codex/config.toml` は `home/dot_codex/modify_private_config.toml` (`private_` で権限 600 を維持) で管理し、`home/.chezmoitemplates/codex/config.toml` のキーだけを上書きする。
- Codex が自動生成した state (`[projects.*]` の trust、`mcp_servers`、`notify`、`marketplaces`、`plugins` など) は TOML マージで保持される。apply のたびに TOML として正規化されるため、コメント・キー順・空行は保存されない。
- マシン固有の上書きは `~/.codex/local.config.toml` (Git 管理外) に書き、`codex --profile local` で読み込ませる。`--profile` は runtime 系コマンド (`codex` / `exec` / `review` / `resume` / `mcp` など) 専用で、`codex login` / `doctor` / `plugin` / `features` などには付けない。

### Claude Code

- `~/.claude/settings.json` は `home/dot_claude/modify_settings.json` で管理し、`home/.chezmoitemplates/claude/settings.json` のキーを apply のたびに上書きする。
- `home/.chezmoitemplates/claude/defaults.json` (`model` / `effortLevel` / `theme`) は未設定のときだけ補う初期値。Claude Code 内で `/model` や `/config` により変更した値や管理外のキーは apply しても保持される。
- プロジェクト固有の設定 (信頼するリポジトリなど) は各プロジェクトの `.claude/settings.local.json` に置く。

## OpenCode / DCP

OpenCode v2 を使用し、[v2 ネイティブ形式](https://opencode.ai/v2/docs/migrate-v1)で設定する。

> **DCP 試験について (2026-11-14〜)**: 現在 DCP を外し、本体の自動 compaction (`compaction.auto: true`) を試験している (v1 では動作に不安があったため v2 で確認中)。
>
> - 問題なければ: `opencode.jsonc` の DCP コメント行、`dcp.jsonc`、この README の DCP 記述を削除する。
> - 問題が出た場合: `opencode.jsonc` の DCP のコメントを外し、`compaction.auto` を `false` に戻す。DCP のバージョンは **3.2.0** に固定する。

### 導入

**Ubuntu 24.04**

```sh
curl -fsSL https://opencode.ai/v2/install | bash -s -- --no-modify-path
```

配置先は `~/.opencode/bin` (PATH は `~/.config/shell/path.sh` で管理)。パッケージ管理で導入した v1 は設定をバックアップして削除してから実行する (curl 導入の v1 はそのまま上書きされる)。

**Windows**

公式のパッケージマネージャー対応はないため (公式は [Windows standalone バイナリ](https://opencode.ai/v2/docs/) のみ)、非公式の [Scoop versions](https://github.com/ScoopInstaller/Versions/blob/master/bucket/opencode2.json) から導入する。

```powershell
scoop bucket add versions  # 未追加の場合
scoop install versions/opencode2
```

旧版がある場合は `~/.config/opencode` をバックアップし、`scoop uninstall opencode` または `scoop uninstall opencode2` (他の導入方式ならその方式) で削除してから導入する。v1 に戻す場合は `scoop install versions/opencode1` を使う。

### 設定

- モデル・権限・共有・compaction は `opencode.jsonc`、DCP は `dcp.jsonc` で管理する (各項目にコメントあり)。既定モデルを使うには Go の認証が必要。Skills の自動検出は [docs/skills.md](docs/skills.md) を参照。
- 本体は `update: "notify"` で更新通知のみ行い、自動更新はしない。
- 本体の手動圧縮は `/compact` (モデルへのリクエストを伴う)。
- DCP に戻した場合は、初回起動時に自動取得され、バージョン固定と `autoUpdate: false` で更新を止める。DCP の手動圧縮は `/dcp-compress [focus]`。

### 手動更新

- **Ubuntu**: `opencode upgrade` (最新版) または `opencode upgrade <version>` (指定版)
- **Windows**: 本体の更新コマンドは Scoop 非対応のため使わず、実行中の `opencode` を終了してから Scoop で更新する (実行中だとスキップされる。再インストールは不要)。

```powershell
scoop update              # bucket の更新のみ
scoop update opencode2    # 実行中の opencode を終了してから実行する
```

両 OS の版をそろえる場合は bucket のバージョンを確認し、Ubuntu 側で同じ版を指定する。更新後は `opencode --version` を確認して再起動する。DCP を戻して更新する場合は `opencode.jsonc` の固定バージョンを変更する。

### 確認とトラブルシューティング

chezmoi 適用後は OpenCode を再起動する (診断出力はそのまま公開しない)。

```sh
opencode --version
opencode debug paths
opencode debug config
opencode models --standalone
```

- DCP を戻した場合の確認は OpenCode 内の `/dcp` を使う (v2.3.0 では DCP が有効でも `opencode plugin list` が「No plugins found」を返すことがある)。初回取得中に `Location plugins did not finish activating` と出た場合は、取得完了後に再試行する。
- 旧版が起動する場合は、Ubuntu では `type -a opencode`、Windows では `Get-Command opencode -All` で実行パスを確認する。
