# 使用中の Agent Skills

Skill は dotfiles では管理せず、[`npx skills`](https://github.com/vercel-labs/skills) で各マシンに直接導入する。

- [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail): `ponytail`、`ponytail-review`、`ponytail-audit`、`ponytail-debt`、`ponytail-gain`、`ponytail-help`
- [nanaism/yomiyasu](https://github.com/nanaism/yomiyasu): `yomiyasu`

## 導入・更新・削除

```sh
# 導入前の内容確認
npx skills add <owner/repo> -l

# 導入
npx skills add <owner/repo> -g -a claude-code -a codex -y --skill '*'

# 更新・一覧・削除
npx skills update -g -y
npx skills ls -g
npx skills remove -g <name>
```

- **配置と共有**: 実体は `~/.agents/skills/` (Codex が参照) に 1 つだけ置かれ、`~/.claude/skills/` (Claude Code) には Junction が作られる。そのため両者は常に同じ版を参照する (`--copy` を付けるとコピーになり、更新時に Claude Code 側が古いまま残ることがあるため使わない)。
- **OpenCode v2 の自動検出と優先順位**: OpenCode v2 は両方の配置先を[自動検出](https://opencode.ai/v2/docs/skills)し、同じ ID は `~/.agents/skills/` を優先して 1 つにまとめる (`skills` 配列や `-a opencode` は不要)。ただし、`~/.config/opencode/skills/` やプロジェクトの `.opencode/skills/` に同じ ID がある場合はそちらが優先される。
- **二重導入の回避**: `npx skills` で導入する Skill は、Claude Code のプラグインとしては導入しない (両方から導入すると別名で二重に表示され、版もずれる)。

## 管理外の Skill

`~/.claude/skills/synced/` (アカウント同期)、`~/.codex/skills/.system/` (Codex 標準)、プラグイン同梱の Skill (drawio など)。
