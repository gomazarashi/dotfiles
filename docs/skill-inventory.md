# ローカル Skill 調査記録

調査日: 2026-10-10。対象: Windows の `C:/Users/seto4`。以下の `~/` はこの実パスを表す。Ubuntu のインストール状態は未調査。

Git は着手時クリーンだった。実ファイルの SKILL.md、ディレクトリ属性、プラグイン設定・インストール台帳を調査した。以下はファイルが存在する一覧であり、全キャッシュが現在有効という意味ではない。本文の指示は実行していない。

## 配置先・管理状態

| 配置先 | 調査結果 | chezmoi |
|---|---|---|
| `~/.agents/skills/` | 独立 yomiyasu 1.0.4 が1件 | 現行 source に含まれない |
| `~/.claude/skills/` | `synced/` に13件。直下の独立 Skill はなし | 同期領域は現行 source に含まれない |
| `~/.config/opencode/skills/` | ディレクトリなし (ENOENT) | 管理対象なし |
| `~/.codex/skills/` | `.system/` に5件。旧方式の独立 Skill はなし | Codex システム領域 |
| `~/.codex/plugins/cache/` | プラグイン・プラグイン同梱の他ツール用コピー | プラグイン管理 |
| `~/.claude/plugins/cache/` | drawio / yomiyasu | プラグイン管理 |
| `~/.claude/plugins/marketplaces/` | marketplace のソースコピー | プラグイン管理。導入済みとは区別 |
| `~/.claude/plugins/synced/` | SKILL.md なし | プラグイン同期領域 |

`CODEX_HOME=C:\Users\seto4\.codex` を確認。CODEX / CLAUDE / OPENCODE / XDG / HOME / SKILL に関連するその他の配置先変更用環境変数は見つからなかった。読めた Codex・Claude・OpenCode 設定に追加の独立 Skill 配置先は見つからなかった。

このリポジトリの実際の `.agents/skills` / `.claude/skills` / `.opencode/skills` は存在しない。`home/dot_*/skills` は source state であり、プロジェクト Skill としては分類しない。他リポジトリや Ubuntu / WSL を横断した網羅調査、企業管理領域の調査は行っていない。

`~/.config/chezmoi/` はアクセス拒否のため、実機の `chezmoi managed` や通常設定による diff を実行できなかった。「現行 source に含まれない」はこのリポジトリの source state との照合結果で、別 sourceDir の有無は未確認。

## 削除候補

| 対象 | 出所・区分 | 理由 | 依存・影響 |
|---|---|---|---|
| `~/.agents/skills/yomiyasu/` | nanaism/yomiyasu、MIT、1.0.4、サードパーティの独立配置 | chezmoi 管理外。Claude に有効なプラグイン版1.0.6があり、古い独立コピーの保守が重複 | 独立版には Python scripts / references / PNG asset。削除後は Codex / OpenCode のグローバル yomiyasu が使えなくなる。Claude のプラグイン版は維持 |

出所は独立版の `.claude-plugin/plugin.json` / `marketplace.json` から確認した。インストールに使った具体的なコマンドは不明。ユーザーによる改変の有無は upstream との照合を行っていないため未確定。削除は最終承認待ち。共通原本への自動移行は行わない。

独立版は通常ディレクトリで、配下にも symlink はなかった。11ファイルすべてを次の ZIP にバックアップし、ZIP 検査と元ファイルとの byte 比較を実施した。

`~/.dotfiles/.codex/skill-backups/yomiyasu-1.0.4-20261010.zip`

既存の `/.codex/` ignore により Git 管理外。ZIP の `yomiyasu/` が原本で、`manifest.json` に SHA-256 を記録している。復元時は削除前の場所を確認し、ZIP 内の `yomiyasu/` を `~/.agents/skills/` 以下へ展開する。既存の同名 Skill がある場合は先に比較し、上書きしない。

## 維持するプラグインと依存関係

