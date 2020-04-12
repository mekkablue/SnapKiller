# encoding: utf-8
from __future__ import division, print_function, unicode_literals

###########################################################################################################
#
#	General Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/General%20Plugin
#
###########################################################################################################

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
		Glyphs.registerDefault("com.mekkablue.SnapKiller.state", False)
		self.isKilling = False
		self.hasNotification = False
		
		# add menu item:
		self.menuItem = NSMenuItem(self.name, self.toggleSnapKillState_)
		Glyphs.menu[EDIT_MENU].append(self.menuItem)
		self.setSnapKillingToState(Glyphs.boolDefaults["com.mekkablue.SnapKiller.state"])
	
	@objc.python_method
	def __del__(self):
		try:
			if self.hasNotification:
				Glyphs.removeCallback(self.killSnaps_, DRAWFOREGROUND)
				self.hasNotification = False
		except:
			# exit gracefully, but do report:
			import traceback
			print(traceback.format_exc())
	
	def toggleSnapKillState_(self, sender):
		self.setSnapKillingToState(not Glyphs.boolDefaults["com.mekkablue.SnapKiller.state"])
	
	@objc.python_method
	def setSnapKillingToState(self, state):
		# make sure the pref is set:
		Glyphs.boolDefaults["com.mekkablue.SnapKiller.state"] = bool(state)

		# add or remove the callback:
		if not state:
			if self.hasNotification:
				Glyphs.removeCallback(self.killSnaps_, DRAWFOREGROUND)
				self.hasNotification = False
		else:
			if not self.hasNotification:
				Glyphs.addCallback(self.killSnaps_, DRAWFOREGROUND)
				self.hasNotification = True
		
		# set menu state (check mark):
		currentState = ONSTATE if state else OFFSTATE
		self.menuItem.setState_(currentState)
	
	def killSnaps_(self, notification):
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
	