import json
import os
import time
from datetime import datetime


class DataLogger:
    def __init__(self, log_dir='logs'):
        self.log_dir = log_dir
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

    def log_data(self, image, center, throttle, steering):
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        log_entry = {
            'timestamp': timestamp,
            'center': center,
            'throttle': throttle,
            'steering': steering
        }
        image_filename = f'{timestamp}.jpg'
        image_path = os.path.join(self.log_dir, image_filename)
        image.save(image_path, format='JPEG')
        log_entry['image'] = image_filename

        log_file = os.path.join(self.log_dir, 'log.json')
        with open(log_file, 'a') as f:
            json.dump(log_entry, f)
            f.write('\n')
