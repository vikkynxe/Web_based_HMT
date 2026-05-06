import RPi.GPIO as GPIO
import time


#// Initialization All

GPIO.setmode(GPIO.BCM)

# GPIO pin setup
PUL_X = 6   #  Pulse
DIR_X = 5   #  Direction
ENA_X = 24   #  Enable

GPIO.setup(PUL_X, GPIO.OUT)
GPIO.setup(DIR_X, GPIO.OUT)
GPIO.setup(ENA_X, GPIO.OUT)
GPIO.output(ENA_X, GPIO.LOW)


# GPIO pin setup
PUL_Y = 16
DIR_Y = 20
ENA_Y = 21

GPIO.setup(PUL_Y, GPIO.OUT)
GPIO.setup(DIR_Y, GPIO.OUT)
GPIO.setup(ENA_Y, GPIO.OUT)
GPIO.output(ENA_Y, GPIO.LOW)


# GPIO pin setup
PUL_Z = 25
DIR_Z = 8
ENA_Z = 7

GPIO.setup(PUL_Z, GPIO.OUT)
GPIO.setup(DIR_Z, GPIO.OUT)
GPIO.setup(ENA_Z, GPIO.OUT)
GPIO.output(ENA_Z, GPIO.LOW)


# GPIO pin setup
PUL_A = 19
DIR_A = 26
ENA_A = 13

GPIO.setup(PUL_A, GPIO.OUT)
GPIO.setup(DIR_A, GPIO.OUT)
GPIO.setup(ENA_A, GPIO.OUT)
GPIO.output(ENA_A, GPIO.LOW)


# Stepper specs
STEP_ANGLE = 1.8  # degrees per step
STEP_DELAY = 0.001  # seconds between pulses (speed)

def rotate_degrees_x(degrees, direction):
    # Set direction
    if direction:
        GPIO.output(DIR_X, GPIO.HIGH)
    else:
        GPIO.output(DIR_X, GPIO.LOW)

    steps = int(abs(degrees) / STEP_ANGLE)

    for _ in range(steps):
        GPIO.output(PUL_X, GPIO.HIGH)
        time.sleep(STEP_DELAY)
        GPIO.output(PUL_X, GPIO.LOW)
        time.sleep(STEP_DELAY)
        
        
def rotate_degrees_y(degrees, direction):
    # Set direction
    if direction:
        GPIO.output(DIR_Y, GPIO.HIGH)
    else:
        GPIO.output(DIR_Y, GPIO.LOW)

    steps = int(abs(degrees) / STEP_ANGLE)

    for _ in range(steps):
        GPIO.output(PUL_Y, GPIO.HIGH)
        time.sleep(STEP_DELAY)
        GPIO.output(PUL_Y, GPIO.LOW)
        time.sleep(STEP_DELAY)
        
        
        
def rotate_degrees_z(degrees, direction):
    # Set direction
    if direction:
        GPIO.output(DIR_Z, GPIO.HIGH)
    else:
        GPIO.output(DIR_Z, GPIO.LOW)

    steps = int(abs(degrees) / STEP_ANGLE)

    for _ in range(steps):
        GPIO.output(PUL_Z, GPIO.HIGH)
        time.sleep(STEP_DELAY)
        GPIO.output(PUL_Z, GPIO.LOW)
        time.sleep(STEP_DELAY)
        
        
def rotate_degrees_a(degrees, direction):
    # Set direction
    if direction:
        GPIO.output(DIR_A, GPIO.HIGH)
    else:
        GPIO.output(DIR_A, GPIO.LOW)

    steps = int(abs(degrees) / STEP_ANGLE)

    for _ in range(steps):
        GPIO.output(PUL_A, GPIO.HIGH)
        time.sleep(STEP_DELAY)
        GPIO.output(PUL_A, GPIO.LOW)
        time.sleep(STEP_DELAY)
        

ENCODER_CLK = 22
ENCODER_DT  = 27
ENCODER_SW  = 17

GPIO.setup(ENCODER_CLK, GPIO.IN)
GPIO.setup(ENCODER_DT, GPIO.IN)
GPIO.setup(ENCODER_SW, GPIO.IN, pull_up_down=GPIO.PUD_UP)


lastCLK = GPIO.input(ENCODER_CLK)

def get_position(axis,nou):
    global lastCLK
    currentCLK = GPIO.input(ENCODER_CLK)
    #// Clock wise
    if currentCLK != lastCLK:
        if GPIO.input(ENCODER_DT) != currentCLK:
            if (axis == "x"):
                rotate_degrees_x((nou or 1), True)
            if (axis == "y"):
                rotate_degrees_y((nou or 1), True)
            if (axis == "z"):
                rotate_degrees_z((nou or 1), True)
            if (axis == "a"):
                rotate_degrees_a((nou or 1), True)
    #// Counter Clock wise
        else:
            if (axis == "x"):
                rotate_degrees_x((nou or 1), False)
            if (axis == "y"):
                rotate_degrees_y((nou or 1), False)
            if (axis == "z"):
                rotate_degrees_z((nou or 1), False)
            if (axis == "a"):
                rotate_degrees_a((nou or 1), False)

    lastCLK = currentCLK

    # Reset position on button press
    if GPIO.input(ENCODER_SW) == GPIO.LOW:
        print("Position reset")
        time.sleep(1)


def finishing():
    GPIO.cleanup()
    
    
if __name__ == "__main__":

    try:
        while True:
            deg = float(input("Enter degrees to rotate x(±): "))
            rotate_degrees_x(deg,True)
            print(f"Rotated {deg} degrees")
            
            deg = float(input("Enter degrees to rotate y(±): "))
            rotate_degrees_y(deg,True)
            print(f"Rotated {deg} degrees")
            
            deg = float(input("Enter degrees to rotate z(±): "))
            rotate_degrees_z(deg,True)
            print(f"Rotated {deg} degrees")
            
            deg = float(input("Enter degrees to rotate a(±): "))
            rotate_degrees_a(deg,True)
            print(f"Rotated {deg} degrees")

    except KeyboardInterrupt:
        ...

    finally:
        finishing()
