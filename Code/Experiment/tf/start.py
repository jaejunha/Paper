import sys

if __name__ == "__main__":
	if len(sys.argv) is 1:
		print("Please select the mode")
	else:
		arg = sys.argv[1]
		if arg == "train":
			print("Trainning mode")
		elif arg == "run":
			print("Running mode")
		else:
			print("Please choose the correct mode")