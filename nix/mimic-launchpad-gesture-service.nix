{
  config,
  lib,
  pkgs,
  self ? {
    src = ./..;
  },
  ...
}:

with lib;

let
  cfg = config.mimic-launchpad-gesture-service;
  pythonWithPackages = pkgs.python313.withPackages (p: [
    p.libevdev
    p.evdev
  ]);

  defaultPinchCommandPackage = pkgs.writeShellScriptBin "pinch-command" ''
    export PATH="${pkgs.ydotool}/bin:$PATH"
    export YDOTOOL_SOCKET=/run/ydotoold/socket
    exec ydotool key 56:1 56:0
  '';

  execStart = pkgs.writeShellScriptBin "exec-start" ''
    export PATH="${pkgs.libinput}/bin:$PATH"
    export PATH="${pkgs.coreutils}/bin:$PATH"
    stdbuf -oL libinput debug-events | ${pythonWithPackages}/bin/python ${self.src}/main.py
  '';

in
{
  options.mimic-launchpad-gesture-service = {
    enable = mkEnableOption "mimic-launchpad-gesture systemd service";

    user = mkOption {
      type = types.str;
      default = "mimic-launchpad-gesture";
      description = "User to run the mimic-launchpad-gesture service as.";
    };

    launchpadPinchCommand = mkOption {
      type = types.package;
      default = defaultPinchCommandPackage;
      description = "A package (derivation) that provides the command to execute when a pinch gesture is detected. The executable within this package should be named 'pinch-command'. The default provides 'ydotool key 56:1 56:0'.";
    };

    launchpadNumFingers = mkOption {
      type = types.ints.unsigned;
      default = 4;
      description = "The number of fingers required for a pinch gesture.";
    };
  };

  config =
    let
      useYdotool = cfg.launchpadPinchCommand == defaultPinchCommandPackage;
    in
    mkIf cfg.enable {
      systemd.services."mimic-launchpad-gesture" = {
        description = "Mimic Launchpad Gesture Service";
        wantedBy = [ "graphical.target" ];
        after = [ "display-manager.service" ];

        serviceConfig = {
          Type = "simple";
          User = cfg.user;
          WorkingDirectory = "/var/lib/${cfg.user}";
          Environment = [
            "LAUNCHPAD_PINCH_COMMAND=${cfg.launchpadPinchCommand}/bin/pinch-command"
            "LAUNCHPAD_NUM_FINGERS=${toString cfg.launchpadNumFingers}"
          ];

          PrivateDevices = false;
          DevicePolicy = "auto";

          ExecStart = "${execStart}/bin/exec-start";

          Restart = "on-failure";
          RestartSec = 5;
        };
      };

      users.users."${cfg.user}" = mkIf (cfg.user != "root") {
        isSystemUser = true;
        group = cfg.user;
        createHome = true;
        home = "/var/lib/${cfg.user}";
        extraGroups = [
          "input"
        ]
        ++ optionals useYdotool [
          "ydotool"
        ];
      };

      users.groups."${cfg.user}" = mkIf (cfg.user != "root") { };

      programs.ydotool.enable = mkDefault useYdotool;
    };
}
