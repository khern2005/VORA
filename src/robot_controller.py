VALID_COMMANDS = {
    "MOVE_LEFT",
    "MOVE_RIGHT",
    "MOVE_UP",
    "MOVE_DOWN",
    "OPEN_GRIPPER",
    "CLOSE_GRIPPER",
    "HOME",
    "STOP",
}


def execute_command(command):
    """Execute a validated VORA robot command."""

    if command not in VALID_COMMANDS:
        print(f"Cannot execute unknown command: {command}")
        return False

    if command == "STOP":
        print("Emergency stop requested.")
        return True

    # Physical robot movement will be added here later.
    print(f"Executing: {command}")
    return True