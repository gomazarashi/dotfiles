# Ponytail の出所

- upstream: https://github.com/DietrichGebert/ponytail
- version: 5.1.0
- 取り込み日: 2026-10-10
- 取り込み元: ローカル Codex プラグインキャッシュ `ponytail/ponytail/5.1.0/skills/`。upstream commit は未照合。
- license: MIT。各 Skill に upstream LICENSE を同梱。
- 補助資料: ponytail-gain が参照する `benchmarks/results/2026-10-07-agentic.md` を同 Skill の `references/` に同梱。

ローカル変更は ponytail-gain の参照パス変更と、ponytail-help の起動・更新手順を共通 Skill の運用へ変更したもの。残り4つの SKILL.md はそのまま取り込んだ。hooks・プラグイン実装・他ツール用コピーは取り込まない。

プラグイン管理からの移行に伴い、Codex の Ponytail プラグインと marketplace、OpenCode の Ponytail plugin 設定、dotfiles の runtime 設定・起動ラッパーを整理する。バックアップは Git 管理外の `.codex/skill-backups/ponytail-migration-20261010/` に保存する。

移行は完了済み。Codex / OpenCode の共通 Skill 認識を実測した。OpenCode 実機は1.18.34であり、v2の実機確認とUbuntu実機確認、Claudeのセッション内確認は未実施。

その後、OpenCodeをv2.0.26に更新し、6つのPonytail Skillとyomiyasuの共通配置からの認識を実測した。参照先はopencode.jsoncのskills配列で明示する。
