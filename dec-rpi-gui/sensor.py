from PyQt5.QtCore import pyqtSignal, QThread
import numpy as np
import time
import datetime

class Sensor(QThread):

    result_callback = pyqtSignal(list, list)

    def run(self):
        
        while not self.stop_flag:
            time.sleep(0.1) # 100ms
            try:
                self.read()
                if len(self.sensor_stack) < self.sensor_stack_count:
                    self.sensor_stack.append(self.current_reading)
                    self.time_stack.append(self.timestamp())
                else:
                    del self.sensor_stack[0]
                    del self.time_stack[0]
                    self.sensor_stack.append(self.current_reading)
                    self.time_stack.append(self.timestamp())

                self.result_callback.emit(self.sensor_stack, self.time_stack)
            except Exception as e:
                pass

    def setup(self):
        self.sensor_stack_count = 200
        self.sensor_stack = []
        self.time_stack = []
        self.stop_flag = False
        self.path = ""
        self.current_reading = 0
        self.t_elapse = 0

    def set_path(self, path):
        self.path = path

    def timestamp(self):
        self.t_elapse += 1
        return self.t_elapse

    def read(self):
        self.current_reading = float(open(self.path, "r").read())

    def stop(self):
        self.stop_flag = True

    