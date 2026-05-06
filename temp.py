import RPi.GPIO as GPIO
import time

# =========================
# GPIO INITIALIZATION
# =========================

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Stepper pin definitions
AXES = {
    "x": {"pul": 6,  "dir": 5,  "ena": 24},
    "y": {"pul": 16, "dir": 20, "ena": 21},
    "z": {"pul": 25, "dir": 8,  "ena": 7},
    "a": {"pul": 19, "dir": 26, "ena": 13},
}

# Setup stepper GPIO
for axis in AXES.values():
    GPIO.setup(axis["pul"], GPIO.OUT)
    GPIO.setup(axis["dir"], GPIO.OUT)
    GPIO.setup(axis["ena"], GPIO.OUT)
    GPIO.output(axis["ena"], GPIO.LOW)   # enable driver

# =========================
# STEPPER CONFIG
# =========================

STEP_ANGLE = 0.9
STEP_DELAY = 0.001

# =========================
# ROTARY ENCODER SETUP
# =========================

ENCODER_CLK = 22
ENCODER_DT  = 27
ENCODER_SW  = 17

GPIO.setup(ENCODER_CLK, GPIO.IN)
GPIO.setup(ENCODER_DT, GPIO.IN)
GPIO.setup(ENCODER_SW, GPIO.IN, pull_up_down=GPIO.PUD_UP)

lastCLK = GPIO.input(ENCODER_CLK)
last_time = time.time()

# =========================
# MOTOR CONTROL
# =========================

def rotate(axis_name, degrees, direction):
    axis = AXES[axis_name]

    GPIO.output(axis["dir"], GPIO.HIGH if direction else GPIO.LOW)

    steps = int(abs(degrees) / STEP_ANGLE)

    for _ in range(steps):
        GPIO.output(axis["pul"], GPIO.HIGH)
        time.sleep(STEP_DELAY)
        GPIO.output(axis["pul"], GPIO.LOW)
        time.sleep(STEP_DELAY)

# =========================
# ENCODER HANDLER
# =========================

def get_encoder_motion(axis, step):
    global lastCLK, last_time

    # debounce
    if time.time() - last_time < 0.002:
        return

    currentCLK = GPIO.input(ENCODER_CLK)

    if currentCLK != lastCLK:

        clockwise = GPIO.input(ENCODER_DT) != currentCLK
        rotate(axis, step, clockwise)

        last_time = time.time()

    lastCLK = currentCLK

    # button press
    if GPIO.input(ENCODER_SW) == GPIO.LOW:
        print("Encoder button pressed")
        time.sleep(0.3)

# =========================
# MAIN PROGRAM
# =========================

def main():

    print("\n=== Multi Axis Jog Controller ===")

    try:
        while True:

            axis = input("\nSelect axis (x/y/z/a): ").lower()

            if axis not in AXES:
                print("Invalid axis")
                continue

            step = float(input("Step size in degrees: "))

            print("Rotate encoder to jog motor. Ctrl+C to change axis.")

            while True:
                get_encoder_motion(axis, step)
                time.sleep(0.001)

    except KeyboardInterrupt:
        print("\nStopping...")

    finally:
        GPIO.cleanup()
        print("GPIO cleaned")

# =========================

if __name__ == "__main__":
    main()
