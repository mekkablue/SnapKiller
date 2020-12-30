# encoding: utf-8

###########################################################################################################
#
#
#	General Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/General%20Plugin
#
#
###########################################################################################################

from __future__ import division, print_function, unicode_literals
import objc
from GlyphsApp import *
from GlyphsApp.plugins import *

class SnapKiller(GeneralPlugin):
	
	@objc.python_method
	def settings(self):
		self.name = Glyphs.localize({
			'en': u'Kill Snapping', 
			'de': u'Einrasten unterdrücken',
			'es': u'Evitar magnetismo entre los nodos',
		})
	
	@objc.python_method
	def start(self):
		self.isKilling = False
		self.hasNotification = False
		
		Glyphs.registerDefault("com.mekkablue.SnapKiller.state", False)

		self.menuItem = NSMenuItem(self.name, self.toggleSnapKill)
		Glyphs.menu[EDIT_MENU].append(self.menuItem)
		
		self.setSnapKillState(self.getSnapKillState())
	
	@objc.python_method
	def __del__(self):
		try:
			if self.hasNotification:
				Glyphs.removeCallback(self.killSnaps, DRAWFOREGROUND)
				self.hasNotification = False
		except:
			# exit gracefully, but do report:
			import traceback
			print( traceback.format_exc() )
	
	@objc.python_method
	def toggleSnapKill(self, sender):
		self.setSnapKillState(not self.getSnapKillState())
	
	@objc.python_method
	def getSnapKillState(self):
		return Glyphs.boolDefaults["com.mekkablue.SnapKiller.state"]
	
	@objc.python_method
	def setSnapKillState(self, state):
		Glyphs.boolDefaults["com.mekkablue.SnapKiller.state"] = bool(state)
		if not state:
			if self.hasNotification:
				Glyphs.removeCallback(self.killSnaps, DRAWFOREGROUND)
				self.hasNotification = False
		else:
			if not self.hasNotification:
				Glyphs.addCallback(self.killSnaps, DRAWFOREGROUND)
				self.hasNotification = True
		
		currentState = ONSTATE if state else OFFSTATE
		self.menuItem.setState_(currentState)
	
	@objc.python_method
	def killSnaps(self, sender, blackAndScale=None):
		# only kill snaps when a document and a tab is open and a glyph layer is open for editing:
		if Glyphs.font and Glyphs.font.currentTab and Glyphs.font.currentTab.activeLayer():
			tool = Glyphs.currentDocument.windowController().toolEventHandler()
			toolCanSnap = tool.respondsToSelector_("cleanSnappers")
			if toolCanSnap and not self.isKilling:
				self.isKilling = True
				tool.cleanSnappers()
				self.isKilling = False
	
	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
	