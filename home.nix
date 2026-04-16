# home.nix
{ pkgs, ... }:

let
  user = builtins.getEnv "USER";
  homeDir = builtins.getEnv "HOME";
in
{
  home.username = user;
  home.homeDirectory = homeDir;

  home.stateVersion = "25.11";

  targets.genericLinux.enable = true;

  home.packages = with pkgs; [
    # 基本的なCLIツール
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

    # 画像編集とプレゼン
    inkscape
    pympress
    pinta
    gimp
    kdePackages.okular

    # terminal / multiplexer
    tmux
    ghostty
  ];

  home.sessionPath = [
    "$HOME/bin"
  ];

  home.sessionVariables = {
    EDITOR = "vim";
  };

  programs.git = {
    enable = true;
    settings = {
      core = {
        autocrlf = "input";
        safecrlf = true;
        attributesFile = "~/.config/git/attributes";
        excludesFile = "~/.config/git/ignore";
      };
    };
  };

  xdg.configFile."git/attributes".source = ./.config/git/attributes;
  xdg.configFile."git/ignore".source = ./.config/git/ignore;
  xdg.configFile."tmux/tmux.conf".source = ./.config/tmux/tmux.conf;
  xdg.configFile."ghostty/config".source = ./.config/ghostty/config;

  programs.home-manager.enable = true;
}
