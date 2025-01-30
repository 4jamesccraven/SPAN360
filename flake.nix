{
  description = "";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    { flake-utils, nixpkgs, ... }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nixpkgs { inherit system; config.allowUnfree = true; };
      in
      {
        packages.mkdev = pkgs.callPackage ./package.nix { };

        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs.python312Packages; [
            pkgs.python312
            beautifulsoup4
            numpy
            requests
            stanza
            torch-bin
            tqdm

            pkgs.cudatoolkit
            pkgs.linuxPackages.nvidia_x11
          ];

          shellHook = ''
            clear
            export CUDA_PATH=${pkgs.cudatoolkit}
            export LD_LIBRARY_PATH=${pkgs.cudatoolkit}/lib:${pkgs.linuxPackages.nvidia_x11}/lib:$LD_LIBRARY_PATH
            export EXTRA_LDFLAGS="-L/lib -L${pkgs.linuxPackages.nvidia_x11}/lib"
            export EXTRA_CCFLAGS="-I/usr/include"
            zsh
            exit
          '';
        };
      }
    );
}
