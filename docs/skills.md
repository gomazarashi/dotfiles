# 使用中の Agent Skills

Skill は dotfiles では管理せず、[`npx skills`](https://github.com/vercel-labs/skills) で各マシンに直接導入する。このファイルは使用中の Skill のメモ。

| 取得元 | Skill |
|---|---|
| [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | `ponytail`、`ponytail-review`、`ponytail-audit`、`ponytail-debt`、`ponytail-gain`、`ponytail-help` |
| [nanaism/yomiyasu](https://github.com/nanaism/yomiyasu) | `yomiyasu` |

## 導入

```sh
npx skills add <owner/repo> -g -a claude-code -a codex --copy -y --skill '*'
```

- 配置先は `~/.claude/skills/` (Claude Code) と `~/.agents/skills/` (Codex)。
- OpenCode v2 は `opencode.jsonc` の `skills: ["~/.agents/skills"]` で `~/.agents/skills` を参照する。`-a opencode` は付けない (二重に見える)。
- `--copy` は実ファイルで置く指定。Windows で symlink 権限を要しない。
- 取得元を足す前に `npx skills add <owner/repo> -l` で内容を確認する。

## 更新・確認・削除

```sh
npx skills update -g -y
npx skills ls -g
npx skills remove -g <name>
```

## 管理外

`~/.claude/skills/synced/` (アカウント同期)、`~/.codex/skills/.system/` (Codex 標準)、プラグイン同梱の Skill (drawio など)。
