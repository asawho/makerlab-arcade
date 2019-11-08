import keyboard
import time, threading
import subprocess
import os

timeoutCleared=True
hotcombo=""
emulatorRunning=False
def stopEmulator():
	global emulatorRunning
	subprocess.run(["ps -ef | awk '/retropie/ {print $2}' | xargs kill"], shell=True)
	subprocess.run(["ps -ef | awk '/emulation/ {print $2}' | xargs kill"], shell=True)
	emulatorRunning=False
def startEmulator():
	global emulatorRunning
	subprocess.Popen(['sudo','-u','pi','emulationstation'])
	emulatorRunning=True
def stopKiosk():
	subprocess.run(["sudo /etc/init.d/lightdm stop"],shell=True)
def startKiosk():
	subprocess.run(["sudo /etc/init.d/lightdm start"],shell=True)

def checkTimeout():
	global timeoutCleared
	global emulation
	global emulatorRunning
	if not timeoutCleared and emulatorRunning:
		stopEmulator()
		startKiosk()
		#subprocess.run(["sudo chvt 7"],shell=True)
	timeoutCleared=False
	threading.Timer(60, checkTimeout).start()

def key_press(key):
	global timeoutCleared
	global hotcombo
	timeoutCleared=True
	hotcombo=(hotcombo+key.name)[-10:]
	if hotcombo[-4:]=="beer":
		subprocess.run(["aplay cantdo.wav"],shell=True)
	if hotcombo[-4:]=="soda":
		subprocess.run(["aplay difficult.wav"],shell=True)
	if key.name=='1':
		stopKiosk()
		startEmulator()
	if key.name=='2':
		stopEmulator()
		startKiosk()
		#subprocess.run(["sudo chvt 7"],shell=True)
	if key.name=='z':
		subprocess.run(["sudo shutdown -h now"],shell=True)	


startKiosk()
keyboard.on_press(key_press)
checkTimeout()
#subprocess.run(["sudo chvt 7"],shell=True)
keyboard.wait()