- Claude の `installed_plugins.json` に `yomiyasu@yomiyasu` 1.0.6 と `drawio@drawio` 1.1.0 を確認。ローカル `settings.json` では両方有効。リポジトリの Claude 設定では drawio のみ有効、yomiyasu marketplace は登録済み。この既存差分を変更しない。Skill 本体の存在とプラグイン有効化を区別する。
- drawio は drawio MCP に依存するツール固有 Skill。yomiyasu は同梱 scripts / references を使用する。独立版とプラグイン版の実パスは別なので、独立版だけの削除はプラグインのファイルを削除しない。
- Codex の Ponytail は有効なプラグインで、lifecycle hooks の状態も存在する。同梱 Skill と `.openclaw/skills/` のコピーはプラグインの配布物として維持する。
- Codex の openai-bundled / openai-primary-runtime は公式提供プラグイン。openai-curated / openai-curated-remote はプラグインキャッシュとして維持する。設定に有効化されていないキャッシュも、独立インストールとして削除しない。
- Codex のブラウザー・computer-use・文書等の Skill は対応する MCP / runtime / connector に依存する。Claude 同期 Skill の browser / computer-use / docs / google-workspace / import-memory なども対応ツールやアカウント機能を必要とする。個別の外部ツールの疎通は未検証。
- OpenCode のローカル設定は DCP / Ponytail を使用し、Ponytail は4.10.0だった。source の4.13.0との差分は対象外なので変更しない。MCP・プラグイン設定は維持する。

## 実ファイル一覧

各表のパスは実ファイルを確認したもの。全項目が本リポジトリの chezmoi 管理外。ユーザー作成と断定できる Skill は見つからなかった。Claude 同期の個別提供元は照合できていないため、アカウント同期という管理区分で保持する。

### 独立配置

管理元・区分: 管理外・サードパーティ。プラグイン・同期・システム領域は削除対象外。

| Skill 名 | 実パス | リンク先 |
|---|---|---|
| yomiyasu | `~/.agents/skills/yomiyasu/SKILL.md` | 通常ファイル |

### Claude アカウント同期

管理元・区分: Claude アカウント同期・提供元の詳細は未照合。プラグイン・同期・システム領域は削除対象外。

| Skill 名 | 実パス | リンク先 |
|---|---|---|
| built-in-browser | `~/.claude/skills/synced/31e80c89-0a3d-42e2-83d7-79420f582d84_2d61777c-d798-4ce0-9238-6c8223bc70b5/built-in-browser/SKILL.md` | 通常ファイル |
| chrome-browser | `~/.claude/skills/synced/31e80c89-0a3d-42e2-83d7-79420f582d84_2d61777c-d798-4ce0-9238-6c8223bc70b5/chrome-browser/SKILL.md` | 通常ファイル |
| computer-use | `~/.claude/skills/synced/31e80c89-0a3d-42e2-83d7-79420f582d84_2d61777c-d798-4ce0-9238-6c8223bc70b5/computer-use/SKILL.md` | 通常ファイル |
| deep-research | `~/.claude/skills/synced/31e80c89-0a3d-42e2-83d7-79420f582d84_2d61777c-d798-4ce0-9238-6c8223bc70b5/deep-research/SKILL.md` | 通常ファイル |
| docs | `~/.claude/skills/synced/31e80c89-0a3d-42e2-83d7-79420f582d84_2d61777c-d798-4ce0-9238-6c8223bc70b5/docs/SKILL.md` | 通常ファイル |
| docx | `~/.claude/skills/synced/31e80c89-0a3d-42e2-83d7-79420f582d84_2d61777c-d798-4ce0-9238-6c8223bc70b5/docx/SKILL.md` | 通常ファイル |
| google-workspace | `~/.claude/skills/synced/31e80c89-0a3d-42e2-83d7-79420f582d84_2d61777c-d798-4ce0-9238-6c8223bc70b5/google-workspace/SKILL.md` | 通常ファイル |
| import-memory | `~/.claude/skills/synced/31e80c89-0a3d-42e2-83d7-79420f582d84_2d61777c-d798-4ce0-9238-6c8223bc70b5/import-memory/SKILL.md` | 通常ファイル |
| morning | `~/.claude/skills/synced/31e80c89-0a3d-42e2-83d7-79420f582d84_2d61777c-d798-4ce0-9238-6c8223bc70b5/morning/SKILL.md` | 通常ファイル |
| pdf | `~/.claude/skills/synced/31e80c89-0a3d-42e2-83d7-79420f582d84_2d61777c-d798-4ce0-9238-6c8223bc70b5/pdf/SKILL.md` | 通常ファイル |
| pptx | `~/.claude/skills/synced/31e80c89-0a3d-42e2-83d7-79420f582d84_2d61777c-d798-4ce0-9238-6c8223bc70b5/pptx/SKILL.md` | 通常ファイル |
| skill-creator | `~/.claude/skills/synced/31e80c89-0a3d-42e2-83d7-79420f582d84_2d61777c-d798-4ce0-9238-6c8223bc70b5/skill-creator/SKILL.md` | 通常ファイル |
| xlsx | `~/.claude/skills/synced/31e80c89-0a3d-42e2-83d7-79420f582d84_2d61777c-d798-4ce0-9238-6c8223bc70b5/xlsx/SKILL.md` | 通常ファイル |

