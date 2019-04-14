import sys
import train as Train
import run as Run

if __name__ == "__main__":
	if len(sys.argv) is 1:
		print("Please select the mode")
	else:
		arg = sys.argv[1]
		if arg == "train":
			print("Trainning mode")
			Train.start()
		elif arg == "run":
			print("Running mode")
			Run.start()
		else:
			print("Please choose the correct mode")