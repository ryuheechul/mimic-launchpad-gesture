from hook import hooks
from pinch_detector import PinchDetector
from env import get_num_fingers_for_pinch


def main():
    print("Hello from mimic-launchpad-gesture!")
    num_fingers = get_num_fingers_for_pinch()
    detector = PinchDetector(num_fingers=num_fingers, hook_commands=hooks["launchpad"])
    detector.run()


if __name__ == "__main__":
    main()
