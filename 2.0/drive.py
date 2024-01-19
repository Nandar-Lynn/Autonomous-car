import os
import logging
#
# import cv2 early to avoid issue with importing after tensorflow
# see https://github.com/opencv/opencv/issues/14884#issuecomment-599852128
#
import myconfig as cfg
import pygame 
from pygame.locals import *
import vehicle
from camera import Webcam
from actuator import ArdPWMSteering, ArdPWMThrottle, ArduinoFirmata
from docopt import docopt
import config

class KeyboardController:
    def __init__(self):
        pygame.init()
        self.screen=pygame.display.set_mode((100, 100))
        self.throttle = 0.0
        self.steering = 0.0
        self.recording = False
    def update(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    self.throttle += 0.05
                elif event.key == K_DOWN:
                    self.throttle -= 0.05
                elif event.key == K_RIGHT:
                    self.steering += 0.05
                elif event.key == K_LEFT:
                    self.steering -= 0.05
                elif event.key == K_r:
                    self.recording = not self.recording
            elif event.type == KEYUP:
                if event.key in [K_UP, K_DOWN]:
                    self.throttle = 0.0
                if event.key in [K_RIGHT, K_LEFT]:
                    self.steering = 0.0
        return self.steering, self.throttle, 'user', self.recording
         
def drive(cfg, use_joystick=False, camera_type='single'):

    # if use_joystick:
    #     ctr = get_js_controller(cfg)
    #     V.add(ctr,
    #         inputs=['cam/image_array'],
    #         outputs=['user/angle', 'user/throttle', 'user/mode', 'recording'],
    #         threaded=True)
    # else:
    # # Use the local web controller
    V = vehicle.Vehicle()
    use_keyboard = True # Toggle to turn off keyboard controll  <------- True/False
    if use_keyboard:  # all new
        ctr = KeyboardController()
        V.add(ctr,
        outputs=['user/angle', 'user/throttle', 'user/mode', 'recording'],
        threaded=True)
    # else: # to here
    #     ctr = LocalWebController(port=cfg.WEB_CONTROL_PORT, mode=cfg.WEB_INIT_MODE, address='0.0.0.0')
    #     V.add(ctr,
    #         inputs=['cam/image_array', 'tub/num_records'],
    #         outputs=['user/angle', 'user/throttle', 'user/mode', 'recording'],
    #         threaded=True)
    #     is_differential_drive = cfg.DRIVE_TRAIN_TYPE.startswith("DC_TWO_WHEEL")

#Initialize car
        cam = Webcam(image_w=cfg.IMAGE_W, image_h=cfg.IMAGE_H, framerate=cfg.CAMERA_FRAMERATE,      camera_index=cfg.CAMERA_INDEX)
        V.add(cam, outputs=['cam/image_array'], threaded=True)
    # Insert the Arduino actuator setup here:
        arduino_controller = ArduinoFirmata(
        servo_pin=cfg.STEERING_ARDUINO_PIN,
        esc_pin=cfg.THROTTLE_ARDUINO_PIN)

        steering = ArdPWMSteering(controller=arduino_controller,
                            left_pulse=cfg.STEERING_ARDUINO_LEFT_PWM,
                            right_pulse=cfg.STEERING_ARDUINO_RIGHT_PWM)

        throttle = ArdPWMThrottle(controller=arduino_controller,
                            max_pulse=cfg.THROTTLE_ARDUINO_FORWARD_PWM,
                            zero_pulse=cfg.THROTTLE_ARDUINO_STOPPED_PWM,
                            min_pulse=cfg.THROTTLE_ARDUINO_REVERSE_PWM)

        V.add(steering, inputs=['user/angle'])
        V.add(throttle, inputs=['user/throttle'])


        # #
        # # add the user input controller(s)
        # # - this will add the web controller
        # # - it will optionally add any configured 'joystick' controller
        # #
        # has_input_controller = hasattr(cfg, "CONTROLLER_TYPE") and cfg.CONTROLLER_TYPE != "mock"
        # ctr = add_user_controller(V, cfg, use_joystick, input_image = 'map/image')
        # #
        # # maintain run conditions for user mode and autopilot mode parts.
        # #
        # V.add(UserPilotCondition(),
        #     inputs=['user/mode', "cam/image_array", "cam/image_array"],
        #     outputs=['run_user', "run_pilot", "ui/image_array"])


        # # This is the path object. It will record a path when distance changes and it travels
        # # at least cfg.PATH_MIN_DIST meters. Except when we are in follow mode, see below...
        # path = CsvThrottlePath(min_dist=cfg.PATH_MIN_DIST)
        # V.add(path, inputs=['recording', 'pos/x', 'pos/y', 'user/throttle'], outputs=['path', 'throttles'])

if __name__ == '__main__':
    args = docopt(__doc__)
    cfg = config.load_config()

    log_level = args['--log'] or "INFO"
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % log_level)
    logging.basicConfig(level=numeric_level)


    if args['drive']:
        drive(cfg, use_joystick=args['--js'], camera_type=args['--camera'])