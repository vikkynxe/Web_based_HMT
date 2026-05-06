import RPi.GPIO as GPIO
import time

# Pin definitions (BCM numbering)
PUL_PIN = 19   # STEP
DIR_PIN = 26   # DIRECTION
ENA_PIN = 22   # ENABLE (optional)


# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(PUL_PIN, GPIO.OUT)
GPIO.setup(DIR_PIN, GPIO.OUT)
GPIO.setup(ENA_PIN, GPIO.OUT)

# Enable driver (assuming active LOW enable)
GPIO.output(ENA_PIN, GPIO.LOW)

def step_motor(steps, direction, pulse_delay):
    GPIO.output(DIR_PIN, direction)
    for _ in range(steps):
        GPIO.output(PUL_PIN, GPIO.HIGH)
        time.sleep(pulse_delay)
        GPIO.output(PUL_PIN, GPIO.LOW)
        time.sleep(pulse_delay)

try:
    while True:
        print("Rotating clockwise")
        pulse_delay = float(input("pulse_delay"))
        step_motor(200, GPIO.LOW, pulse_delay)  # 200 steps forward
        time.sleep(1)


except KeyboardInterrupt:
    print("Stopping motor and cleaning up GPIO")
finally:
    GPIO.output(ENA_PIN, GPIO.HIGH)  # Disable driver
    GPIO.cleanup()
