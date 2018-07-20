import sys

import help as Help
import ap as AP

def treatError():
	if sys.argv[1] == 'change':
		AP.giveAlert('arg')
	else:
		Help.giveAlert()	

def parseMenu():
	try:
		if sys.argv[1] == 'help':
	         	Help.giveHelp()
                elif sys.argv[1] == 'iface':
                        AP.getInterface()
                elif sys.argv[1] == 'scan':
                        AP.scanESSID()
        	elif sys.argv[1] == 'change':
			if len(sys.argv) > 3:
                		AP.changeESSID(sys.argv[2], sys.argv[3])
			else:
				AP.changeESSID(sys.argv[2], '')
		else:
			treatError()
	except IndexError:
		treatError()
	except TypeError:
		pass

if __name__ == '__main__':
	if len(sys.argv) == 1:
		Help.giveAlert()
	else:
		parseMenu()
