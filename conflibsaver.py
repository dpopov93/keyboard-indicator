#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Configuration saver library, easy create, 
edit and using library for your program
setting manipulation

Author: Denis Popov
E-mail: spidermind93@gmail.com
Created: 30.11.2017
Version: 0.1a

'''

import os

def str2bool(string) :
	try :
		if string.lower() == 'true' : return True
		elif string.lower() == 'false' : return False
	except AttributeError : 
		return None

def create_file(path_to_file, string_config = 'None', display_messages = False) :
	try :
		with open(path_to_file, 'w') as f:
			f.write(string_config)
	except IOError :
		if display_messages == True : print('IOError: Perhaps path to file is not found. Try to create...')
		create_path_to_file(path_to_file)

def create_path_to_file(path_to_file, string_config = 'None', display_messages = False) :
	tmp_addr = ''
	for dirs in os.path.realpath(path_to_file).split('/') [1:-1] :
		tmp_addr += '/' + dirs
		if os.path.exists(tmp_addr) != True :
			try :
				os.makedirs(tmp_addr)
			except FileExistsError :
				if display_messages == True : print('Error: directory is exists')
			create_file(path_to_file, string_config)

def read_file(path_to_file, string_config = 'None', display_messages = False) :
	data = None
	try :
		with open(path_to_file, 'r') as f :
			data = f.read().split()
	except FileNotFoundError :
		if display_messages == True :
			while True :
				answer = input ('FileNotFoundError: configuration file is not exists. Create new file? (y / n): ')
				if answer.lower() not in ('y', 'n', 'yes', 'no') :
					print('Answer is wrong... Try "y" or "n"')
				else :
					if answer.lower() in ('y', 'yes') : create_file(path_to_file, string_config)
	else :
		if len(data) < 3 : data = ['None']
	finally :
		return data

def param_count(path_to_file) :
	try :
		return len(read_file(path_to_file)) // 3
	except ZeroDivisionError :
		print('Error: file is epmty!')
		return 0
	except :
		print('Error reading file')
		return 0

def data_to_string(data) :
	complete_string = ''
	
	for x in range (0, len(data) // 3) :
		for y in range (0, 3) :
			complete_string += data[x*3+y] + ' '
		complete_string += '\n'
	
	return complete_string

def set_param(path_to_file, param_name, param_value) :
	param_is_exists = has_param(path_to_file, param_name)
	if param_is_exists == None : return None
	else :
		data = read_file(path_to_file)
	
		if data == None :
			data = [param_name, '=', param_value]
		else :
			if len(data) >= 3 :
				if param_is_exists :
					for index, item in enumerate(data) :
						if item == param_name :
							data[index+2] = param_value
				else :
					data += [param_name, '=', param_value]
			else :
				data = [param_name, '=', param_value]
	
		try :
			with open(path_to_file, 'w') as f :
				f.write(data_to_string(data))
		except IOError :
			print('IOError: error adding param to file')
			return False
	
		return True

def get_param(path_to_file, param_name) :
	data = read_file(path_to_file)
	
	try :
		for index, item in enumerate(data) :
			if item == param_name : return data[index+2]
	except TypeError :
		print('TypeError: data is empty')

def has_param(path_to_file, param_name) :
	data = read_file(path_to_file)
	
	if data != None and len(data) >= 3 :
		for item in data :
			if item == param_name : return True
		return False
	else : return None
