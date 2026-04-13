# dotfiles

個人用の dotfiles リポジトリです。現在は主に次の設定を管理しています。

- `Nix` / `Home Manager` による開発環境
- `Codex` の動作設定
- `Obsidian` Vault の設定
- `git` / `nix` のユーザー設定ファイル

## ディレクトリ構成

### Nix / Home Manager

- `flake.nix`: flake のエントリポイント。`nixpkgs` / `home-manager` / `rust-overlay` を定義
- `flake.lock`: flake input のバージョン固定
- `home.nix`: Home Manager の本体設定

### Codex

- `.codex/config.toml`: モデル、reasoning effort、sandbox、ネットワーク利用などの設定
- `.codex/AGENTS.md`: Codex 向けの作業ルール

### Git / Nix

- `.config/git/attributes`: Git attributes
- `.config/git/ignore`: グローバル ignore
- `.config/nix/nix.conf`: `nix-command` / `flakes` の有効化

### Obsidian

- `.obsidian/app.json`: エディタ挙動
- `.obsidian/appearance.json`: 表示設定
- `.obsidian/core-plugins.json`: コアプラグイン設定
- `.obsidian/community-plugins.json`: Community Plugin 一覧
- `.obsidian/templates.json`: Templates 設定
- `.obsidian/plugins/`: Community Plugin ごとの設定

現在の Community Plugin:

- `editor-width-slider`
- `templater-obsidian`
- `obsidian-git`

## Home Manager 設定

現在の flake では `homeConfigurations."main"` をエクスポートしています。

`home.nix` ではユーザー名とホームディレクトリを固定値ではなく環境変数から取得します。

- `home.username = builtins.getEnv "USER";`
- `home.homeDirectory = builtins.getEnv "HOME";`

そのため、公開用のプレースホルダーを書き換える運用ではなく、実行環境の `USER` / `HOME` をそのまま使う構成です。
この値を flake 評価時に参照するため、適用時は `--impure` を前提としています。

主に次のツール群を Home Manager で導入しています。

- CLI ツール: `curl`, `wget`, `jq`, `fd`, `ripgrep`, `tree`, `htop`
- エディタ・文書系: `vim`, `neovim`, `pandoc`, `typst`, `ffmpeg`
- 開発ツール: `gcc`, `cmake`, `gnumake`, `pkg-config`, `autoconf`, `automake`, `libtool`, `bison`, `flex`
- 言語環境: `python3`, `pipx`, `ruby`, `rust-bin.stable.latest.default`, `uv`, `nodejs_24`, `bun`
- その他: `gh`, `drawio`, `inkscape`, `gimp`, `okular` など

また、以下も Home Manager で設定しています。

- `$HOME/bin` を `PATH` に追加
- `EDITOR=vim`
- Git の `attributesFile` / `excludesFile`

## 適用方法

事前に `Nix` で flakes を使える状態にしておきます。手元では `.config/nix/nix.conf` に次を置いています。

```conf
experimental-features = nix-command flakes
```

`home.nix` が `builtins.getEnv` を使うため、評価は impure モードで行います。

適用コマンド:

```bash
home-manager switch --impure --flake .#main
```

`home-manager` をまだ入れていない環境では、たとえば次のように実行できます。

```bash
nix run home-manager/release-25.11 -- switch --impure --flake .#main
```
