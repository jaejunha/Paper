import numpy as np
import random

from simulation import Simulation

SIZE_EPISODE = 100
SIZE_ACTION = 3
SIZE_STATE = 3

def start():
	network = Simulation()
	
	epsilon = 1.0
	time_step = 0
	for episode in range(SIZE_EPISODE):
		gameover = False
		total_reward = 0
		time_step = 0

		state = network.reset()
		"""
		#bot.initState(state)
		"""
		while not gameover:

			if np.random.rand() < epsilon:
				action = random.randrange(SIZE_ACTION)
			else:
				max_Q = 0
				max_action = 0
				for a in range(SIZE_ACTION):
					if Q_table[state][a] > max_Q:
						max_Q = Q_table[state][a]
						max_action = a
				action = max_action
			
			# 시간 지날 수록 입실론 값 줄이기
			epsilon -= 1 / SIZE_EPISODE

			# action에 따라 state 이동
			state, reward, gameover = network.step(action)
			total_reward += reward

			# Q-table에 값 저장
			Q_table[state][action] = reward
			# 감마함수, 이전 스테이트와 action 고려 필수
			
			state = network.randomize()
			
			time_step += 1
			if total_reward >= 10:
				gameover = True
		print('에피소드: %d 게임횟수: %d 점수: %d' % (episode + 1, time_step, total_reward))