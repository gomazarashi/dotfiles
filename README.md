# README.md

# dotfiles

個人用の設定ファイルを管理するリポジトリです。現在は主に以下を管理しています。

- `Home Manager` ベースの Nix 設定
- `Codex` の設定
- `Obsidian` Vault 設定

## ディレクトリ構成

### Nix / Home Manager

- `flake.nix`: Home Manager の flake エントリポイント
- `home.nix`: Home Manager の本体設定
- `flake.lock`: flake input のバージョン固定

### Codex

- `.codex/config.toml`: Codex のモデル、サンドボックス、ネットワーク設定

### Obsidian

- `.obsidian/app.json`: エディタ挙動（リンク更新、添付先など）
- `.obsidian/appearance.json`: 表示設定（フォントサイズなど）
- `.obsidian/core-plugins.json`: コアプラグイン有効/無効設定
- `.obsidian/community-plugins.json`: Community Plugin 一覧
- `.obsidian/templates.json`: Templates フォルダ設定
- `.obsidian/plugins/`: Community Plugins ごとの設定ディレクトリ

## Nix 設定について

このリポジトリの Nix 設定は、公開用にプレースホルダーを含む最小構成として管理しています。

現在のプレースホルダー値:

- `flake.nix`
  - `homeConfigurations."user"`
- `home.nix`
  - `home.username = "user";`
  - `home.homeDirectory = "/home/user";`

利用前に、自分の環境に合わせてこれらを書き換えてください。

## 適用方法

Nix flakes が有効な環境で、プレースホルダーを書き換えた後に次を実行します。

```bash
home-manager switch --flake .#your-username
```
