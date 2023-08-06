# Version : 2.0.0
# Author : LiuWei
# Date : 2019.11.07

#!/user/bin/python
#-*- coding:uft-8 -*-

from abstractgameunit import AbstractGameUnit
from gameutils import print_bold

class Knight(AbstractGameUnit):
	def __init__(self,name = 'Sir Foo'):
		super().__init__(name = name)
		self.max_hp = 40
		self.health_meter = self.max_hp
		self.unit_type = 'friend'

	def info(self):
		print('I am a Knight!')

	def acquire_hut(self,hut):
		print_bold('Entering hut %d...'%hut.number,end = ' ')
		is_enemy = (isinstance(hut.occupant,AbstractGameUnit)) and hut.occupant.unit_type == 'enemy'
		continue_attack = 'y'
		if is_enemy:
			print_bold('Enemy sighted!')
			self.show_health(bold=True,end=' ')
			while continue_attack:
				continue_attack = input('.......continue attack?(y/n) :')
				if continue_attack == 'n':
					self.run_away()
					break
				self.attack(hut.occupant)
				if hut.occupant.health_meter <= 0:
					print('')
					hut.acquire(self)
					break
				if self.health_meter <= 0:
					print('')
					break
		else:
			if hut.get_occupant_type() == 'unoccupied':
				print_bold('Hut is unoccupied.')
			else:
				print_bold('Friend sighted!')
			hut.acquire(self)
			self.heal()

	def run_away(self):
		print_bold('Running away...')
		self.enemy = None