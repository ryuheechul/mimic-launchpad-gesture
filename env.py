import os


def is_debug_mode() -> bool:
    return os.environ.get("DEBUG_MODE") is not None


def get_launchpad_pinch_command(default_command: str) -> str:
    return os.environ.get("LAUNCHPAD_PINCH_COMMAND", default_command)


def get_num_fingers_for_pinch() -> int:
    try:
        return int(os.environ.get("LAUNCHPAD_NUM_FINGERS", "4"))
    except ValueError:
        return 4
