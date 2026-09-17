def parse_command(text):
    text = text.lower().strip()

    if "move left" in text:
        return "MOVE_LEFT"

    if "move right" in text:
        return "MOVE_RIGHT"

    if "move up" in text:
        return "MOVE_UP"

    if "move down" in text:
        return "MOVE_DOWN"

    if "open gripper" in text:
        return "OPEN_GRIPPER"

    if "close gripper" in text:
        return "CLOSE_GRIPPER"

    if "go home" in text or "home" in text:
        return "HOME"

    if "stop" in text:
        return "STOP"

    return "UNKNOWN"
