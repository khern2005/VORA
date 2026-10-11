
import sys
import select
from time import sleep_ms

poller = select.poll()
poller.register(sys.stdin, select.POLLIN)

print("VORA Pico 2 ready")
print("Waiting for commands...")

while True:
    events = poller.poll(0)

    if events:
        command = sys.stdin.readline().strip()

        if command:
            print("Received:", command)

            if command == "MOVE_LEFT":
                print("Base would move left")

            elif command == "MOVE_RIGHT":
                print("Base would move right")

            elif command == "STOP":
                print("Stop command received")

            else:
                print("Unknown command")

    sleep_ms(20)
