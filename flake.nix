{
  description = "Development environment with pixi";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        lib = nixpkgs.lib;
      in
      {
        devShells.default = pkgs.mkShell {
          packages = with pkgs; [
            pixi
          ];

          # export SHELL=${lib.getExe pkgs.bash}
          shellHook = ''
            export PS1="(nix-dev) \u@\h:\w\$ "
            echo "Development environment with pixi is ready!"
            echo "Run 'pixi shell --environment development' to start the pixi shell for development."
          '';
        };
      });
}
