from command_parser import parse_command

print("VORA Voice Control")
print("Type 'stop' to exit.")

while True:
    text = input("Command: ")

    command = parse_command(text)
    print(f"Detected: {command}")

    if command == "STOP":
        break
