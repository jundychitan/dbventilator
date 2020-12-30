from PyQt5.QtCore import pyqtSignal, QThread
import numpy as np
import time
import datetime

class Sensor(QThread):

    result_callback = pyqtSignal(object, object)

    def run(self):
        
        while not self.stop_flag:
            time.sleep(0.5) # 500ms
            try:
                self.read()
                if self.recording:
                    if len(self.sensor_stack) < self.sensor_stack_count:
                        self.sensor_stack.append(float(self.current_reading))
                        self.time_stack.append(self.timestamp())
                    else:
                        del self.sensor_stack[0]
                        del self.time_stack[0]
                        self.sensor_stack.append(float(self.current_reading))
                        self.time_stack.append(self.timestamp())
                    self.result_callback.emit(self.sensor_stack, self.time_stack)
                else:
                    # Not recording values
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
        self.recording = True

    def set_recording(self, state):
        self.recording = state

    def set_path(self, path):
        self.path = path

    def timestamp(self):
        self.t_elapse += 1
        return self.t_elapse

    def read(self):
        self.current_reading = open(self.path, "r").read()

    def stop(self):
        self.stop_flag = True

    