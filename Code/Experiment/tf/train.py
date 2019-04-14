import tensorflow as tf

def start():
	print("hello")
	sess = tf.Session()

	#call Network
	#call DQN model
	
	saver = tf.train.Saver()
	saver.save(sess, 'model/dqn.ckpt', global_step=time_step)