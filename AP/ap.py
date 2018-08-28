import sys

import rssi as RSSI

CONST_INT_PORT = 7777

def checkIP():
    list_ip = sys.argv[1].split('.')
    if len(list_ip) < 4:
        return False
    try:
        for str_ip in list_ip:
            int_ip = int(str_ip)
            if int_ip > 255 or int_ip < 0:
                return False
    except:
        return False
    return True

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print 'Help > python ap.py <Server IP>'
    else:
        if checkIP() == False:
            print 'Help > Check Server IP'
        else:
            RSSI.sendRSSI(sys.argv[1], CONST_INT_PORT)
