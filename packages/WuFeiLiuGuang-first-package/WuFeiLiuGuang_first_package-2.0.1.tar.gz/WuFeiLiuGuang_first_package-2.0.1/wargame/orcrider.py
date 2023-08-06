# Version : 2.0.0
# Author : LiuWei
# Date : 2019.11.07

#!/user/bin/python
#-*- coding:uft-8 -*-

from abstractgameunit import AbstractGameUnit

class OrcRider(AbstractGameUnit):
	def __init__(self,name = ''):
		super().__init__(name = name)
		self.max_hp = 30
		self.health_meter = self.max_hp
		self.unit_type = 'enemy'
		self.hut_number = 0

	def info(self):
		print("Grrr..I am an Orc Wolf Rider. Don't mess with me.")