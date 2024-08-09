{
  description = "A lightweight API designed to simulate bank credit scenarios for real estate financing";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        devShell = pkgs.mkShell {
          nativeBuildInputs = with pkgs;
            let
              pythonWithPackages = python3.withPackages (p:
                with p; [
                  flask
                  pydantic
                ]
              );
            in
            [
              pythonWithPackages
              gnumake
            ];
        };
      }
    );
}
