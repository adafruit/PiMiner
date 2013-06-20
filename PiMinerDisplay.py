#!/usr/bin/python

from PiMinerInfo import PiMinerInfo
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate

class PiMinerDisplay:
  
	col = []	
	prevCol = 0  
	lcd = Adafruit_CharLCDPlate()
	info = PiMinerInfo()
	mode = 1
	offset = 0
	maxOffset = 0
	screen = []	
	
	def __init__(self):
		self.lcd.clear()
		self.col = (self.lcd.ON,   self.lcd.OFF, self.lcd.YELLOW, self.lcd.OFF,
	                self.lcd.GREEN, self.lcd.OFF, self.lcd.TEAL,   self.lcd.OFF,
        	        self.lcd.BLUE,  self.lcd.OFF, self.lcd.VIOLET, self.lcd.OFF,
                	self.lcd.RED,    self.lcd.OFF)
		self.lcd.backlight(self.col[self.prevCol])
		
	#Display Local Info - Accepted, Rejected, HW Errors \n Average Hashrate
	def dispLocalInfo(self):
		self.dispScreen(self.info.screen1)

	#Display Secondary info 1 - Pool Name \n Remote hashrate
	def dispPoolInfo(self):
		self.dispScreen(self.info.screen2)

	#Display Secondary info 2 - Rewards (confirmed + unconfirmed) \n Current Hash
	def dispRewardsInfo(self):
        	self.dispScreen(self.info.screen3)
	
	#Send text to display
	def dispScreen(self, newScreen):
		self.screen = newScreen
		self.maxOffset = max((len(self.screen[0]) - 16), (len(self.screen[1]) - 16))
		self.lcd.clear()
                s = self.screen[0] + '\n' + self.screen[1]
                self.lcd.message(s)

	#Cycle Backlight Color / On/Off
	def backlightStep(self):
		if self.prevCol is (len(self.col) -1): self.prevCol = -1
          	newCol = self.prevCol + 1
          	self.lcd.backlight(self.col[newCol])
          	self.prevCol = newCol
	
	def scrollLeft(self):
		if self.offset >= self.maxOffset: return
		self.lcd.scrollDisplayLeft()
		self.offset += 1

	def scrollRight(self):
		if self.offset <= 0: return
		self.lcd.scrollDisplayRight()
		self.offset -= 1
		
	def modeUp(self):
		self.mode += 1
		if self.mode > 2: self.mode = 0
		self.update()

	def modeDown(self):
		self.mode -= 1
                if self.mode < 0: self.mode = 2
                self.update()

	def update(self):
		self.info.refresh()
                if self.mode == 0: self.dispPoolInfo()
                elif self.mode == 1: self.dispLocalInfo()
                elif self.mode == 2: self.dispRewardsInfo()
		
