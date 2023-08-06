# Version : 2.0.0
# Author : LiuWei
# Date : 2019.11.07

#!/user/bin/python
#-*- coding:uft-8 -*-

import random
from hut import Hut
from knight import Knight
from orcrider import OrcRider
from gameutils import print_bold,print_dotted_line

class AttackOfTheOrcs:
	def __init__(self):
		self.huts = []
		self.player = None

	def get_occupants(self):
		return [x.get_occupant_type() for x in self.huts]

	def show_game_mission(self):
		print_bold('Mission:')
		print('  1.Fight with the enemy.')
		print('  2.Bring all the huts in the village under you control.')
		print_dotted_line()

	def _process_user_choice(self):
		verifying_choice = True
		idx = 0
		print('Current occupants : %s'%self.get_occupants())
		while verifying_choice:
			user_choice = input('Choose a hut number to enter(1-5) :')
			try:
				idx = int(user_choice)
			except ValueError as e:
				print('Invalid input,args:%s\n'%e.args)
				continue
			try:
				if self.huts[idx-1].is_acquired:
					print('You have already acquired this hut. Try again.'
					'<INFO: You can Not get healed in already acquired hut.>')
				else:
					verifying_choice = False
			except IndexError:
				print('Invalid input:',idx)
				print('Number should be in the range 1-5. Try again')
				continue
		return idx

	def _occupy_huts(self):
		for i in range(5):
			choice_list = ['enemy','friend',None]
			computer_choice = random.choice(choice_list)
			if computer_choice == 'enemy':
				name = 'enemy' + str(i+1)
				self.huts.append(Hut(i+1,OrcRider(name)))
			elif computer_choice == 'friend':
				name = 'Knight' + str(i+1)
				self.huts.append(Hut(i+1,Knight(name)))
			else:
				self.huts.append(Hut(i+1,computer_choice))

	def play(self):
		self.palyer = Knight()
		self._occupy_huts()
		acquired_hut_counter = 0
		self.show_game_mission()
		self.palyer.show_health(bold=True)
		while acquired_hut_counter < 5:
			idx = self._process_user_choice()
			self.palyer.acquire_hut(self.huts[idx-1])
			if self.palyer.health_meter <= 0:
				print_bold('You lose : (Better luck next time).')
				break
			if self.huts[idx-1].is_acquired:
				acquired_hut_counter += 1
		if acquired_hut_counter == 5:
			print_bold('Congratulations! You win!!!')

if __name__ == '__main__':
	game = AttackOfTheOrcs()
	game.play()