#!/usr/bin/python

import sys
sys.path.append("/home/pi/Adafruit-Raspberry-Pi-Python-Code/Adafruit_CharLCDPlate")

from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
from PiMinerDisplay import PiMinerDisplay
from time import time

lcd = Adafruit_CharLCDPlate()
pDisplay = PiMinerDisplay()
prevCol = -1
prev = -1
lastTime = time()

pDisplay.dispLocalInfo()

# Listen for button presses
while True:
  b = lcd.buttons()
	if b is not prev:
		if lcd.buttonPressed(lcd.SELECT):
			pDisplay.backlightStep()
        	elif lcd.buttonPressed(lcd.LEFT):
	  		pDisplay.scrollRight()
        	elif lcd.buttonPressed(lcd.RIGHT):
          		pDisplay.scrollLeft()
		elif lcd.buttonPressed(lcd.UP):
                        pDisplay.modeUp()
		elif lcd.buttonPressed(lcd.DOWN):
                        pDisplay.modeDown()
		prev = b
		lastTime = time()
	else:
		now = time()
		since = now - lastTime
		if since > 4.0 or since < 0.0:
			pDisplay.update()
			lastTime = now
