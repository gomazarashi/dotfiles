# 使用中の Agent Skills

Skill は dotfiles では管理せず、[`npx skills`](https://github.com/vercel-labs/skills) で各マシンに直接導入する。このファイルは使用中の Skill のメモ。

- [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail): `ponytail`、`ponytail-review`、`ponytail-audit`、`ponytail-debt`、`ponytail-gain`、`ponytail-help`
- [nanaism/yomiyasu](https://github.com/nanaism/yomiyasu): `yomiyasu`

## 導入

```sh
npx skills add <owner/repo> -g -a claude-code -a codex -y --skill '*'
```

- 実体は `~/.agents/skills/` (Codex が参照) に一つだけ置かれ、`~/.claude/skills/` (Claude Code) には Junction が作られる。そのため、Claude Code と Codex は常に同じ版になる。
- OpenCode v2 は両方の配置先を[自動検出](https://opencode.ai/v2/docs/skills)し、同じ ID は `~/.agents/skills/` を優先して一つにまとめる。ただし `~/.config/opencode/skills/` とプロジェクトの `.opencode/skills/` に同じ ID があれば、そちらが優先される。`skills` 配列と `-a opencode` は不要。
- `--copy` は付けない。コピーにすると、更新時に Claude Code 側だけ古いままになることがある。
- 取得元を追加する前に `npx skills add <owner/repo> -l` で内容を確認する。

## 更新・確認・削除

```sh
npx skills update -g -y
npx skills ls -g
npx skills remove -g <name>
```

## 管理外

`~/.claude/skills/synced/` (アカウント同期)、`~/.codex/skills/.system/` (Codex 標準)、プラグイン同梱の Skill (drawio など)。

`npx skills` で導入する Skill は、Claude Code のプラグインとしては導入しない。両方から導入すると別名で二重に表示され、版もずれる。
