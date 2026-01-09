# mimic-launchpad-gesture

`mimic-launchpad-gesture` is a Python application designed to detect pinch-in and pinch-out gestures from `libinput` debug events and execute configurable commands based on these gestures. It's particularly useful for mimicking macOS-like trackpad gestures, such as opening Launchpad, on Linux systems.

## Features

*   **Pinch Gesture Detection:** Accurately detects pinch-in and pinch-out gestures.
*   **Configurable Commands:** Executes user-defined shell commands upon gesture detection.
*   **Debug Mode:** Provides verbose output for debugging gesture recognition.
*   **Flexible Input:** Can read `libinput` events directly or from piped input (e.g., a file).

## Why this project?

I was inspired by tools like [fusuma](https://github.com/iberianpig/fusuma), which offer advanced touchpad gesture recognition for Linux. However, I found `fusuma` wasn't always easy to get working on my system, and honestly, all I really needed were reliable pinch-in and pinch-out gestures to give me that satisfying feeling of opening Launchpad. This project is my attempt to create a lightweight and focused alternative, aiming to provide a straightforward way to get those essential pinch gestures working with minimal efforts.

## Requirements

*   Python (managed by `uv`)
*   `uv` (for dependency management and running the application)
*   `libinput` (for gesture events)
*   `ydotool` (optional, used in the default `LAUNCHPAD_PINCH_COMMAND` to simulate key presses for actions like opening Launchpad)

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-repo/mimic-launchpad-gesture.git
    cd mimic-launchpad-gesture
    ```
2.  **Install dependencies:**
    ```bash
    uv sync
    ```

## Usage

The project uses a `Makefile` for convenient execution.

### Running the application

To run the application, you typically need access to `libinput` events, which often requires `sudo` privileges or being part of the `input` group.

*   **Run with automatic sudo detection:**
    ```bash
    make run
    ```
    This command will check if you are in the `input` group. If so, it runs without `sudo`; otherwise, it prompts for `sudo` to execute `libinput debug-events`.

*   **Run without sudo (if in `input` group):**
    ```bash
    make run-without-sudo
    ```

*   **Run with sudo (explicitly):**
    ```bash
    make run-with-sudo
    ```

### Debugging

Debug mode provides additional output to help understand gesture detection.

*   **Debug with automatic sudo detection:**
    ```bash
    make debug
    ```

*   **Debug without sudo:**
    ```bash
    make debug-without-sudo
    ```

*   **Debug with sudo:**
    ```bash
    make debug-with-sudo
    ```

### Static Samples

You can test the gesture detection logic using pre-recorded `libinput` event samples.

*   **Run sample 1:**
    ```bash
    make debug-static1
    ```
    (This sample contains a sequence of 2, 3, and 4-finger pinch-in/out gestures.)

*   **Run sample 2:**
    ```bash
    make debug-static2
    ```
    (This sample contains arbitrary random events.)

## Configuration

The behavior of the application can be configured using environment variables:

*   `LAUNCHPAD_PINCH_COMMAND`: The shell command to execute when a pinch gesture is detected.
    *   **Default:** `echo 'Pinch command not set. Set LAUNCHPAD_PINCH_COMMAND environment variable.'` (This provides feedback if no command is configured.)
    *   **Example:** `export LAUNCHPAD_PINCH_COMMAND="ydotool key 56:1 56:0"` (This example uses `ydotool` to simulate a key press. You can replace this with any command that suits your system's shortcuts, e.g., `xdotool key super+v` for a different shortcut.)
*   `LAUNCHPAD_NUM_FINGERS`: The number of fingers required for a pinch gesture to be recognized.
    *   **Default:** `4`

These can be set in your shell before running `make run` or directly within the `Makefile` if you prefer.

## Project Structure

*   `main.py`: The main entry point of the application.
*   `pinch_detector.py`: Contains the `PinchDetector` class responsible for processing `libinput` events and detecting gestures.
*   `input_events.py`: Handles reading and parsing `libinput` debug events.
*   `hook.py`: Manages the execution of commands based on detected gestures.
*   `env.py`: Utility functions for reading environment variables.
*   `Makefile`: Defines various commands for running and debugging the application.
*   `pyproject.toml`: Project metadata and dependencies.
*   `uv.lock`: Lock file for `uv` dependency management.
*   `samples/`: Directory containing sample `libinput` event outputs for testing.

## NixOS systemd Service

This project includes a NixOS module to run `mimic-launchpad-gesture` as a `systemd` service.

1.  **Import the module:**
    First, make this repository's module available to your NixOS configuration. If you have cloned this repository locally, you can import it in your `configuration.nix` like this:

    ```nix
    # configuration.nix
    { config, pkgs, ... }:

    {
      imports = [
        # ... other imports
        # Note: `/path/to/mimic-launchpad-gesture` is a placeholder.
        # The actual path depends on where you've cloned the repo or how you manage Nix packages.
        /path/to/mimic-launchpad-gesture/nix/mimic-launchpad-gesture-service.nix

      ];
      # ... rest of your configuration
    }
    If you are managing your NixOS configuration with a tool like Niv or Flakes, you would typically make this repository an input and then import the module from that input.

    For an example using Niv, see: https://github.com/ryuheechul/dotfiles/commit/9e6bc97c2eb3c790acd751eae01912dace8aab5e.
    ```

2.  **Enable and configure the service:**
    Within your `configuration.nix`, enable the service and configure its options:

    ```nix
    # configuration.nix
    { config, pkgs, ... }:

    {
      # ... (imports as above)

      mimic-launchpad-gesture-service = {
        enable = true;
        # Optional: Customize the command executed on pinch gesture
        # launchpadPinchCommand = pkgs.writeShellScriptBin "custom-pinch-command" ''
        #   ${pkgs.xdotool}/bin/xdotool key super+a
        # '';
        # Optional: Set the number of fingers required for the gesture
        # launchpadNumFingers = 3;
      };

      # The 'programs.ydotool.enable' option is automatically handled by this module
      # if you are using the default 'launchpadPinchCommand'. You only need to set
      # it explicitly if you are overriding the command and still wish to use ydotool
      # for other purposes, or if you wish to disable it.

      # ... rest of your configuration
    }
    ```
