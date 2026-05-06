#import RPi.GPIO as GPIO
import time


def main_servo(stepper):
    
    if stepper == "x":
        PUL_PIN = 9
        DIR_PIN = 8
        ENA_PIN = 7
    else :
        PUL_PIN = 12
        DIR_PIN = 13
        ENA_PIN = 14


    # Encoder pins
    ENCODER_CLK = 5
    ENCODER_DT  = 4
    ENCODER_SW  = 3


    stepsPerClick = 200      # adjust for speed & resolution
    pulseDelay = 0.00005     # 50 microseconds

    positionSteps = 0
    lastCLK = 0
    
    print(stepper)

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(ENCODER_CLK, GPIO.IN)
    GPIO.setup(ENCODER_DT, GPIO.IN)
    GPIO.setup(ENCODER_SW, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.setup(PUL_PIN, GPIO.OUT)
    GPIO.setup(DIR_PIN, GPIO.OUT)
    GPIO.setup(ENA_PIN, GPIO.OUT)

    GPIO.output(ENA_PIN, GPIO.LOW)  # Enable driver

    lastCLK = GPIO.input(ENCODER_CLK)
    print("Initial CLK:", lastCLK)

    def moveMotor(direction, steps):
        GPIO.output(DIR_PIN, GPIO.HIGH if direction else GPIO.LOW)

        for _ in range(steps):
            GPIO.output(PUL_PIN, GPIO.HIGH)
            time.sleep(pulseDelay)
            GPIO.output(PUL_PIN, GPIO.LOW)
            time.sleep(pulseDelay)

    try:
        while True:
            currentCLK = GPIO.input(ENCODER_CLK)

            if currentCLK != lastCLK:
                if GPIO.input(ENCODER_DT) != currentCLK:
                    moveMotor(True, stepsPerClick)   # CW
                    positionSteps += stepsPerClick
                else:
                    moveMotor(False, stepsPerClick)  # CCW
                    positionSteps -= stepsPerClick

                print("Position:", positionSteps)

            lastCLK = currentCLK

            # Reset position on button press
            if GPIO.input(ENCODER_SW) == GPIO.LOW:
                positionSteps = 0
                print("Position reset")
                time.sleep(1)

            time.sleep(0.001)

    except KeyboardInterrupt:
        print("Exiting...")

    finally:
        GPIO.cleanup()
