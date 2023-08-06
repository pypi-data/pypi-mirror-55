# Version : 2.0.0
# Author : LiuWei
# Date : 2019.11.07

#!/user/bin/python
#-*- coding:uft-8 -*-

from gameutils import print_bold

class Hut:
	def __init__(self,number,occupant):
		self.occupant = occupant
		self.number = number
		self.is_acquired = False

	def acquire(self,new_occupant):
		self.occupant = new_occupant
		self.is_acquired = True
		print_bold('Good job! Hut %d acquired!'%self.number)

	def get_occupant_type(self):
		if self.is_acquired:
			occupant_type = 'Acquired'
		elif self.occupant is None:
			occupant_type = 'Unoccupied'
		else:
			occupant_type = self.occupant.unit_type
		return occupant_type