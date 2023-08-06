# Version : 2.0.0
# Author : LiuWei
# Date : 2019.11.06

#!/user/bin/python
#-*- coding:uft-8 -*-

class GameUnitError(Exception):
	def __init__(self,message = ''):
		super().__init__(message)
		self.padding = '~'*50 + '\n'
		self.error_message = 'Unspecified Error!'

class  HealthMeterException(GameUnitError):
	def __init__(self,message=''):
		super().__init__(message)
		self.error_message = self.padding + 'ERROR: Health Meter Problem' + '\n' + self.padding
		