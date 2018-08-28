import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = 'localhost'
port = 7777
s.connect((host, port))

s.sendall("Hello\n")
s.close()