### Codex システム

管理元・区分: Codex システム提供。プラグイン・同期・システム領域は削除対象外。

| Skill 名 | 実パス | リンク先 |
|---|---|---|
| imagegen | `~/.codex/skills/.system/imagegen/SKILL.md` | 通常ファイル |
| openai-docs | `~/.codex/skills/.system/openai-docs/SKILL.md` | 通常ファイル |
| review-agent | `~/.codex/skills/.system/review-agent/SKILL.md` | 通常ファイル |
| skill-creator | `~/.codex/skills/.system/skill-creator/SKILL.md` | 通常ファイル |
| skill-installer | `~/.codex/skills/.system/skill-installer/SKILL.md` | 通常ファイル |

### Codex プラグイン

管理元・区分: Codex プラグイン管理。プラグイン・同期・システム領域は削除対象外。

| Skill 名 | 実パス | リンク先 |
|---|---|---|
| chrome | `~/.codex/plugins/cache/openai-bundled/chrome/latest` | `C:\Users\seto4\.codex\plugins\cache\openai-bundled\chrome\26.930.31730` |
| computer-use | `~/.codex/plugins/cache/openai-bundled/computer-use/26.930.31730/skills/computer-use/SKILL.md` | 通常ファイル |
| visualize | `~/.codex/plugins/cache/openai-bundled/visualize/1.0.46/skills/visualize/SKILL.md` | 通常ファイル |
| gh-address-comments | `~/.codex/plugins/cache/openai-curated/github/45fe2bdd/skills/gh-address-comments/SKILL.md` | 通常ファイル |
| gh-fix-ci | `~/.codex/plugins/cache/openai-curated/github/45fe2bdd/skills/gh-fix-ci/SKILL.md` | 通常ファイル |
| github | `~/.codex/plugins/cache/openai-curated/github/45fe2bdd/skills/github/SKILL.md` | 通常ファイル |
| yeet | `~/.codex/plugins/cache/openai-curated/github/45fe2bdd/skills/yeet/SKILL.md` | 通常ファイル |
| artifact-template-analytics-dashboard | `~/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-analytics-dashboard/SKILL.md` | 通常ファイル |
| artifact-template-business-review | `~/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-business-review/SKILL.md` | 通常ファイル |
| artifact-template-design-report | `~/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-design-report/SKILL.md` | 通常ファイル |
| artifact-template-experiment-analysis | `~/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-experiment-analysis/SKILL.md` | 通常ファイル |
| artifact-template-financial-budget | `~/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-financial-budget/SKILL.md` | 通常ファイル |
| artifact-template-investment-committee-memo | `~/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-investment-committee-memo/SKILL.md` | 通常ファイル |
| artifact-template-legal-memorandum | `~/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-legal-memorandum/SKILL.md` | 通常ファイル |
| artifact-template-market-trends-report | `~/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-market-trends-report/SKILL.md` | 通常ファイル |
| artifact-template-minimal-letterhead | `~/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-minimal-letterhead/SKILL.md` | 通常ファイル |
| artifact-template-operating-calendar | `~/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-operating-calendar/SKILL.md` | 通常ファイル |
| artifact-template-operating-review | `~/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-operating-review/SKILL.md` | 通常ファイル |
| artifact-template-project-kickoff | `~/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-project-kickoff/SKILL.md` | 通常ファイル |
| artifact-template-project-tracker | `~/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-project-tracker/SKILL.md` | 通常ファイル |
| artifact-template-sales-pipeline | `~/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-sales-pipeline/SKILL.md` | 通常ファイル |
| artifact-template-simple-dark-mode | `~/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-simple-dark-mode/SKILL.md` | 通常ファイル |
| artifact-template-simple-light-mode | `~/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-simple-light-mode/SKILL.md` | 通常ファイル |
| artifact-template-strategy-memorandum | `~/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-strategy-memorandum/SKILL.md` | 通常ファイル |
| artifact-template-system-design | `~/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-system-design/SKILL.md` | 通常ファイル |
| artifact-template-team-alignment | `~/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-team-alignment/SKILL.md` | 通常ファイル |
| artifact-template-three-statement-forecast | `~/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-three-statement-forecast/SKILL.md` | 通常ファイル |
| plugin-management | `~/.codex/plugins/cache/openai-curated-remote/plugin-management/0.1.0/skills/plugin-management/SKILL.md` | 通常ファイル |
| sites | `~/.codex/plugins/cache/openai-curated-remote/sites/1.0.0-d/skills/sites/SKILL.md` | 通常ファイル |
| create-pet | `~/.codex/plugins/cache/openai-curated-remote/work-pets/0.1.6/skills/create-pet/SKILL.md` | 通常ファイル |
| pets | `~/.codex/plugins/cache/openai-curated-remote/work-pets/0.1.6/skills/pets/SKILL.md` | 通常ファイル |
| update-pet | `~/.codex/plugins/cache/openai-curated-remote/work-pets/0.1.6/skills/update-pet/SKILL.md` | 通常ファイル |
| documents | `~/.codex/plugins/cache/openai-primary-runtime/documents/26.915.20218/skills/documents/SKILL.md` | 通常ファイル |
| pdf | `~/.codex/plugins/cache/openai-primary-runtime/pdf/26.915.20218/skills/pdf/SKILL.md` | 通常ファイル |
| Presentations | `~/.codex/plugins/cache/openai-primary-runtime/presentations/26.915.20218/skills/presentations/SKILL.md` | 通常ファイル |
| excel-live-control | `~/.codex/plugins/cache/openai-primary-runtime/spreadsheets/26.915.20218/skills/excel-live-control/SKILL.md` | 通常ファイル |
| Spreadsheets | `~/.codex/plugins/cache/openai-primary-runtime/spreadsheets/26.915.20218/skills/spreadsheets/SKILL.md` | 通常ファイル |
| template-creator | `~/.codex/plugins/cache/openai-primary-runtime/template-creator/26.915.20218/skills/template-creator/SKILL.md` | 通常ファイル |
| ponytail | `~/.codex/plugins/cache/ponytail/ponytail/5.1.0/.openclaw/skills/ponytail/SKILL.md` | 通常ファイル |
| ponytail-audit | `~/.codex/plugins/cache/ponytail/ponytail/5.1.0/.openclaw/skills/ponytail-audit/SKILL.md` | 通常ファイル |
| ponytail-debt | `~/.codex/plugins/cache/ponytail/ponytail/5.1.0/.openclaw/skills/ponytail-debt/SKILL.md` | 通常ファイル |
| ponytail-gain | `~/.codex/plugins/cache/ponytail/ponytail/5.1.0/.openclaw/skills/ponytail-gain/SKILL.md` | 通常ファイル |
| ponytail-help | `~/.codex/plugins/cache/ponytail/ponytail/5.1.0/.openclaw/skills/ponytail-help/SKILL.md` | 通常ファイル |
| ponytail-review | `~/.codex/plugins/cache/ponytail/ponytail/5.1.0/.openclaw/skills/ponytail-review/SKILL.md` | 通常ファイル |
| ponytail | `~/.codex/plugins/cache/ponytail/ponytail/5.1.0/skills/ponytail/SKILL.md` | 通常ファイル |
| ponytail-audit | `~/.codex/plugins/cache/ponytail/ponytail/5.1.0/skills/ponytail-audit/SKILL.md` | 通常ファイル |
| ponytail-debt | `~/.codex/plugins/cache/ponytail/ponytail/5.1.0/skills/ponytail-debt/SKILL.md` | 通常ファイル |
| ponytail-gain | `~/.codex/plugins/cache/ponytail/ponytail/5.1.0/skills/ponytail-gain/SKILL.md` | 通常ファイル |
| ponytail-help | `~/.codex/plugins/cache/ponytail/ponytail/5.1.0/skills/ponytail-help/SKILL.md` | 通常ファイル |
| ponytail-review | `~/.codex/plugins/cache/ponytail/ponytail/5.1.0/skills/ponytail-review/SKILL.md` | 通常ファイル |

