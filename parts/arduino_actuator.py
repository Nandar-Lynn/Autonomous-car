import serial
import time

class ArduinoActuatorController:
    def __init__(self, port='/dev/ttyACM0', baudrate=57600):
        self.serial = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)  # Allow some time for the connection to establish
        
        self.current_steering = 90  # Default to middle position (90 degrees)
        self.current_throttle = 0   # Default to stop

    def send_command(self, steering_angle, throttle_speed):
        # Map the values from [-1, 1] to your desired PWM range, e.g., [1000, 2000]
        pwm_steering = int((steering_angle / 180.0) * (2300 - 700) + 700)
        pwm_throttle = int((throttle_speed * 500) + 1500)
        
        command = f'STEER:{pwm_steering};THROTTLE:{pwm_throttle};'
        print(f"Sending to Arduino: {command}")
        self.serial.write(command.encode())

    def run(self, steering, throttle):
        print(f"Steering Value: {steering}, Throttle Value: {throttle}")
        self.send_command(steering_angle=steering, throttle_speed=throttle)
        return steering, throttle
    
    def update(self, pulse):
        value = (pulse - 1500) / 500.0  # Simple example
        return value

    def set_pulse(self, channel, pulse):
        if channel == "steering":
            angle = (pulse - 700) * 180.0 / (2300 - 700)  # Map pulse width back to angle
            self.send_command(steering_angle=angle, throttle_speed=self.current_throttle)
        elif channel == "throttle":
            speed = (pulse - 1000) / 100.0  # Map pulse width back to speed (-1 to 1)
            self.send_command(steering_angle=self.current_steering, throttle_speed=speed)

    def shutdown(self):
        self.serial.close()

