# default.nix
{ pkgs ? import <nixpkgs> {}
, config ? {}
, lib ? pkgs.lib
, ... } @ args:

(import ./nix/mimic-launchpad-gesture-service.nix args)
