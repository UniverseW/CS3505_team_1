#Team 1
#This is the same as server.py except it works with only one client file.
#The only changes are the turntoken no longer moves, and all
#'for i range(4)' has been changed to 'for i in range(1)
"""A simple server program that acts as half a chat program with a client.

The server listens for any connections to any clients. The server then waits for the client to send
a message to the server. The server keeps a record of all connected clients and broadcasts any message from a client to all clients.
"""      
from socket import *
from time import sleep
import _thread, sys
import json
from random import randint

#Objective: Send colour + 

class Conns: #A simple class that keeps a list of current client connections. This allows the threads, which are created by each connection, to broadcast a message to all connections.
    def __init__(self):
        self._clients= []
        self.colours=["red","green","yellow","blue"]
        self.token = 0 #the index of which player's turn it is.
    def clients(self): #returns list of client connections
        return self._clients
    def add(self,connection): #adds "connection" to the list of connections self.clients
        if len(self.clients()) <2:
            self._clients += [connection]
    def isfull(self):
        return len(self.clients()) ==2

cons = Conns() #Creates instance of class
def ConnectionHandler(connection,client_address,cons): #Handles threads created for each connection to the server.
    print('connection from', client_address)
    print("is full?")
    print(cons.isfull())
    if cons.isfull(): #If there are 4 players connected, start a game
        StartGame()
    while True:
        data = connection.recv(4096) #Get data from client
        print(data.decode())
        msg = json.loads(data.decode()) #decode and create dict from data
        if "roll" in msg: #If request for roll is sent, call rolldice() function and broadcast the dice roll.
            num = rolldice()
            data = {"Colour":msg["Colour"],"dicenum":num} 
            data = json.dumps(data)
        if "turnOver" in msg: #If a client says it's turn is finished, move the token on to the next person.
            cons.token += 1
            if cons.token >1:
                cons.token = 0
            data = {"Colour":cons.colours[cons.token],"turnToken":True}
            data = json.dumps(data)
            print("iT is now the turn of   ",cons.colours[cons.token])
        if "Sendout" in msg or "Movement" in msg: #If the JSON message is Sendout or Movement, simply forward it unchanged to all other clients.
            data = json.dumps(msg)
        for i in range(2):
            cons.clients()[i].sendall(data.encode())
            print(data)

      

        
def StartGame():
    """A function that starts the game. It assigns a colour to each client by order in which they connected, and gives the turn token to the red player"""
    start = [{"Colour":"red","start":True},{"Colour":"green","start":True},{"Colour":"yellow","start":True},{"Colour":"blue","start":True}]
    for i in range (2):
        start[i] = json.dumps(start[i])
    for i in range(2):
        cons.clients()[i].sendall(start[i].encode())
        print("sent start to ",i)
    sleep(3)
    token =json.dumps({"Colour":"red","turnToken":True})
    for i in range(2):
        cons.clients()[i].sendall(token.encode())
        
    
def rolldice():
    """Returns a random number between 1 and 6"""
    return randint(4,6)
    #return 6

    

if __name__ == "__main__":#If this file is being executed as the top layer, start the server.
    try:
        sock = socket(AF_INET, SOCK_STREAM) #Creates TCP server socket.        
        ipaddr = gethostbyname(gethostname()) # IP Address of the current machine.
        server_address = (ipaddr, 10001)#Sets values for host- the current domain name and port number 10000.
        print('*** Server starting on %s port %s ***' % server_address)
        print('IP address is %s' % ipaddr)
        sock.bind(server_address) # Bind Socket to the host and port
        sock.listen(5) # Listens for incoming connections.

        while True: #Server always running.
            print('*** Waiting for a connection ***')
            connection, client_address = sock.accept() # Accepts connection between client and server.
            if not cons.isfull():
                cons.add(connection)
                try:
                    _thread.start_new_thread ( ConnectionHandler, (connection, client_address,cons) ) #Starts a new thread for each connection.
                except InterruptedError:
                    print("Error! The signal has been interrupted.")
                    connection.close()
                
    except  OSError:
        print("OS Error: Port number already in use or another server process may be running")
        sys.exit()
    except AttributeError:
            print("Error! An error has occured. Please try again later.")
            sys.exit()
    sock.close();