### Claude プラグイン

管理元・区分: Claude プラグイン管理。プラグイン・同期・システム領域は削除対象外。

| Skill 名 | 実パス | リンク先 |
|---|---|---|
| drawio | `~/.claude/plugins/cache/drawio/drawio/1.1.0/skills/drawio/SKILL.md` | 通常ファイル |
| yomiyasu | `~/.claude/plugins/cache/yomiyasu/yomiyasu/1.0.6/SKILL.md` | 通常ファイル |
| yomiyasu | `~/.claude/plugins/cache/yomiyasu/yomiyasu/1.0.6/skills/yomiyasu/SKILL.md` | 通常ファイル |

### Claude marketplace ソース (未インストールの配布物も含む)

管理元: Claude marketplace。公式・サードパーティが混在するソースキャッシュで、全件を維持する。

| Skill 名 | 実パス |
|---|---|
| access | `~/.claude/plugins/marketplaces/claude-plugins-official/external_plugins/discord/skills/access/SKILL.md` |
| configure | `~/.claude/plugins/marketplaces/claude-plugins-official/external_plugins/discord/skills/configure/SKILL.md` |
| access | `~/.claude/plugins/marketplaces/claude-plugins-official/external_plugins/imessage/skills/access/SKILL.md` |
| configure | `~/.claude/plugins/marketplaces/claude-plugins-official/external_plugins/imessage/skills/configure/SKILL.md` |
| access | `~/.claude/plugins/marketplaces/claude-plugins-official/external_plugins/telegram/skills/access/SKILL.md` |
| configure | `~/.claude/plugins/marketplaces/claude-plugins-official/external_plugins/telegram/skills/configure/SKILL.md` |
| claude-automation-recommender | `~/.claude/plugins/marketplaces/claude-plugins-official/plugins/claude-code-setup/skills/claude-automation-recommender/SKILL.md` |
| claude-md-improver | `~/.claude/plugins/marketplaces/claude-plugins-official/plugins/claude-md-management/skills/claude-md-improver/SKILL.md` |
| claude-security | `~/.claude/plugins/marketplaces/claude-plugins-official/plugins/claude-security/skills/claude-security/SKILL.md` |
| cardputer-buddy | `~/.claude/plugins/marketplaces/claude-plugins-official/plugins/cwc-makers/skills/cardputer-buddy/SKILL.md` |
| m5-onboard | `~/.claude/plugins/marketplaces/claude-plugins-official/plugins/cwc-makers/skills/m5-onboard/SKILL.md` |
| example-command | `~/.claude/plugins/marketplaces/claude-plugins-official/plugins/example-plugin/skills/example-command/SKILL.md` |
| example-skill | `~/.claude/plugins/marketplaces/claude-plugins-official/plugins/example-plugin/skills/example-skill/SKILL.md` |
| frontend-design | `~/.claude/plugins/marketplaces/claude-plugins-official/plugins/frontend-design/skills/frontend-design/SKILL.md` |
| writing-hookify-rules | `~/.claude/plugins/marketplaces/claude-plugins-official/plugins/hookify/skills/writing-rules/SKILL.md` |
| math-olympiad | `~/.claude/plugins/marketplaces/claude-plugins-official/plugins/math-olympiad/skills/math-olympiad/SKILL.md` |
| siege | `~/.claude/plugins/marketplaces/claude-plugins-official/plugins/math-proof/skills/siege/SKILL.md` |
| solo | `~/.claude/plugins/marketplaces/claude-plugins-official/plugins/math-proof/skills/solo/SKILL.md` |
| build-mcp-app | `~/.claude/plugins/marketplaces/claude-plugins-official/plugins/mcp-server-dev/skills/build-mcp-app/SKILL.md` |
| build-mcp-server | `~/.claude/plugins/marketplaces/claude-plugins-official/plugins/mcp-server-dev/skills/build-mcp-server/SKILL.md` |
| build-mcpb | `~/.claude/plugins/marketplaces/claude-plugins-official/plugins/mcp-server-dev/skills/build-mcpb/SKILL.md` |
| playground | `~/.claude/plugins/marketplaces/claude-plugins-official/plugins/playground/skills/playground/SKILL.md` |
| agent-development | `~/.claude/plugins/marketplaces/claude-plugins-official/plugins/plugin-dev/skills/agent-development/SKILL.md` |
| command-development | `~/.claude/plugins/marketplaces/claude-plugins-official/plugins/plugin-dev/skills/command-development/SKILL.md` |
| hook-development | `~/.claude/plugins/marketplaces/claude-plugins-official/plugins/plugin-dev/skills/hook-development/SKILL.md` |
| mcp-integration | `~/.claude/plugins/marketplaces/claude-plugins-official/plugins/plugin-dev/skills/mcp-integration/SKILL.md` |
| plugin-settings | `~/.claude/plugins/marketplaces/claude-plugins-official/plugins/plugin-dev/skills/plugin-settings/SKILL.md` |
| plugin-structure | `~/.claude/plugins/marketplaces/claude-plugins-official/plugins/plugin-dev/skills/plugin-structure/SKILL.md` |
| skill-development | `~/.claude/plugins/marketplaces/claude-plugins-official/plugins/plugin-dev/skills/skill-development/SKILL.md` |
| project-artifact | `~/.claude/plugins/marketplaces/claude-plugins-official/plugins/project-artifact/skills/project-artifact/SKILL.md` |
| receipts | `~/.claude/plugins/marketplaces/claude-plugins-official/plugins/receipts/skills/receipts/SKILL.md` |
| session-report | `~/.claude/plugins/marketplaces/claude-plugins-official/plugins/session-report/skills/session-report/SKILL.md` |
| skill-creator | `~/.claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/SKILL.md` |
| drawio | `~/.claude/plugins/marketplaces/drawio/plugins/claude-code/skills/drawio/SKILL.md` |
| drawio | `~/.claude/plugins/marketplaces/drawio/plugins/codex/drawio/skills/drawio/SKILL.md` |
| drawio | `~/.claude/plugins/marketplaces/drawio/plugins/copilot/skills/drawio/SKILL.md` |
| yomiyasu | `~/.claude/plugins/marketplaces/yomiyasu/SKILL.md` |
| yomiyasu | `~/.claude/plugins/marketplaces/yomiyasu/skills/yomiyasu/SKILL.md` |

