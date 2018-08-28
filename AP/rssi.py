import socket
import os

#iw dev wlan0 station dump

def giveAlert(str_error):
    list_command = {'status': 'Help > Check your interface status'}
    print list_command[str_error]

def sendRSSI(str_host, CONST_INT_PORT):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((str_host, CONST_INT_PORT))
    file_in, file_out, file_error = os.popen3('iw dev wlan0 station dump')
    if file_error.read():
        giveAlert('status')
    else:
        print 'hello'
    s.sendall("Hello\n")
    s.close()
