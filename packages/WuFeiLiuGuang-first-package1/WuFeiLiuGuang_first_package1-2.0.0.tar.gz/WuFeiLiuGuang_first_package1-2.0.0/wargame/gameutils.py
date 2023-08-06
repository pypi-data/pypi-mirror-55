# Version : 2.0.0
# Author : LiuWei
# Date : 2019.11.07

#!/user/bin/python
#-*- coding:uft-8 -*-

import random

def print_bold(msg,end='\n'):
	print('\033[1m' + msg + '\033[0m',end=end)

def print_dotted_line(width = 72):
	print('-'*width)

def weighted_random_selection(object1,object2):
	weighted_list = [id(object1)]*4 + [id(object2)]*6
	selection = random.choice(weighted_list)
	if selection == id(object1):
		return object1
	return object2