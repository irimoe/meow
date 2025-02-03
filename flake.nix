{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
  let
    pkgs = nixpkgs.packages."x86_64-linux";
  in
  {
    devShells.x86_64-linux.default = pkgs.mkShell { #default is now a devshell
      name = "dev";
      packages = with pkgs; [
        
      ];
    };
    default = self.devShells.x86_64-linux.default; #changed from package to devshell
  };
}