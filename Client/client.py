import sys

import help as Help

def parseMenu():
        if sys.argv[1] == 'help':
                Help.giveHelp()
	else:
		Help.giveAlert()

if __name__ == '__main__':
	if len(sys.argv) == 1:
		Help.giveAlert()
	else:
		parseMenu()
