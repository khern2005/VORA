
import pytest
from src.command_parser import parse_command


@pytest.mark.parametrize("phrase,command", [
    ("move left", "MOVE_LEFT"),
    ("move right", "MOVE_RIGHT"),
    ("move up", "MOVE_UP"),
    ("move down", "MOVE_DOWN"),
    ("open gripper", "OPEN_GRIPPER"),
    ("close gripper", "CLOSE_GRIPPER"),
    ("go home", "HOME"),
    ("stop", "STOP"),
])
def test_valid_commands(phrase, command):
    result = parse_command(phrase)
    assert result["command"] == command


@pytest.mark.parametrize("phrase,angle,speed", [
    ("move left", 15, 30),
    ("move right ninety degrees", 90, 30),
    ("move up at twenty percent speed", 15, 20),
    ("move down sixty degrees at fifty percent speed", 60, 50),
    ("move left forty five degrees at thirty percent speed", 45, 30),
])
def test_angle_and_speed(phrase, angle, speed):
    result = parse_command(phrase)
    assert result["angle"] == angle
    assert result["speed"] == speed


@pytest.mark.parametrize("phrase", [
    "don't move left",
    "do not move up",
    "never open gripper",
    "move left two hundred degrees",
    "move right zero degrees",
    "move up at zero percent speed",
    "move down at one hundred fifty percent speed",
])
def test_invalid_commands(phrase):
    assert parse_command(phrase)["command"] == "UNKNOWN"


@pytest.mark.parametrize("phrase", [
    "hello",
    "random words",
    "turn around",
])
def test_unknown_commands(phrase):
    assert parse_command(phrase)["command"] == "UNKNOWN"
