import random
import numpy as np

class Simulation:
	def __init__(self):
	
		self.reward = 0.
		self.total_game = 0

	def _getState(self):
		#state = np.zeros((1, 1))
		state = self.enemy

		return state

	def reset(self):
		self.reward = 0
		self.total_game += 1

		self.me = 0
		self.enemy = random.randrange(0, 3)

		return self._getState()

	def step(self, action):

		# 가위 바위 보 게임인데 상대가 낸 것을 보고 결정하는? 게임으로 테스트
		self.me = action

		# 이김
		if (self.me == 2 and self.enemy == 1) or (self.me == 1 and self.enemy == 0) or (self.me == 0 and self.enemy == 2):
			self.reward = 2
			gameover = False
		# 비김
		elif (self.me == 2 and self.enemy == 2) or (self.me == 1 and self.enemy == 1) or (self.me == 0 and self.enemy == 0):
			self.reward = 1
			gameover = False

		# 짐
		else:
			gameover = True

    
		return self._getState(), self.reward, gameover

	def randomize(self):
		self.enemy = random.randrange(0, 3)
		
		return self._getState()