import tensorflow as tf
from dqn import DQN

def start():
	print("hello")
	sess = tf.Session()

	#call Network
	bot = DQN(sess)
	
	saver = tf.train.Saver()
	ckpt = tf.train.get_checkpoint_state("model")
	saver.restore(sess, ckpt.model_checkpoint_path)