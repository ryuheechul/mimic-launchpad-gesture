import subprocess
import re
import sys
from typing import Iterator, Optional
from dataclasses import dataclass

GESTURE_PINCH_BEGIN = "GESTURE_PINCH_BEGIN"
GESTURE_PINCH_UPDATE = "GESTURE_PINCH_UPDATE"
GESTURE_PINCH_END = "GESTURE_PINCH_END"


@dataclass
class LibinputEvent:
    event_type: str
    num_fingers: Optional[int] = None
    zoom: Optional[float] = None


def feed_input_events() -> Iterator[str]:
    """
    Runs `stdbuf -oL libinput debug-events` and yields its output line by line.
    If stdin has input, it reads from stdin instead.
    """
    if not sys.stdin.isatty():
        # Read from stdin if input is piped or redirected
        for line in sys.stdin:
            yield line
    else:
        # Fallback to existing logic if stdin is a TTY

        # Run libinput debug-events directly
        cmd_list = ["stdbuf", "-oL", "libinput", "debug-events"]

        process = subprocess.Popen(
            cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        if process.stdout:
            for line in process.stdout:
                yield line


def parse_libinput_event(line: str) -> Optional[LibinputEvent]:
    """Parses a single line from libinput debug events and returns a LibinputEvent object."""
    parts = line.strip().split()

    if len(parts) < 2 or "GESTURE_PINCH" not in line:
        return None

    event_type = parts[1]
    num_fingers: Optional[int] = None
    zoom: Optional[float] = None

    try:
        if event_type == GESTURE_PINCH_BEGIN:
            if len(parts) > 3:
                num_fingers = int(parts[3])
        elif event_type == GESTURE_PINCH_UPDATE:
            if len(parts) > 4:
                num_fingers = int(parts[4])
            match = re.search(r"unaccelerated\)\s+([\d.]+)", line)
            if match:
                zoom = float(match.group(1))
    except ValueError:
        # Ignore lines where parsing fails (e.g., num_fingers not an int, zoom not a float)
        return None

    return LibinputEvent(event_type=event_type, num_fingers=num_fingers, zoom=zoom)
