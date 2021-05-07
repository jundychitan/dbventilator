# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/settings.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(640, 500)
        MainWindow.setStyleSheet("")
        MainWindow.setDocumentMode(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.centralwidget.setStyleSheet("background-color: rgb(20, 33, 61);")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout.setHorizontalSpacing(60)
        self.formLayout.setVerticalSpacing(20)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 75 11pt \"Segoe UI\";")
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(50, -1, 50, -1)
        self.horizontalLayout.setSpacing(50)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_assist = QtWidgets.QPushButton(self.centralwidget)
        self.btn_assist.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.btn_assist.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_assist.setStyleSheet("color: rgb(0, 0, 0);\n"
"background-color: rgb(229, 229, 229);")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/buttons/img/pngfind.com-help-icon-png-6607487.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_assist.setIcon(icon)
        self.btn_assist.setIconSize(QtCore.QSize(32, 32))
        self.btn_assist.setFlat(False)
        self.btn_assist.setObjectName("btn_assist")
        self.horizontalLayout.addWidget(self.btn_assist)
        self.btn_control = QtWidgets.QPushButton(self.centralwidget)
        self.btn_control.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_control.setStyleSheet("color: rgb(0, 0, 0);\n"
"background-color: rgb(229, 229, 229);")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/buttons/img/iconfinder_intellectual-brain-intelligent-guru-sage-pundit_3790079.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_control.setIcon(icon1)
        self.btn_control.setIconSize(QtCore.QSize(32, 32))
        self.btn_control.setFlat(False)
        self.btn_control.setObjectName("btn_control")
        self.horizontalLayout.addWidget(self.btn_control)
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 75 11pt \"Segoe UI\";\n"
"margin-top: 15px;")
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.txt_tidal_volume = QtWidgets.QSpinBox(self.centralwidget)
        self.txt_tidal_volume.setMaximumSize(QtCore.QSize(16777215, 30))
        self.txt_tidal_volume.setStyleSheet("background-color: rgb(229, 229, 229);\n"
"font: 75 11pt \"Segoe UI\";")
        self.txt_tidal_volume.setFrame(False)
        self.txt_tidal_volume.setAlignment(QtCore.Qt.AlignCenter)
        self.txt_tidal_volume.setProperty("showGroupSeparator", False)
        self.txt_tidal_volume.setSuffix("")
        self.txt_tidal_volume.setMinimum(250)
        self.txt_tidal_volume.setMaximum(800)
        self.txt_tidal_volume.setObjectName("txt_tidal_volume")
        self.horizontalLayout_2.addWidget(self.txt_tidal_volume)
        self.formLayout.setLayout(1, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 75 11pt \"Segoe UI\";\n"
"margin-top: 15px;")
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.txt_resprate = QtWidgets.QSpinBox(self.centralwidget)
        self.txt_resprate.setMaximumSize(QtCore.QSize(16777215, 30))
        self.txt_resprate.setStyleSheet("background-color: rgb(229, 229, 229);\n"
"font: 75 11pt \"Segoe UI\";")
        self.txt_resprate.setAlignment(QtCore.Qt.AlignCenter)
        self.txt_resprate.setSuffix("")
        self.txt_resprate.setMinimum(10)
        self.txt_resprate.setMaximum(30)
        self.txt_resprate.setObjectName("txt_resprate")
        self.horizontalLayout_3.addWidget(self.txt_resprate)
        self.formLayout.setLayout(2, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_3)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 75 11pt \"Segoe UI\";\n"
"margin-top: 15px;")
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.txt_ieratio = QtWidgets.QSpinBox(self.centralwidget)
        self.txt_ieratio.setMaximumSize(QtCore.QSize(16777215, 30))
        self.txt_ieratio.setStyleSheet("background-color: rgb(229, 229, 229);\n"
"font: 75 11pt \"Segoe UI\";")
        self.txt_ieratio.setAlignment(QtCore.Qt.AlignCenter)
        self.txt_ieratio.setSuffix("")
        self.txt_ieratio.setMinimum(1)
        self.txt_ieratio.setMaximum(3)
        self.txt_ieratio.setObjectName("txt_ieratio")
        self.horizontalLayout_4.addWidget(self.txt_ieratio)
        self.formLayout.setLayout(3, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_4)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 75 11pt \"Segoe UI\";\n"