## 検証結果

- chezmoi v2.72.2 を使用。`tests/check_skills.py` と既存の `tests/check_alternate_git.py` は PASS。
- 一時 source / target / state を使用し、Windows / Linux の `.chezmoi.os` を切り替えて配置パスを検証した。UTF-8、本文の `{{ ... }}`、全256 byte 値を含むバイナリ、空ファイル、属性と紛らわしい名前、補助ファイルの階層を確認した。
- 原本だけの編集が両 target に反映されること、diff → dry-run → apply の手順、dry-run が target を変更しないこと、管理外 Skill と Claude 同期ファイルの保持を検証した。source 削除後も target は残る挙動を確認した。恒久サンプルは配置していない。
- 実際の `~/.agents/skills` / `~/.claude/skills` に対して、明示的な source と隔離した設定・state で限定 diff / dry-run を実行した。両方とも差分なし。共通原本は空なので実機への apply は不要であり、行っていない。
- 通常設定による検証と全体 diff / dry-run は `~/.config` / `~/.config/chezmoi` のアクセス拒否で実行できなかった。全体 apply は行っていない。対象外の設定ファイルは変更していない。
- 認識先は各ツールの公式資料と照合した。現在の Codex セッションでは既存の独立 yomiyasu が認識されている。Claude Code は2.1.294。共通 Skill を実機へ追加してのセッション確認は行っていない。
- OpenCode の実機 CLI は起動時に config ディレクトリを作成できず、EEXIST で失敗した。OpenCode v2 の互換読込先・優先順位は公式資料で確認したが、このマシンでの共通 Skill の認識は未実測。
- Ubuntu の実機 / 実行ビットは未検証。Windows 上で Linux 用 template data を使った検証は実機検証と区別する。WSL の一覧取得も失敗した。
- Git の既存ユーザー差分はなく、commit / push は行っていない。

