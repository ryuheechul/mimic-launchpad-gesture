from typing import Optional
from input_events import (
    feed_input_events,
    parse_libinput_event,
    LibinputEvent,
    GESTURE_PINCH_BEGIN,
    GESTURE_PINCH_UPDATE,
    GESTURE_PINCH_END,
)
from hook import execute_hook_command

# The command to execute when a "pinch in" is detected.
# PINCH_IN_COMMAND = "echo 'Pinch in detected'"


# We need to keep track of the previous zoom value to detect the direction of the pinch.
# previous_zoom = 1.0
# command_executed_for_current_gesture = False


class PinchDetector:
    def __init__(self, num_fingers: int, hook_commands: dict):
        self.previous_zoom = 1.0
        self.command_executed_for_current_gesture = False
        self.pinch_in_occurred_during_updates = False
        self.num_fingers_for_pinch = num_fingers
        self.hook_commands = hook_commands
        self.pinch_direction_detected: Optional[str] = None

    def _handle_pinch_update_event(self, event: LibinputEvent):
        """Handles GESTURE_PINCH_UPDATE events."""
        if event.zoom is None:
            return

        zoom = event.zoom
        if zoom < self.previous_zoom:
            self.pinch_in_occurred_during_updates = True
            self.pinch_direction_detected = "in"
        elif zoom > self.previous_zoom:
            self.pinch_direction_detected = "out"
        self.previous_zoom = zoom

    def _handle_pinch_begin_event(self):
        """Handles GESTURE_PINCH_BEGIN events."""
        self.command_executed_for_current_gesture = False
        self.pinch_in_occurred_during_updates = False
        self.pinch_direction_detected = None

    def _handle_pinch_end_event(self):
        """Handles GESTURE_PINCH_END events."""
        if self.command_executed_for_current_gesture:
            return

        command_executed = execute_hook_command(
            self.hook_commands, self.pinch_direction_detected
        )
        if command_executed:
            self.command_executed_for_current_gesture = True

    def _process_gesture_line(self, line: str):
        """Processes a single line from libinput debug events for gesture recognition."""
        from env import is_debug_mode

        if is_debug_mode():
            print(f"DEBUG: Raw line: {line}")
        event = parse_libinput_event(line)

        if event is None or "GESTURE_PINCH" not in event.event_type:
            return

        # Check num_fingers only if it's a BEGIN or UPDATE event and num_fingers is available
        if (
            event.num_fingers is not None
            and event.num_fingers != self.num_fingers_for_pinch
        ):
            return

        if event.event_type == GESTURE_PINCH_UPDATE:
            self._handle_pinch_update_event(event)
        elif event.event_type == GESTURE_PINCH_BEGIN:
            self._handle_pinch_begin_event()
        elif event.event_type == GESTURE_PINCH_END:
            self._handle_pinch_end_event()

    def run(self):
        for line in feed_input_events():
            if "GESTURE_PINCH" in line:
                self._process_gesture_line(line)
