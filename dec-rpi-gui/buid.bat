@echo off
title DEC RPI GUI BUILD
pyuic5 ui\splashscreen.ui -o splashscreen.py
pyuic5 ui\dashboard.ui -o dashboard.py
pyuic5 ui\settings.ui -o settings.py
pyrcc5 src\images.qrc -o images_rc.py