def parse_command(text):
    text = text.lower().strip()

    if "left" in text:
        return "MOVE_LEFT"
    elif "right" in text:
        return "MOVE_RIGHT"
    elif "up" in text:
        return "MOVE_UP"
    elif "down" in text:
        return "MOVE_DOWN"
    elif "stop" in text:
        return "STOP"
    else:
        return "UNKNOWN"
