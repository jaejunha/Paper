import socket

#iwlist wlan0 scan

host = 'localhost'
port = 7777
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

s.sendall("Hello\n")
s.close()
