import tensorflow as tf

def start():
	print("hello")
	sess = tf.Session()

	#call Network
	#call DQN model
	
	saver = tf.train.Saver()
	ckpt = tf.train.get_checkpoint_state("model")
	saver.restore(sess, ckpt.model_checkpoint_path)