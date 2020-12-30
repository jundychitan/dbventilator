from PyQt5.QtCore import pyqtSignal, QThread
import numpy as np
import time
import datetime

class Sensor(QThread):

    result_callback = pyqtSignal(object, object)

    def run(self):
        
        while not self.stop_flag:
            time.sleep(0.5) # 500ms
            if self.is_paused:
                continue

            if self.process_only:
                self.result_callback.emit(None, None)
                continue
            try:
                if self.recording:
                    self.read()
                    if len(self.sensor_stack) < self.sensor_stack_count:
                        self.sensor_stack.append(float(self.current_reading))
                        self.time_stack.append(self.timestamp())
                    else:
                        del self.sensor_stack[0]
                        del self.time_stack[0]
                        self.sensor_stack.append(float(self.current_reading))
                        self.time_stack.append(self.timestamp())
                    self.result_callback.emit(self.sensor_stack, self.time_stack)
                elif self.time_is_data:
                    self.read()
                    if self.current_reading=="reset":
                        self.t_elapse = 0
                    self.result_callback.emit(self.timestamp(), None)
                else:
                    # Not recording values
                    self.read()
                    self.result_callback.emit(self.current_reading, None)

            except Exception as e:
                pass

    def setup(self):
        self.sensor_stack_count = 100
        self.sensor_stack = []
        self.time_stack = []
        self.stop_flag = False
        self.path = ""
        self.current_reading = 0
        self.t_elapse = 0
        self.time_is_data = False
        self.recording = True
        self.is_paused = False
        self.name = ""
        self.process_only = False

    def set_recording(self, state):
        self.recording = state

    def set_name(self, name):
        self.name = name

    def as_proceedure(self):
        self.process_only=True

    def get_name(self):
        return self.name

    def set_path(self, path):
        self.path = path

    def for_timestamp(self, state):
        self.time_is_data=True

    def freeze(self):
        self.is_paused = True

    def unfreeze(self):
        self.is_paused = False

    def timestamp(self):
        self.t_elapse += 1 # 500 ms per call
        return self.t_elapse

    def read(self):
        self.current_reading = open(self.path, "r").read()

    def stop(self):
        self.stop_flag = True

    