
import sys
import select
from time import sleep_ms
from motor_controller import Motor

# Initialize motors
# J1: Base motor, 20:1 gearbox
base = Motor(step_pin=0, dir_pin=1, gear_ratio=20)

# J2: Shoulder motor, 1:1 gearbox
shoulder = Motor(step_pin=2, dir_pin=3, gear_ratio=1)

# USB serial command input
poller = select.poll()
poller.register(sys.stdin, select.POLLIN)

# Movement amount per command (degrees)
MOVE_DEGREES = 5

print("VORA Pico 2 ready")
print("Base (J1) and Shoulder (J2) initialized")
print("Waiting for commands...")


def print_status():
    print("--- VORA Motor Status ---")

    print("Base (J1):")
    print("  Estimated angle:", round(base.get_angle(), 2))
    print("  Moving:", base.is_moving())
    print("  Stopped:", base.stopped)

    print("Shoulder (J2):")
    print("  Estimated angle:", round(shoulder.get_angle(), 2))
    print("  Moving:", shoulder.is_moving())
    print("  Stopped:", shoulder.stopped)


while True:
    # Check for incoming USB serial commands
    if poller.poll(0):
        command = sys.stdin.readline().strip().upper()

        # Base motor commands
        if command == "MOVE_LEFT":
            base.move_relative(MOVE_DEGREES)

        elif command == "MOVE_RIGHT":
            base.move_relative(-MOVE_DEGREES)

        # Shoulder motor commands
        elif command == "SHOULDER_UP":
            shoulder.move_relative(MOVE_DEGREES)

        elif command == "SHOULDER_DOWN":
            shoulder.move_relative(-MOVE_DEGREES)

        # Stop both motors
        elif command == "STOP":
            base.stop()
            shoulder.stop()
            print("All motors stopped")

        # Reset software stop for both motors
        elif command == "RESET_STOP":
            base.reset_stop()
            shoulder.reset_stop()
            print("Software STOP reset for both motors")

        # Display motor status
        elif command == "STATUS":
            print_status()

        elif command:
            print("Unknown command:", command)

    # Update both motors independently
    base.update()
    shoulder.update()

    sleep_ms(1)
