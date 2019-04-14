import tensorflow as tf
from dqn import DQN

def start():
	print("hello")
	sess = tf.Session()

	#call Network
	bot = DQN(sess)
	
	saver = tf.train.Saver()
	saver.save(sess, 'model/dqn.ckpt', global_step=time_step)