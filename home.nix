{ pkgs, ... }:

{
  home.username = "user";
  home.homeDirectory = "/home/user";
  home.stateVersion = "25.11";

  home.packages = with pkgs; [
    # 基本的なCLIツール
    git
    curl
    wget
    jq
    fd
    ripgrep
    tree
    htop

    # エディタと文書作成
    vim
    neovim
    ffmpeg
    pandoc
    typst

    # 圧縮・展開とクリップボード
    unzip
    zip
    xsel

    # ネットワークと診断
    gh
    whois
    tcpdump
    traceroute
    iperf3
    nettools

    # ビルドツール
    gcc
    cmake
    gnumake
    pkg-config
    autoconf
    automake
    libtool
    bison
    flex

    # 言語系ツールチェーン
    python3
    pipx
    ruby
    rust-bin.stable.latest.default
    uv
    nodejs_24
    bun

    # ナレッジ管理と作図
    drawio
    obsidian

    # 画像編集とプレゼン
    inkscape
    pympress
    pinta
    gimp
    kdePackages.okular
  ];

  home.sessionPath = [
    "$HOME/bin"
  ];

  home.sessionVariables = {
    EDITOR = "vim";
  };

  programs.home-manager.enable = true;
}
