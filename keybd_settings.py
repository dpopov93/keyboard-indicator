#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''

This Ubuntu Unity indicator for keyboard 
leds Caps Lock and Numeric pad

# Settings module

Author: Denis Popov
E-mail: spidermind93@gmail.com
Created: 27.11.2017

'''

import sys, gi, os, conflibsaver, time

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gio, GdkPixbuf

class ProgramSettings() :
	def __init__(self):		
		self.conf_file_path = ('/home/denis/.config/keybd-indicator/keybd_indicator.conf')
		self.param_name = 'message_display'
		
		if conflibsaver.has_param(self.conf_file_path, self.param_name) in [None, False] : self.create_settings()
		
	def get_option_state(self):
		state = conflibsaver.str2bool(conflibsaver.get_param(self.conf_file_path, self.param_name))
		if state != None : return state
		else :
			self.create_settings()
			return True
		
	def create_settings(self):
		conflibsaver.create_file(self.conf_file_path, self.param_name + ' = ' + 'True')

	def set_option_state(self, state):
		conflibsaver.set_param(self.conf_file_path, self.param_name, str(state))

class SettingsWindow(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self)
		self.settings = ProgramSettings()
		
		self.set_title('Settings')
		self.set_position(Gtk.WindowPosition.CENTER)
		
		pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(filename = "iconApp.svg", width = 256, height = 256, preserve_aspect_ratio = True)
		image1 = Gtk.Image.new_from_pixbuf(pixbuf)
		
		label_about = Gtk.Label()
		label_about.set_text('Description about program.\nThis Application for bla-bla and qua-qua.\nAuthor: Denis Popov\nE-mail: spidermind93@gmail.com')
		
		self.display_message_at_startup = Gtk.CheckButton("Display message when indicator is startup")
		self.display_message_at_startup.connect('toggled', self.on_chk_btn_state_change)
		if self.settings.get_option_state() : self.display_message_at_startup.set_active(True)
		
		btn_close = Gtk.Button(label = 'Close')
		btn_close.connect('clicked', lambda wnd: self.close())
		
		content = Gtk.VBox(margin=10)
		widgets_container = Gtk.VBox()
		button_box = Gtk.HBox(halign = Gtk.Align.END)
		
		widgets_container.pack_start(image1, expand = True, fill = True, padding = 0)
		widgets_container.pack_start(label_about, expand = True, fill = True, padding = 5)
		widgets_container.pack_start(self.display_message_at_startup, expand = True, fill = True, padding = 2)
		
		button_box.pack_start(btn_close, expand = False, fill = True, padding = 0)
		
		content.add(widgets_container)
		content.add(button_box)
		
		self.add(content)
		self.show_all()
	
	def on_chk_btn_state_change(self, widget):
		if self.display_message_at_startup.get_active() : self.settings.set_option_state(True)
		else : self.settings.set_option_state(False)
		

if __name__ == '__main__':
	sys.stderr.write('Error: program must be run from main file...\n')
	sys.exit(1)
