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
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs.python312Packages; [
            pkgs.python312
            beautifulsoup4
            tqdm
          ];
        };
      }
    );
}
