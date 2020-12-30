from PyQt5.QtCore import pyqtSignal, QThread
import numpy as np
import time

class Sensor(QThread):

    result_callback = pyqtSignal(list)

    def run(self):
        while not self.stop_flag:
            time.sleep(0.1)
            try:
                self.read()
                if len(self.sensor_stack) < self.sensor_stack_count:
                    self.sensor_stack.append(self.current_reading)
                else:
                    del self.sensor_stack[0]
                    self.sensor_stack.append(self.current_reading)
                self.result_callback.emit(self.sensor_stack)
            except:
                pass			

    def setup(self):
        self.sensor_stack_count = 100
        self.sensor_stack = []
        self.stop_flag = False
        self.path = ""
        self.current_reading = 0

    def set_path(self, path):
        self.path = path

    def read(self):
        self.current_reading = float(open(self.path, "r").read())

    def stop(self):
        self.stop_flag = True

    
