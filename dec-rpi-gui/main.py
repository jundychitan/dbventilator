import sys
from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import (Qt, pyqtSignal, QThread, pyqtSlot, QCoreApplication)
from dashboard import *
import numpy as np
from threading import Thread
from sensor import *
import settings as form_settings
from helper import *
from pyqtgraph import *
import time


class Main(QMainWindow, Ui_MainWindow):

    process_pool = []
    running = 0
    is_assist = 1

    def __init__(self):
        super(Main, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.showFullScreen()
        self.btn_settings.clicked.connect(self.show_Settings)
        self.btn_run.clicked.connect(self.run_process)
    
        # Graph Elements
        self.gv_pressure.setLabels(left='Pressure')
        self.gv_pressure.setAntialiasing(True)
        self.gv_pressure.setRange(yRange=[0,15])
        self.gv_pressure.setMouseEnabled(x=False, y=False)
        self.gv_pressure

        self.gv_flow.setLabels(left='Flow')
        self.gv_flow.setAntialiasing(True)
        self.gv_flow.setRange(yRange=[0,30])
        self.gv_flow.setMouseEnabled(x=False, y=False)

        self.gv_volume.setLabels(left='Volume')
        self.gv_volume.setAntialiasing(True)
        self.gv_volume.setRange(yRange=[0,800])
        self.gv_volume.setMouseEnabled(x=False, y=False)

        self.refresh_display()
        
        # Thread Instances
        pressure_sensor = Sensor(self)
        pressure_sensor.setup()
        pressure_sensor.set_path(env("PRESSURE_PATH"))
        pressure_sensor.result_callback.connect(self.pressure_listener)
        pressure_sensor.start()
        self.process_pool.append(pressure_sensor)

        flow_sensor = Sensor(self)
        flow_sensor.setup()
        flow_sensor.set_path(env("FLOW_PATH"))
        flow_sensor.result_callback.connect(self.flow_listener)
        flow_sensor.start()
        self.process_pool.append(flow_sensor)

        volume_sensor = Sensor(self)
        volume_sensor.setup()
        volume_sensor.set_path(env("VOLUME_PATH"))
        volume_sensor.result_callback.connect(self.volume_listener)
        volume_sensor.start()
        self.process_pool.append(volume_sensor)

        # Thread for semi-realtime gui update !Note: dont add on process pool(for sensors only)
        #display_refresh_th = QThread(target=self.realtime_refresh_display, name="GUI Update")
        #display_refresh_th.start()

        peak_pressure = Sensor(self)
        peak_pressure.setup()
        peak_pressure.set_path(env("PEAK_PRESSURE_PATH"))
        peak_pressure.set_recording(False)
        peak_pressure.result_callback.connect(self.peak_pressure_listener)
        peak_pressure.start()
        self.process_pool.append(peak_pressure)

        p_plateau = Sensor(self)
        p_plateau.setup()
        p_plateau.set_path(env("P_PLATEAU_PATH"))
        p_plateau.set_recording(False)
        p_plateau.result_callback.connect(self.p_plateau_listener)
        p_plateau.start()
        self.process_pool.append(p_plateau)

        th_alarm_color = Sensor(self)
        th_alarm_color.setup()
        th_alarm_color.set_path(env("ALARM_COLOR_PATH"))
        th_alarm_color.set_recording(False)
        th_alarm_color.result_callback.connect(self.th_alarm_color_listener)
        th_alarm_color.start()
        self.process_pool.append(th_alarm_color)

        th_alarm_status = Sensor(self)
        th_alarm_status.setup()
        th_alarm_status.set_path(env("ALARM_STATUS_PATH"))
        th_alarm_status.set_recording(False)
        th_alarm_status.result_callback.connect(self.th_alarm_status_listener)
        th_alarm_status.start()
        self.process_pool.append(th_alarm_status)
        """
        with open(env("PEAK_PRESSURE_PATH"), 'r') as f: self.lbl_pressure_peak.setText(f'{f.read()}')
            with open(env("P_PLATEAU_PATH"), 'r') as f: self.lbl_p_plateau.setText(f'{f.read()}')

            with open(env("ALARM_COLOR_PATH"), 'r') as f: self.alarm_color.setStyleSheet("border-radius: 3px;\nbackground-color: rgb("+f.read()+");")
            with open(env("ALARM_STATUS_PATH"), 'r') as f: self.alarm_status.setText(f'{f.read()}')
        """


    def run_process(self):
        if self.running==0:
            self.running=1
            self.start_process()
            self.btn_run.setStyleSheet("border-radius: 10px; background-color: rgb(170, 0, 0);")
        else:
            self.running=0
            self.stop_process()
            self.btn_run.setStyleSheet('border-radius: 10px; background-color: rgb(0, 170, 127);')

    def start_process(self):
        with open(env("PROCESS_CONTROL_PATH"), 'w+') as f: f.write("on")

    def stop_process(self):
        with open(env("PROCESS_CONTROL_PATH"), 'w+') as f: f.write("off")

    def show_Settings(self):
        self.window = QMainWindow()
        self.form_settingsProperties = form_settings.Ui_MainWindow()
        self.ui = self.form_settingsProperties.setupUi(self.window)
        self.window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.window.showFullScreen()
        self.form_settingsProperties.btn_save.clicked.connect(self.save_settings)
        self.form_settingsProperties.btn_assist.clicked.connect(self.set_assist)
        self.form_settingsProperties.btn_control.clicked.connect(self.set_control)
        
        with open(env("MODE_PATH"), 'r') as f:
            if f.read()=="control":
                self.form_settingsProperties.btn_control.setStyleSheet("color: rgb(0, 0, 0);\nbackground-color: rgb(252, 163, 17);")
            else:
                self.form_settingsProperties.btn_assist.setStyleSheet("color: rgb(0, 0, 0);\nbackground-color: rgb(252, 163, 17);")
        
        with open(env("TIDAL_PATH"), 'r') as f: self.form_settingsProperties.txt_tidal_volume.setValue(int(f.read()))
        
        with open(env("RESP_RATE_PATH"), 'r') as f: self.form_settingsProperties.txt_resprate.setValue(int(f.read()))

        with open(env("IERATIO_PATH"), 'r') as f: self.form_settingsProperties.txt_ieratio.setValue(int(f.read()))

        with open(env("PEAK_FLOW_PATH"), 'r') as f: self.form_settingsProperties.txt_peakflow.setValue(int(f.read()))

        with open(env("PEEP_PATH"), 'r') as f: self.form_settingsProperties.txt_peep.setValue(int(f.read()))

        with open(env("FIO2_PATH"), 'r') as f: self.form_settingsProperties.txt_fio2.setValue(int(f.read()))
        self.window.show()

    def set_assist(self):
        self.is_assist = 1
        self.form_settingsProperties.btn_assist.setStyleSheet("color: rgb(0, 0, 0);\nbackground-color: rgb(252, 163, 17);")
        self.form_settingsProperties.btn_control.setStyleSheet("color: rgb(0, 0, 0);\nbackground-color: rgb(229, 229, 229);")

    def set_control(self):
        self.is_assist = 0
        self.form_settingsProperties.btn_control.setStyleSheet("color: rgb(0, 0, 0);\nbackground-color: rgb(252, 163, 17);")
        self.form_settingsProperties.btn_assist.setStyleSheet("color: rgb(0, 0, 0);\nbackground-color: rgb(229, 229, 229);")

    def save_settings(self):
        if self.is_assist:
            with open(env("MODE_PATH"), 'w+') as f: f.write("assist")
        else:
            with open(env("MODE_PATH"), 'w+') as f: f.write("control")

        volume = str(self.form_settingsProperties.txt_tidal_volume.text()).replace(' mL', '')
        with open(env("TIDAL_PATH"), 'w+') as f: f.write(volume)

        resp_rate = str(self.form_settingsProperties.txt_resprate.text()).replace(' Bpm', '')
        with open(env("RESP_RATE_PATH"), 'w+') as f: f.write(resp_rate)

        ieratio = str(self.form_settingsProperties.txt_ieratio.text()).replace("1:", "")
        with open(env("IERATIO_PATH"), 'w+') as f: f.write(ieratio)

        flow = str(self.form_settingsProperties.txt_peakflow.text()).replace(' Lpm', '')
        with open(env("PEAK_FLOW_PATH"), 'w+') as f: f.write(flow)

        peep = str(self.form_settingsProperties.txt_peep.text()).replace(" cmH2O", "")
        with open(env("PEEP_PATH"), 'w+') as f: f.write(peep)

        fio2 = str(self.form_settingsProperties.txt_fio2.text()).replace(' %', '')
        with open(env("FIO2_PATH"), 'w') as f: f.write(fio2)

        self.refresh_display()
        self.window.close()

    def refresh_display(self):
        with open(env("MODE_PATH"), 'r') as f: self.lbl_mode.setText(f.read().title())
        with open(env("TIDAL_PATH"), 'r') as f: self.lbl_tidal_volume.setText(f'{f.read()}')
        with open(env("RESP_RATE_PATH"), 'r') as f: self.lbl_resp_rate.setText(f'{f.read()}')
        with open(env("IERATIO_PATH"), 'r') as f: self.lbl_ieratio.setText(f'1:{f.read()}')
        with open(env("PEAK_FLOW_PATH"), 'r') as f: self.lbl_flow.setText(f'{f.read()}')
        with open(env("PEEP_PATH"), 'r') as f: self.lbl_peep.setText(f'{f.read()}')
        with open(env("FIO2_PATH"), 'r') as f: self.lbl_fio2.setText(f'{f.read()}%')
        
    @pyqtSlot(object, object)
    def pressure_listener(self, pressure_stack, time_stack):
        self.gv_pressure.clear()

        self.gv_pressure.plot(x=time_stack, y=pressure_stack, pen=mkPen(color=(252, 163, 17)))

    @pyqtSlot(object, object)
    def flow_listener(self, flow_stack, time_stack):
        self.gv_flow.clear()
        self.gv_flow.plot(x=time_stack, y=flow_stack, pen=mkPen(color=(252, 163, 17)))

    @pyqtSlot(object, object)
    def volume_listener(self, volume_stack, time_stack):
        self.gv_volume.clear()
        self.gv_volume.plot(x=time_stack, y=volume_stack, pen=mkPen(color=(252, 163, 17)))

    @pyqtSlot(object, object)
    def peak_pressure_listener(self, reading, other):
        self.lbl_pressure_peak.setText(f'{reading}')

    @pyqtSlot(object, object)
    def p_plateau_listener(self, reading, other):
        self.lbl_p_plateau.setText(reading)

    @pyqtSlot(object, object)
    def th_alarm_color_listener(self, reading, other):
        self.alarm_color.setStyleSheet("border-radius: 3px;\nbackground-color: rgb("+reading+");")

    @pyqtSlot(object, object)
    def th_alarm_status_listener(self, reading, other):
        self.alarm_status.setText(reading)

    def closeEvent(self, event):
        for process in self.process_pool:
            process.stop()
            time.sleep(1)
        
        time.sleep(1)

app = QtWidgets.QApplication([])
application = Main()
application.show()
sys.exit(app.exec_())