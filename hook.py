import subprocess
from typing import Optional
from env import is_debug_mode, get_launchpad_pinch_command


def execute_hook_command(
    hook_commands: dict, pinch_direction_detected: Optional[str]
) -> bool:
    """Executes a given command and prints a debug message."""
    command_to_execute = None
    debug_message = None

    if pinch_direction_detected == "in":
        command_to_execute = hook_commands.get("pinch_in")
        debug_message = "Pinch in detected"
    elif pinch_direction_detected == "out":
        command_to_execute = hook_commands.get("pinch_out")
        debug_message = "Pinch out detected"

    if not command_to_execute:
        return False

    if debug_message:
        if is_debug_mode():
            print(f"DEBUG: {debug_message}, running command: {command_to_execute}")
    subprocess.run(command_to_execute, shell=True, check=True)
    return True


default_pinch_command = (
    "echo 'Pinch command not set. Set LAUNCHPAD_PINCH_COMMAND environment variable.'"
)
pinch_command = get_launchpad_pinch_command(default_pinch_command)

hooks = {"launchpad": {"pinch_in": pinch_command, "pinch_out": pinch_command}}
