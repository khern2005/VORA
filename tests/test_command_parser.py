from src.command_parser import parse_command


def test_valid_commands():
    assert parse_command("move left") == "MOVE_LEFT"
    assert parse_command("move right") == "MOVE_RIGHT"
    assert parse_command("move up") == "MOVE_UP"
    assert parse_command("move down") == "MOVE_DOWN"
    assert parse_command("open gripper") == "OPEN_GRIPPER"
    assert parse_command("close gripper") == "CLOSE_GRIPPER"
    assert parse_command("go home") == "HOME"
    assert parse_command("stop") == "STOP"


def test_negated_commands():
    assert parse_command("don't move left") == "UNKNOWN"
    assert parse_command("do not move right") == "UNKNOWN"
    assert parse_command("don't open gripper") == "UNKNOWN"
    assert parse_command("never move down") == "UNKNOWN"


def test_unknown_commands():
    assert parse_command("i like pizza") == "UNKNOWN"
    assert parse_command("hello vora") == "UNKNOWN"
    assert parse_command("dance") == "UNKNOWN"