残作業: 権限を解決した環境での全体 diff / dry-run、実際に採用する共通 Skill 追加後の各ツールの認識確認。

## 承認後の整理結果

2026-10-10、ユーザーの「消すのが妥当そうなものは消してください」により独立版 yomiyasu 1.0.4 の整理を実施した。上記一覧は整理前の調査記録。

削除直前に ZIP と現存する11ファイルの一覧・内容・SHA-256 の一致を再確認した。再帰削除は自動承認レビューに「blocked by policy」で拒否されたため、完全削除の代わりに、通常ディレクトリであることと全配下に reparse point がないことを確認して次の検索対象外ディレクトリへ退避した。

`~/.dotfiles/.codex/skill-backups/yomiyasu-1.0.4-retired-20261010/`

元の `~/.agents/skills/yomiyasu/` が存在しないことを確認した。Claude のプラグイン版1.0.6・設定・インストール台帳、Codex システム領域、Claude 同期領域の計281ファイルは整理前後の SHA-256 が一致した。ほかの Skill・プラグインは削除していない。独立版は Codex / OpenCode の新しいセッションから読み込まれなくなる。既存セッションに読み込み済みの内容は残る場合がある。

退避先と ZIP は Git 管理外。復元する場合は元の配置先が空であることを確認し、退避ディレクトリを `~/.agents/skills/yomiyasu/` に戻す。実機への chezmoi apply、commit / push は行っていない。

