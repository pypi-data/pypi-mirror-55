#!/usr/bin/python3           # This is server.py file
import socket
import json
import time

import ssl

def loaded():
    print("Module loaded correctly.")

def recieve(host, port):
   banner = "###### MPI PROTOCOL ######"
   message = ""
   print("[INFO] [MPI] Creating socket")
   serversocket = socket.socket(
                   socket.AF_INET, socket.SOCK_STREAM) 
   # bind to the port
   serversocket.bind((host, port))                                  
   serversocket = ssl.wrap_socket(serversocket, ssl_version=ssl.PROTOCOL_TLS, ciphers="ADH-AES256-SHA")
   # queue up to 5 requests
   serversocket.listen(5)

   # establish a connection
   clientsocket,addr = serversocket.accept()

   print("[INFO] [MPI] Got a connection from %s" % str(addr))
   print("[INFO] [MPI] Staring Handshake")
   msg = clientsocket.recv(1024)                                     
   if msg.decode('ascii') != "GREET":
      print("[ERROR] [MPI] Handshake not successful")
      clientsocket.close()
   else:
      clientsocket.send("GREET".encode('ascii'))
      print("[INFO] [MPI] Receiving data")
      msg = clientsocket.recv(1024)
      #clientsocket.send(msg.encode('ascii'))
      clientsocket.close()
      print("[INFO] [MPI] Closing socket")
      

   return msg.decode('ascii')

def send(host, port, message):
    banner = "###### MPI PROTOCOL ######"
    print("[INFO] [MPI] Creating socket")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    # connection to hostname on the port.
    try:
        s.connect((host, port))
    except:
        print("[ERROR] [MPI] Could not connect to master node")

    # Receive no more than 1024 bytes

    print("[INFO] [MPI] Starting Handshake")
    msg = "GREET"
    s.send(msg.encode('ascii'))    
    msg = s.recv(1024)                                     
    if msg.decode('ascii') != "GREET":
        print("[ERROR] [MPI] Handshake not successful")
        s.close()      
    else:
        print("[INFO] [MPI] Handshake successful")
        print("[INFO] [MPI] Sending data")
        s.send(message.encode('ascii'))
        #print(s.recv(1024))
        s.close()
        print("[INFO] [MPI] Closing socket")



def request(host, port, target):
   mpi_send(host, port, "rqst mf")
   data_string = mpi_recieve(host, port)
   machinefile = json.loads(data_string)
   meta = []
   for each in target:
      meta.append(machinefile["vars"][each])
   return(meta)
   
def export(host, port, key_values_dict):
   mpi_send(host, port, "rqst mf")
   data_string = mpi_recieve(host, port)
   machinefile = json.loads(data_string)
   machinefile["vars"].update(key_values_dict)
   mpi_send(host, port, "expt mf")
   serve(machinefile, host, port)
   return machinefile

def serve(MachineFile, host, port):
   data_string = json.dumps(MachineFile)
   mpi_send(host, port, data_string)

def multiplexer(MachineFile, host, port):
   comm = mpi_recieve(host, port)
   if comm == "rqst mf":
      serve(MachineFile, host, port)
      return MachineFile
   elif comm == "expt mf":
      MachineFile = mpi_recieve(host, port)
      #serve(MachineFile, host, port)
      return MachineFile
   else:
      return 1

"""
A -> quer a var B1
         -> Procurar no machine file


"""
