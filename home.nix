{ pkgs, ... }:

{
  home.username = "user";
  home.homeDirectory = "/home/user";
  home.stateVersion = "25.11";

  home.packages = with pkgs; [
    git
    curl
    wget
    jq
    tree
    htop
    ripgrep
    fd
    unzip
    zip

    vim
    neovim
    gh
    ffmpeg
    pandoc
    xsel
    whois
    tcpdump
    traceroute
    iperf3
    nettools

    gcc
    cmake
    gnumake
    pkg-config
    autoconf
    automake
    libtool
    bison
    flex

    python3
    pipx
    ruby
    cargo
    rustc
    rustfmt
    uv
    nodejs_24
    bun
    typst

    drawio
    obsidian
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
