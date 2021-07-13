import socket
import time

s=socket.socket()
HOST="10.0.100.2"
PORT=6000

REQUIRED_CHARACTER="\n" #### REQUIRED FOR LOGSTASH TO TAKE EVENT SEPARATED (TCP PLUGIN)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("ok")
    i=0
    while i<50:
        time.sleep(3)
        bytes_=bytes("Hello, world"+str(i)+REQUIRED_CHARACTER,'utf-8')
        s.send(bytes_)
        i=i+1
        #data = s.recv(1024)
        #print('Received', repr(data))
    s.close()