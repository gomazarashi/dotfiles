# yomiyasu の出所

- upstream: https://github.com/nanaism/yomiyasu
- version: 1.0.6
- commit: `4075fc34fb0333ca1fe42d32cd619338f4a138ba` (Claude のインストール台帳より)
- 取り込み日: 2026-10-10
- license: MIT。upstream LICENSE を同梱。
- 取り込み元: Claude プラグインキャッシュ `yomiyasu/yomiyasu/1.0.6/` の SKILL.md、references、assets、本文が参照する2つの Python script。

本文と補助ファイルは改変していない。プラグイン設定・評価用コーパス生成スクリプトは共通 Skill に取り込まない。古い独立版1.0.4は復元用バックアップとしてのみ残す。

原本は `home/.skills/yomiyasu/`。Codex / Claude Code に chezmoi で実配置し、OpenCode v2 は共通配置を利用する。編集は原本で行い、更新時は upstream の version / commit と差分を確認する。

移行前の Claude プラグインと設定は Git 管理外の `.codex/skill-backups/yomiyasu-migration-20261010/` に保存した。プラグインZIPは元ファイルとの一致を確認済み。

移行・配置完了。CodexとOpenCode v2.0.26で認識を確認した。2つのPython scriptを実行しJSON出力を確認。Claudeは実配置の一致まで確認し、セッション内の確認とUbuntu実機確認は未実施。
