{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  packages = [
    pkgs.python313
    pkgs.python313Packages.pip
    pkgs.python313Packages.pillow
    pkgs.exiftool
    pkgs.pyright
  ];
}
