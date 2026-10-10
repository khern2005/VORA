
import re

DEFAULT_ANGLE = 15
DEFAULT_SPEED = 30

ONES = {
    "zero": 0, "one": 1, "two": 2, "three": 3,
    "four": 4, "five": 5, "six": 6, "seven": 7,
    "eight": 8, "nine": 9, "ten": 10,
    "eleven": 11, "twelve": 12, "thirteen": 13,
    "fourteen": 14, "fifteen": 15, "sixteen": 16,
    "seventeen": 17, "eighteen": 18, "nineteen": 19
}

TENS = {
    "twenty": 20, "thirty": 30, "forty": 40,
    "fifty": 50, "sixty": 60, "seventy": 70,
    "eighty": 80, "ninety": 90
}

NUMBER_WORDS = set(ONES) | set(TENS) | {"hundred", "and"}

NUMBER_PATTERN = (
    r"(?:\d+|"
    r"(?:(?:" + "|".join(ONES) + r")\s+)?hundred"
    r"(?:\s+and)?"
    r"(?:\s+(?:" + "|".join(TENS) + r")"
    r"(?:\s+(?:" + "|".join(ONES) + r"))?"
    r"|\s+(?:" + "|".join(ONES) + r"))?"
    r"|(?:" + "|".join(TENS) + r")"
    r"(?:\s+(?:" + "|".join(ONES) + r"))?"
    r"|(?:" + "|".join(ONES) + r"))"
)


def spoken_number(value):
    value = value.strip().replace("-", " ")

    if value.isdigit():
        return int(value)

    words = value.split()
    total = 0
    current = 0

    for word in words:
        if word == "and":
            continue
        elif word in ONES:
            current += ONES[word]
        elif word in TENS:
            current += TENS[word]
        elif word == "hundred":
            current = max(current, 1) * 100
        else:
            return None

    return total + current


def unknown():
    return {
        "command": "UNKNOWN",
        "angle": None,
        "speed": None
    }


def parse_command(text):
    text = text.lower().strip().replace("-", " ")

    # Reject negated commands.
    if re.search(r"\b(?:don't|dont|do not|never|no)\b", text):
        return unknown()

    # Recognize STOP.
    if re.fullmatch(r"(?:stop|stop now|emergency stop)", text):
        return {
            "command": "STOP",
            "angle": None,
            "speed": None
        }

    commands = {
        "move left": "MOVE_LEFT",
        "move right": "MOVE_RIGHT",
        "move up": "MOVE_UP",
        "move down": "MOVE_DOWN",
        "open gripper": "OPEN_GRIPPER",
        "close gripper": "CLOSE_GRIPPER",
        "go home": "HOME",
        "home": "HOME"
    }

    command = "UNKNOWN"

    for phrase, action in commands.items():
        if re.search(r"\b" + re.escape(phrase) + r"\b", text):
            command = action
            break

    if command == "UNKNOWN":
        return unknown()

    # These actions don't need angles or speeds.
    if command in {"HOME", "OPEN_GRIPPER", "CLOSE_GRIPPER"}:
        return {
            "command": command,
            "angle": None,
            "speed": None
        }

    # Match complete numeric expressions.
    angle_match = re.search(
        rf"\b({NUMBER_PATTERN})\s*(?:degrees?|°)\b",
        text
    )

    speed_match = re.search(
        rf"\b({NUMBER_PATTERN})\s*(?:percent|%)\s*(?:speed)?\b"
        rf"|\bspeed\s*(?:of\s*)?({NUMBER_PATTERN})\b",
        text
    )

    angle = DEFAULT_ANGLE
    speed = DEFAULT_SPEED

    if angle_match:
        angle = spoken_number(angle_match.group(1))

    if speed_match:
        speed = spoken_number(
            speed_match.group(1) or speed_match.group(2)
        )

    # Reject unsupported numeric phrases.
    # This also catches phrases like "two hundred degrees"
    # if the regex matched only "hundred degrees".
    for match in (angle_match, speed_match):
        if match:
            prefix = text[:match.start()].split()
            if prefix and prefix[-1] in NUMBER_WORDS:
                return unknown()

    # Preliminary software limits.
    if angle is None or speed is None:
        return unknown()

    if not (1 <= angle <= 180):
        return unknown()

    if not (1 <= speed <= 100):
        return unknown()

    return {
        "command": command,
        "angle": angle,
        "speed": speed
    }
