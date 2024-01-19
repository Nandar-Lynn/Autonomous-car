# """ 
# My CAR CONFIG 

import os

# # FILE PATHS
CAR_PATH = PACKAGE_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.join(CAR_PATH, 'data')
MODELS_PATH = os.path.join(CAR_PATH, 'models')
# VEHICLE loop
DRIVE_LOOP_HZ = 20      # the vehicle loop will pause if faster than this speed.
MAX_LOOPS = None        # the vehicle loop can abort after this many iterations, when given a positive integer.
# # CAMERA configuration
CAMERA_TYPE = "WEBCAM"   # (PICAM|WEBCAM|CVCAM|CSIC|V4L|D435|MOCK|IMAGE_LIST)
TOGGLE_RECORDING_BTN = "web/r"

IMAGE_W = 640
IMAGE_H = 480
IMAGE_DEPTH = 3         # default RGB=3, make 1 for mono
CAMERA_FRAMERATE = DRIVE_LOOP_HZ
CAMERA_VFLIP = False
CAMERA_HFLIP = False
CAMERA_INDEX = 0 # used for 'WEBCAM' and 'CVCAM' when there is more than one camera connected
# # For CSIC camera - If the camera is mounted in a rotated position, changing the below parameter will correct the output frame orientation
# CSIC_CAM_GSTREAMER_FLIP_PARM = 0 # (0 => none , 4 => Flip horizontally, 6 => Flip vertically)
BGR2RGB = False  # true to convert from BRG format to RGB format; requires opencv
# # For IMAGE_LIST camera
PATH_MASK = "~/mycar/data/tub_1_20-03-12/*.jpg"

#(corresponding to tire angle at steering == -1)
# # MEASURED ROBOT PROPERTIES
AXLE_LENGTH = 0.214     # length of axle; distance between left and right wheels in meters
WHEEL_BASE = 0.313       # distance between front and back wheels in meters
WHEEL_RADIUS = 0.055  # radius of wheel in meters
MIN_SPEED = 0.1        # minimum speed in meters per second; speed below which car stalls
MAX_SPEED = 3.0        # maximum speed in meters per second; speed at maximum throttle (1.06
MIN_THROTTLE = 0.1     # throttle (0 to 1.0) that corresponds to MIN_SPEED, throttle below which car stalls
MAX_STEERING_ANGLE = 3.141592653589793 / 4  # for car-like robot; maximum steering angle in radians
DRIVE_TRAIN_TYPE = "PWM_STEERING_THROTTLE"
# Arduino configuration
STEERING_ARDUINO_PIN = 5  # Example value: Pin number for the steering servo on the Arduino
THROTTLE_ARDUINO_PIN = 6  # Example value: Pin number for the throttle/ESC on the Arduino
# PWM values for Steering with Arduino
STEERING_ARDUINO_LEFT_PWM = 20  # PWM value for full left turn on the Arduino
STEERING_ARDUINO_RIGHT_PWM = 160  # PWM value for full right turn on the Arduino
# PWM values for Throttle with Arduino
THROTTLE_ARDUINO_FORWARD_PWM = 120  # PWM value for full forward throttle on the Arduino
THROTTLE_ARDUINO_STOPPED_PWM = 90  # PWM value when throttle is stopped on the Arduino
THROTTLE_ARDUINO_REVERSE_PWM = 60  # PWM value for full reverse throttle on the Arduino