"margin-top: 15px;")
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.txt_peakflow = QtWidgets.QSpinBox(self.centralwidget)
        self.txt_peakflow.setMaximumSize(QtCore.QSize(16777215, 30))
        self.txt_peakflow.setStyleSheet("background-color: rgb(229, 229, 229);\n"
"font: 75 11pt \"Segoe UI\";")
        self.txt_peakflow.setAlignment(QtCore.Qt.AlignCenter)
        self.txt_peakflow.setSuffix("")
        self.txt_peakflow.setMinimum(10)
        self.txt_peakflow.setMaximum(50)
        self.txt_peakflow.setObjectName("txt_peakflow")
        self.horizontalLayout_5.addWidget(self.txt_peakflow)
        self.formLayout.setLayout(4, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_5)
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 75 11pt \"Segoe UI\";\n"
"margin-top: 15px;")
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.txt_peep = QtWidgets.QSpinBox(self.centralwidget)
        self.txt_peep.setMaximumSize(QtCore.QSize(16777215, 30))
        self.txt_peep.setStyleSheet("background-color: rgb(229, 229, 229);\n"
"font: 75 11pt \"Segoe UI\";")
        self.txt_peep.setAlignment(QtCore.Qt.AlignCenter)
        self.txt_peep.setSuffix("")
        self.txt_peep.setMaximum(20)
        self.txt_peep.setObjectName("txt_peep")
        self.horizontalLayout_6.addWidget(self.txt_peep)
        self.formLayout.setLayout(5, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_6)
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 75 11pt \"Segoe UI\";\n"
"margin-top: 15px;")
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.txt_fio2 = QtWidgets.QSpinBox(self.centralwidget)
        self.txt_fio2.setMaximumSize(QtCore.QSize(16777215, 30))
        self.txt_fio2.setStyleSheet("background-color: rgb(229, 229, 229);\n"
"font: 75 11pt \"Segoe UI\";")
        self.txt_fio2.setAlignment(QtCore.Qt.AlignCenter)
        self.txt_fio2.setSuffix("")
        self.txt_fio2.setMaximum(100)
        self.txt_fio2.setObjectName("txt_fio2")
        self.horizontalLayout_7.addWidget(self.txt_fio2)
        self.formLayout.setLayout(6, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_7)
        self.btn_save = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_save.sizePolicy().hasHeightForWidth())
        self.btn_save.setSizePolicy(sizePolicy)
        self.btn_save.setMaximumSize(QtCore.QSize(120, 64))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.btn_save.setFont(font)
        self.btn_save.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_save.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.btn_save.setAutoFillBackground(False)
        self.btn_save.setStyleSheet("color: rgb(0, 0, 0);\n"
"background-color: rgb(229, 229, 229);\n"
"border-radius: 10px;")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/buttons/img/save-48.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_save.setIcon(icon2)
        self.btn_save.setIconSize(QtCore.QSize(32, 48))
        self.btn_save.setFlat(True)
        self.btn_save.setObjectName("btn_save")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.btn_save)
        self.verticalLayout.addLayout(self.formLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Mode"))
        self.btn_assist.setText(_translate("MainWindow", "Assist"))
        self.btn_control.setText(_translate("MainWindow", "Control"))
        self.label_2.setText(_translate("MainWindow", "Tidal Volume(mL)"))
        self.label_3.setText(_translate("MainWindow", "Respiratory Rate(BPM)"))
        self.label_4.setText(_translate("MainWindow", "I:E Ratio"))
        self.txt_ieratio.setPrefix(_translate("MainWindow", "1:"))
        self.label_5.setText(_translate("MainWindow", "Peak Flow(Lpm)"))
        self.label_6.setText(_translate("MainWindow", "PEEP(cmH2O)"))
        self.label_7.setText(_translate("MainWindow", "FiO2(%)"))
        self.btn_save.setText(_translate("MainWindow", "Save Changes"))

import images_rc
