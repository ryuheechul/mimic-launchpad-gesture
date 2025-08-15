# exports here to show these things are configurable
# The command to execute when a pinch gesture is detected.
# By default, this uses `ydotool` to simulate a key press (Alt key, which is 56:1 for press and 56:0 for release) which
# is configured on my system to open Launchpad. You can change this to any
# command that suits your system's shortcuts or desired action.
export LAUNCHPAD_PINCH_COMMAND ?= ydotool key 56:1 56:0
export LAUNCHPAD_NUM_FINGERS ?= 4

LIBINPUT_CMD = stdbuf -oL libinput debug-events
TIMEOUT_CMD = timeout 10

.PHONY: debug
debug:
	groups $(whoami) | grep -q input && \
		$(MAKE) debug-without-sudo || \
		$(MAKE) debug-with-sudo

.PHONY: debug-without-sudo
debug-without-sudo:
	$(TIMEOUT_CMD) $(LIBINPUT_CMD) | DEBUG_MODE=1 uv run main.py

.PHONY: debug-with-sudo
debug-with-sudo:
	sudo $(TIMEOUT_CMD) $(LIBINPUT_CMD) | DEBUG_MODE=1 uv run main.py

.PHONY: debug-static1
debug-static1:
	cat samples/1/stdout.txt | uv run main.py

.PHONY: debug-static2
debug-static2:
	cat samples/2/stdout.txt | uv run main.py

.PHONY: run-without-sudo
run-without-sudo:
	uv run main.py

.PHONY: run-with-sudo
run-with-sudo:
	sudo $(LIBINPUT_CMD) | uv run main.py

.PHONY: run
run:
	groups $(whoami) | grep -q input && \
		$(MAKE) run-without-sudo || \
		$(MAKE) run-with-sudo
