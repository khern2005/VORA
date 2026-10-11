
from machine import Pin
from time import ticks_us, ticks_diff


class Motor:
    def __init__(self, step_pin, dir_pin, gear_ratio=1):
        self.step = Pin(step_pin, Pin.OUT, value=0)
        self.direction = Pin(dir_pin, Pin.OUT, value=0)

        # Motor configuration
        self.pulses_per_motor_rev = 800
        self.gear_ratio = gear_ratio

        self.pulses_per_degree = (
            self.pulses_per_motor_rev * self.gear_ratio
        ) / 360

        # Motor position tracking
        self.current_pulses = 0
        self.target_pulses = 0

        # Motor state
        self.stopped = False
        self.step_high = False
        self.active_direction = 1

        # Step timing
        self.half_period_us = 2500
        self.last_transition = ticks_us()

    def get_angle(self):
        return self.current_pulses / self.pulses_per_degree

    def is_moving(self):
        return self.step_high or (
            not self.stopped
            and self.current_pulses != self.target_pulses
        )

    def move_to(self, angle):
        if self.stopped:
            print("Movement blocked: STOP active")
            return

        self.target_pulses = round(
            angle * self.pulses_per_degree
        )

        print("Target angle:", round(angle, 2))

    def move_relative(self, degrees):
        if self.stopped:
            print("Movement blocked: STOP active")
            return

        pulse_change = round(
            degrees * self.pulses_per_degree
        )

        self.target_pulses += pulse_change

        print(
            "Target angle:",
            round(
                self.target_pulses / self.pulses_per_degree,
                2
            )
        )

    def stop(self):
        self.stopped = True
        self.target_pulses = self.current_pulses

        self.step.value(0)
        self.step_high = False

        print("Software STOP activated")

    def reset_stop(self):
        self.stopped = False
        self.last_transition = ticks_us()

        print("Software STOP reset")

    def update(self):
        if self.stopped:
            return

        now = ticks_us()

        if ticks_diff(
            now,
            self.last_transition
        ) < self.half_period_us:
            return

        # Complete the current step pulse
        if self.step_high:
            self.step.value(0)
            self.step_high = False
            self.last_transition = now

            self.current_pulses += self.active_direction

            if self.current_pulses == self.target_pulses:
                print(
                    "Move complete. Estimated angle:",
                    round(self.get_angle(), 2)
                )

            return

        # No movement required
        if self.current_pulses == self.target_pulses:
            return

        # Determine movement direction
        self.active_direction = (
            1
            if self.target_pulses > self.current_pulses
            else -1
        )

        self.direction.value(
            1 if self.active_direction == 1 else 0
        )

        # Begin the next step pulse
        self.step.value(1)
        self.step_high = True
        self.last_transition = now