## Ponytail の共通管理への移行結果

2026-10-10、ユーザーの指示により Ponytail をプラグイン管理から dotfiles / chezmoi の共通 Skill 管理へ移行した。

- 5.1.0 の6つの Skill を `home/.skills/` に取り込み、各 Skill の LICENSE と ponytail-gain の benchmark 資料を保存した。出所とローカル変更は `docs/ponytail-source.md` を参照。
- Skill の限定 diff / dry-run を確認後、実機の `~/.agents/skills/` と `~/.claude/skills/` に chezmoi apply を実施。全ファイルが原本と一致し、その後の限定 diff は空だった。
- `codex plugin remove ponytail@ponytail --json` と `codex plugin marketplace remove ponytail --json` が成功。5.1.0 のプラグインキャッシュは削除された。残った3件の Ponytail hook 状態を除去し、Ponytail 以外の TOML 設定がバックアップと意味的に一致することを確認した。
- OpenCode の設定から Ponytail の登録だけを除去。DCP、モデル、権限、既存の compaction 設定は保持した。旧4.10.0 / 4.9.0のキャッシュはバックアップ配下へ退避した。
- dotfiles の Ponytail runtime config と `opencode-full` ラッパー、Bash alias を廃止。実機の Windows runtime config とラッパーもバックアップへ退避した。Ubuntu では旧配置ファイルと alias が残る場合があるため、各マシンで確認して整理する。
- Codex app-server の `skills/list` と OpenCode の `debug skill --pure` が、`~/.agents/skills/` の6つの Skill を認識した。モデル推論は実行していない。Claude Code は配置ファイルの一致まで確認し、セッション内の一覧確認は未実施。
- 実機の OpenCode は1.18.34で、v2への更新は行っていない。v2での認識は公式の互換配置仕様との照合であり、実測と区別する。
- 共通 Skill 展開テストと既存 Git 設定テストは PASS。Windows 上で Linux template data を用いた配置検証も PASS。Ubuntu 実機は未検証。
- 権限制約が解除された環境で全体 diff と `apply --dry-run --verbose --force` も実行した。管理外ファイルの削除はなく、残る差分は Claude / Codex / OpenCode / Git / PowerShell の既存設定差分だった。全体 apply は行わず、今回の Skill だけを適用した。
- バックアップ: `.codex/skill-backups/ponytail-migration-20261010/`。Codex のプラグイン ZIP、変更前の Codex / OpenCode 設定、退避キャッシュ・runtime ファイル、diff / dry-run 出力を保存した。Git 管理外であり、設定の実値を含むため公開しない。

