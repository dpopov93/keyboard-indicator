#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''

This Ubuntu Unity indicator for keyboard 
leds Caps Lock and Numeric pad

# Main module

Author: Denis Popov
E-mail: spidermind93@gmail.com
Created: 27.11.2017

'''

import os, time, subprocess, threading, gi, conflibsaver, keybd_settings as _kbds

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')

from gi.repository import Gtk, Gio, AppIndicator3, Notify

APPINDICATOR_ID_CAPS = 'caps_app_indicator'
APPINDICATOR_ID_NUM = 'num_app_indicator'

img_caps_off = os.path.abspath('caps_off.svg')
img_caps_on = os.path.abspath('caps_on.svg')
img_num_off = os.path.abspath('num_off.svg')
img_num_on = os.path.abspath('num_on.svg')

class KeyboardDaemon(threading.Thread):
	def run(self):
		self.alive = True
		self.daemon = True

		while self.alive:
			Application.set_icon_by_state(subprocess.getoutput('xset q | grep LED')[65])
			time.sleep(0.1)

	def stop(self):
		self.alive = False
		self.stopped = True

class Application(Gtk.Application):
	
	def __init__(self):
		Gtk.Application.__init__(self,
		flags=Gio.ApplicationFlags.FLAGS_NONE)
		self.settings = _kbds.ProgramSettings()

		self.license_type = Gtk.License.GPL_3_0

	def do_activate(self):
		#TODO: Check for settings of notify
		
		Notify.init('keyboard_indicator')
		if self.settings.get_option_state():
			Notify.Notification.new('Keyboard Indicator', "Keyboard indicator is running\nLed status on your panel", os.path.abspath('iconApp.svg')).show()
			
		global daemon_led
		daemon_led = KeyboardDaemon()
		
		global indicator_caps, indicator_num
		
		indicator_caps = AppIndicator3.Indicator.new(APPINDICATOR_ID_CAPS, img_caps_off, AppIndicator3.IndicatorCategory.SYSTEM_SERVICES)
		indicator_caps.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
		indicator_caps.set_menu(self.p_menu())
	
		indicator_num = AppIndicator3.Indicator.new(APPINDICATOR_ID_NUM, img_num_off, AppIndicator3.IndicatorCategory.SYSTEM_SERVICES)
		indicator_num.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
		indicator_num.set_menu(self.p_menu())
	
		threading.Thread(target=Gtk.main).start()
		threading.Thread(target=daemon_led.run).start()
		
	def p_menu(self):
		self.menu = Gtk.Menu()
	
		self.item_settings = Gtk.MenuItem('Settings')
		self.item_quit = Gtk.MenuItem('Quit')
	
		self.item_settings.connect('activate', self.open_settings_window)
		self.item_quit.connect('activate', self.on_quit)
	
		self.menu.append(self.item_settings)
		self.menu.append(self.item_quit)
		self.menu.show_all()
	
		return self.menu

	def set_icon_by_state(state):
		global indicator_caps, indicator_num
		
		if (state == '0'):
			indicator_caps.set_icon(img_caps_off)
			indicator_num.set_icon(img_num_off)
		elif (state == '1'):
			indicator_caps.set_icon(img_caps_on)
			indicator_num.set_icon(img_num_off)
		elif (state == '2'):
			indicator_caps.set_icon(img_caps_off)
			indicator_num.set_icon(img_num_on)
		elif (state == '3'):
			indicator_caps.set_icon(img_caps_on)
			indicator_num.set_icon(img_num_on)

	def open_settings_window(self, widget):
		self.window = _kbds.SettingsWindow()
		self.window.show_all()

	def do_startup(self):
		Gtk.Application.do_startup(self)

	def do_shutdown(self):
		Gtk.Application.do_shutdown(self)

	def on_quit(self, widget):
		daemon_led.stop()
		Notify.uninit()
		Gtk.main_quit()
		self.quit()

if __name__ == '__main__':
	application = Application()
	application.run(None)
