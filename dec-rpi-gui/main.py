import sys
from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import (Qt, pyqtSignal, QThread, pyqtSlot, QCoreApplication)
from dashboard import *
import numpy as np
from threading import *
from sensor import *
import settings as form_settings


class Main(QMainWindow, Ui_MainWindow):

    process_pool = []

    def __init__(self):
        super(Main, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.showFullScreen()
        self.btn_settings.clicked.connect(self.show_Settings)
        self.btn_start.clicked.connect(self.start_process)
        self.btn_stop.clicked.connect(self.stop_process)

        # Graph Elements
        self.gv_pressure.setLabels(title='Pressure (cmH2O)', left='Magnitude', bottom='Time (t)')
        self.gv_pressure.setAntialiasing(True)
        self.gv_pressure.setRange(yRange=[0,50])

        self.gv_flow.setLabels(title='Flow (SLPM)', left='Magnitude', bottom='Time (t)')
        self.gv_flow.setAntialiasing(True)
        self.gv_flow.setRange(yRange=[0,30])

        self.gv_volume.setLabels(title='Volume (ml)', left='Magnitude', bottom='Time (t)')
        self.gv_volume.setAntialiasing(True)
        self.gv_volume.setRange(yRange=[0,800])

        self.refresh_display()
        
        # Thread Instances
        pressure_sensor = Sensor(self)
        pressure_sensor.setup()
        pressure_sensor.set_path("/mnt/ramdisk/pressure.txt")
        pressure_sensor.result_callback.connect(self.pressure_listener)
        pressure_sensor.start()
        self.process_pool.append(pressure_sensor)

        flow_sensor = Sensor(self)
        flow_sensor.setup()
        flow_sensor.set_path("/mnt/ramdisk/flow.txt")
        flow_sensor.result_callback.connect(self.flow_listener)
        flow_sensor.start()
        self.process_pool.append(flow_sensor)

        volume_sensor = Sensor(self)
        volume_sensor.setup()
        volume_sensor.set_path("/mnt/ramdisk/volume.txt")
        volume_sensor.result_callback.connect(self.volume_listener)
        volume_sensor.start()
        self.process_pool.append(volume_sensor)

    def start_process(self):
        with open('/home/pi/dec-rpi-gui/temp/process_control.txt', 'w') as f: f.write("on")

    def stop_process(self):
        with open('/home/pi/dec-rpi-gui/temp/process_control.txt', 'w') as f: f.write("off")

    def show_Settings(self):
        self.window = QMainWindow()
        self.form_settingsProperties = form_settings.Ui_MainWindow()
        self.ui = self.form_settingsProperties.setupUi(self.window)
        self.window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.window.showFullScreen()
        self.form_settingsProperties.btn_save_changes.clicked.connect(self.save_settings)

        with open('/home/pi/dec-rpi-gui/temp/mode.txt', 'r') as f: self.form_settingsProperties.cmb_mode.setCurrentText(f.read().title())

        with open('/home/pi/dec-rpi-gui/temp/tidal_volume.txt', 'r') as f: self.form_settingsProperties.txt_volume.setValue(int(f.read()))

        with open('/home/pi/dec-rpi-gui/temp/resp_rate.txt', 'r') as f: self.form_settingsProperties.txt_resp_rate.setValue(int(f.read()))

        with open('/home/pi/dec-rpi-gui/temp/ie_ratio.txt', 'r') as f: self.form_settingsProperties.txt_ieratio.setValue(int(f.read()))

        with open('/home/pi/dec-rpi-gui/temp/peak_flow.txt', 'r') as f: self.form_settingsProperties.txt_flow.setValue(int(f.read()))

        with open('/home/pi/dec-rpi-gui/temp/peep.txt', 'r') as f: self.form_settingsProperties.txt_peep.setValue(int(f.read()))

        with open('/home/pi/dec-rpi-gui/temp/fio2.txt', 'r') as f: self.form_settingsProperties.txt_fio2.setValue(int(f.read()))

        self.window.show()

    def save_settings(self):
        mode = str(self.form_settingsProperties.cmb_mode.currentText()).lower()
        volume = str(self.form_settingsProperties.txt_volume.text()).replace('mL', '')
        resp_rate = str(self.form_settingsProperties.txt_resp_rate.text()).replace(' Breath/min', '')
        ieratio = str(self.form_settingsProperties.txt_ieratio.text())
        flow = str(self.form_settingsProperties.txt_flow.text()).replace(' Lpm', '')
        peep = str(self.form_settingsProperties.txt_peep.text())
        fio2 = str(self.form_settingsProperties.txt_fio2.text()).replace('%', '')

        with open('/home/pi/dec-rpi-gui/temp/mode.txt', 'w') as f: f.write(mode)

        with open('/home/pi/dec-rpi-gui/temp/tidal_volume.txt', 'w') as f: f.write(volume)

        with open('/home/pi/dec-rpi-gui/temp/resp_rate.txt', 'w') as f: f.write(resp_rate)

        with open('/home/pi/dec-rpi-gui/temp/ie_ratio.txt', 'w') as f: f.write(ieratio)

        with open('/home/pi/dec-rpi-gui/temp/peak_flow.txt', 'w') as f: f.write(flow)

        with open('/home/pi/dec-rpi-gui/temp/peep.txt', 'w') as f: f.write(peep)

        with open('/home/pi/dec-rpi-gui/temp/fio2.txt', 'w') as f: f.write(fio2)

        self.refresh_display()
        self.window.close()

    def refresh_display(self):
        with open('/home/pi/dec-rpi-gui/temp/mode.txt', 'r') as f: self.lbl_mode.setText(f.read().title())

        with open('/home/pi/dec-rpi-gui/temp/tidal_volume.txt', 'r') as f: self.lbl_tidal_volume.setText(f'{f.read()} mL')

        with open('/home/pi/dec-rpi-gui/temp/resp_rate.txt', 'r') as f: self.lbl_resp_rate.setText(f'{f.read()} BPM')

        with open('/home/pi/dec-rpi-gui/temp/ie_ratio.txt', 'r') as f: self.lbl_ieratio.setText(f'1:{f.read()}')

        with open('/home/pi/dec-rpi-gui/temp/peak_flow.txt', 'r') as f: self.lbl_flow.setText(f'{f.read()} Lpm')

        with open('/home/pi/dec-rpi-gui/temp/peep.txt', 'r') as f: self.lbl_peep.setText(f'{f.read()} cmH2O')

        with open('/home/pi/dec-rpi-gui/temp/fio2.txt', 'r') as f: self.lbl_fio2.setText(f'{f.read()}%')

        with open('/home/pi/dec-rpi-gui/temp/pressure_peak.txt', 'r') as f: self.lbl_pressure_peak.setText(f'{f.read()} cmH2O')

        with open('/home/pi/dec-rpi-gui/temp/p_plateau.txt', 'r') as f: self.lbl_p_plateau.setText(f'{f.read()} cmH2O')
        
    @pyqtSlot(list)
    def pressure_listener(self, pressure_stack):
        self.gv_pressure.clear()
        self.gv_pressure.plot(pressure_stack)

    @pyqtSlot(list)
    def flow_listener(self, flow_stack):
        self.gv_flow.clear()
        self.gv_flow.plot(flow_stack)

    @pyqtSlot(list)
    def volume_listener(self, volume_stack):
        self.gv_volume.clear()
        self.gv_volume.plot(volume_stack)

    def closeEvent(self, event):
        for process in self.process_pool:
            process.stop()
            time.sleep(1)
        
        time.sleep(1)

app = QtWidgets.QApplication([])
application = Main()
application.show()
sys.exit(app.exec_())