既存セッションは読み込み済みのプラグイン指示が残る場合がある。新しいセッションで共通 Skill を使用する。プラグイン hooks・既定モード・自動更新の機能は移行対象に含めない。commit / push は行っていない。

## コミット・プッシュ後の yomiyasu 移行と OpenCode v2 更新

2026-10-10、共通管理と Ponytail の移行を `b162fce`（共通Skill管理の導入とPonytailの移行）として main にコミットし、origin/main へプッシュした。その後のユーザー指示により、次の作業を実施した。

- yomiyasu 1.0.6 を共通原本へ取り込み、両配置先に chezmoi apply。11ファイルの一致を確認。出所と範囲は `docs/yomiyasu-source.md` を参照。
- Claude の公式 CLI で `yomiyasu@yomiyasu` を user scope から uninstall（persistent data は保持）し、yomiyasu marketplace の user 登録を解除した。他の Claude 設定は変更前と意味的に一致することを確認した。dotfiles の marketplace 登録も除去した。
- 移行前の1.0.6プラグインは ZIP と元ファイルの一致を確認して保存した。古い独立版1.0.4の退避・ZIPも保持する。復元用以外に旧版を有効化しない。
- Scoop の versions bucket を追加し、opencode2 2.0.26 をダウンロード・ハッシュ検証後、opencode 1.18.34 を uninstall して opencode2 を install。コマンド名 opencode が v2.0.26 を返すことを確認。Scoop が展開用依存の7zip 26.04も導入した。
- v1バイナリと設定は `.codex/skill-backups/opencode-v2-20261010/` に保存した。認証情報・モデル・権限・DCPは維持し、v2未対応の compaction.prune のみ除去した。
- OpenCode に `skills: ["~/.agents/skills"]` を追加し、共通配置先を明示した。ローカルAPIの初期化前の skill.list は空で、セッション初期化と登録完了を待つ必要があった。確認用の一時セッションを作成・削除し、Ponytail6件とyomiyasuの7件が共通配置から認識されることを確認した。モデル推論は実行していない。確認用の localhost サーバーは停止済み。
- Codex skills/list でも7件を確認。Claude は両OSの設定テンプレートのJSON解析と配置ファイルの一致まで確認し、実際のセッション一覧確認は未実施。
- yomiyasu_lint.py と yomiyasu_diff.py は一時サンプルで実行し、JSON出力を確認した。共通Skill展開テストと既存Git設定テストは PASS。Ubuntu実機は未検証。
- 全体 diff / dry-run を再確認し、削除差分はなかった。残る対象外の既存設定差分は適用していない。限定 Skill diff は空。
