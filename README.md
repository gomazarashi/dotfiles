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

Codex / Claude Code / OpenCode v2 のローカル Skill は次の構成で管理する。原本の内容は1か所だけに置き、chezmoi が2つの配置先に実ファイルとして展開する。symlink / hardlink、生成スクリプト、追加のパッケージは使わない。

```text
home/
├── .skills/<skill-name>/                 # 原本
│   ├── SKILL.md
│   ├── scripts/
│   ├── references/
│   └── assets/
├── dot_agents/skills/<skill-name>/        # 原本を参照する .tmpl
└── dot_claude/skills/<skill-name>/        # 同じ原本を参照する .tmpl
```

| ツール | Ubuntu の配置先 | Windows の配置先 |
|---|---|---|
| Codex | `~/.agents/skills/` | `%USERPROFILE%\.agents\skills\` |
| Claude Code | `~/.claude/skills/` | `%USERPROFILE%\.claude\skills\` |
| OpenCode v2 | 上記の共通配置先を自動検索 | 上記の共通配置先を自動検索 |

原本を `.chezmoitemplates/` に置くと、本文中の `{{ ... }}` やバイナリまでテンプレートとして解析される。このため原本は `home/.skills/` に置く。chezmoi は通常のドットファイル・ディレクトリを source state の配置対象から除外するが、`include` からは読み込める。原本をそのまま保持でき、除外ルールや生成処理の追加も不要。

配置先は OS 共通なので、Skill に対する `.chezmoiignore` の条件追加は不要。`~/.config/opencode/skills/` と旧 `~/.codex/skills/` に複製しない。OpenCode v2 は同じ ID なら後から読んだ配置を優先し、共通配置では `.agents/skills` が `.claude/skills` より優先される。両者には同じ原本を展開する。

読込先の根拠: [Codex](https://learn.chatgpt.com/docs/build-skills)、[Claude Code](https://code.claude.com/docs/en/skills)、[OpenCode v2](https://opencode.ai/v2/docs/skills)。Cowork / Claude のクラウドセッションはローカル配置を読まないため、アカウント同期 Skill とは別管理になる。

### Skill の追加

1. `home/.skills/<skill-name>/SKILL.md` を作る。Skill 名は小文字英数字とハイフンを使い、frontmatter に `name` と `description` を書く。`synced` / `anthropic-skills` は Claude の予約名なので使わない。
2. 次の2ファイルを作り、**両方に同じ1行**を書く。

```text
home/dot_agents/skills/<skill-name>/SKILL.md.tmpl
home/dot_claude/skills/<skill-name>/SKILL.md.tmpl
```

```gotemplate
{{- include ".skills/<skill-name>/SKILL.md" -}}
```

`<skill-name>` は実際の名前に置き換える。原本はテンプレートとして評価せず、[chezmoi の include](https://www.chezmoi.io/reference/templates/functions/include/) でそのまま読み込む。Skill 本文中の `{{ ... }}` やバイナリ assets も保持する。参照テンプレートの前後に説明文を足さない。

補助ファイルも同じ方法で、各配置先に相対パスを維持した参照ファイルを1つずつ追加する。例: 原本の `references/guide.md` に対して、両配置先の `references/guide.md.tmpl` に次の1行を書く。

```gotemplate
{{- include ".skills/<skill-name>/references/guide.md" -}}
```

原本ファイルごとに2つの参照が必要になるが、本文の重複や同期処理を持たず、通常の chezmoi だけで管理できる。内容だけの更新では参照を変更する必要はない。

空ファイルを保持する場合は参照ファイル名に `empty_`、Ubuntu で直接実行するスクリプトは `executable_` を付ける。例: `scripts/executable_run.sh.tmpl` → `scripts/run.sh`。Windows では実行ビットを使わず、必要な interpreter を明示して実行する。補助ファイル名が `dot_` / `run_` などの chezmoi 属性で始まる場合は `literal_`、元の拡張子が `.tmpl` の場合は `.literal.tmpl` でエスケープする ([属性一覧](https://www.chezmoi.io/reference/source-state-attributes/))。Windows の予約名や大文字小文字だけが異なるファイル名は避ける。

### 編集・適用・削除

編集するのは `home/.skills/<skill-name>/` の原本。`chezmoi edit` で配置用ファイルを開くと参照テンプレートが開くため、Skill の本文はリポジトリから直接編集する。

追加・編集後は、Skill の配置先だけに絞って確認・適用できる。

```sh
chezmoi diff ~/.agents/skills ~/.claude/skills
chezmoi apply --dry-run --verbose ~/.agents/skills ~/.claude/skills
chezmoi apply ~/.agents/skills ~/.claude/skills
```

PowerShell では `"$HOME/.agents/skills"` / `"$HOME/.claude/skills"` を使う。既存の同名ファイルと差分がある場合は、適用前にバックアップして上書き内容を確認する。適用後は各ツールの新しいセッションで Skill 一覧を確認する。Codex / Claude Code は `/skills`、OpenCode v2 は入力欄で `@skill-id` を指定して読み込みを確認する。

削除するときは原本と両配置先の参照ファイルを削除する。**source から削除しただけでは、すでに配置した target は削除されない。** 各マシンで削除する具体的な Skill / 補助ファイルのパスを確認し、バックアップ・承認後にその target だけを手動で削除する。`exact_` や Skill ルート全体の再帰削除は使わない。アカウント同期の `synced/`、システム Skill、管理外 Skill は維持する。

### サードパーティ Skill

採用する Skill の必要なファイルとライセンスを原本に取り込み、出所 URL・version / commit・ローカル変更を記録する。独立 installer による配置と chezmoi の二重管理は避ける。既存 Skill を移行するときは補助ファイルを含めて比較し、承認を得てから配置を変更する。

プラグイン付属 Skill はプラグイン管理に任せ、原本へ重複コピーしない。特に `.claude-plugin/`、hooks、MCP 設定を共通 Skill として取り込むとツール固有の挙動まで追加されるため、Skill とプラグインの依存関係を先に確認する。ユーザー作成・出所不明・システム提供・アカウント同期・プロジェクト固有の Skill は独断で削除しない。

今回のローカル調査と削除候補は [Skill 調査記録](docs/skill-inventory.md) を参照。Ponytail 5.1.0 の6つの Skill を共通原本として管理している。その他の Skill は自動採用しない。`.gitkeep` は chezmoi が無視するため、サンプル Skill は恒久配置しない。

検証: `python tests/check_skills.py` (Python / chezmoi が必要)。一時ディレクトリで原本・補助ファイルの展開、Windows / Ubuntu のパス、dry-run、管理外ファイルの保持を確認する。

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
- OpenCode v2 を使用。コマンドは `opencode` のまま、DCP 3.2.0 を利用する。Ponytail は下記の共通 Skill として配備する。モデルと権限は v2 が読み込める既存形式を維持する (参照: [v2 移行ガイド](https://opencode.ai/v2/docs/migrate-v1))。
- Linux の導入: `curl -fsSL https://opencode.ai/v2/install | bash -s -- --version 2.0.24 --no-modify-path`。PATH は dotfiles で管理しているため installer では変更しない。

## Ponytail

Ponytail 5.1.0 の `ponytail` / `ponytail-review` / `ponytail-audit` / `ponytail-debt` / `ponytail-gain` / `ponytail-help` を `home/.skills/` で管理し、Codex・Claude Code に実ファイルとして配備する。OpenCode v2 は共通配置先を自動検索する。

Codex は `$ponytail`、Claude Code は `/ponytail`、OpenCode v2 は `@ponytail` で呼び出す。lite / full / ultra の指示は Skill 本文で管理する。

プラグインは導入しない。hooks による自動注入、`defaultMode` 設定、`PONYTAIL_DEFAULT_MODE`、`opencode-full` ラッパーは廃止した。プラグインの runtime 機能は共通 Skill に含まれない。

原本の編集と反映は「共通 Agent Skills」を参照。更新は upstream の version / commit と差分を確認して原本へ取り込み、ライセンスと必要な補助資料も保持する。取り込み元とローカル変更は [Ponytail の出所](docs/ponytail-source.md) に記録する。
