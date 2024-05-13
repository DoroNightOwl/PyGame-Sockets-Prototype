#Importing required modules
import socket
import json
from threading import Thread
from time import time
from sprites import AnimatedObject
from math import sqrt


ADRESS = socket.gethostname()
PORT = 9000

#Initializing the game server socket
game_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
game_server.bind((ADRESS, PORT))
game_server.listen()

#Initializing two empty lists, one of the clients and one for the server logs
clients = []
log = []

#This function has the purpose of iterating through each client
#Retrieve inputs from them and process new data
#Which will be sent back to each of the clients
def game_processing(clients):
    server_start_message = "Server has started !"
    log.append(server_start_message)
    print(server_start_message)
    buffer = "@"
    speed = 50
    diagonal_speed = sqrt(pow(speed,2)/2)
    entities = {}
    initial_time = time()
    current_time = time()
    delta_time = current_time - initial_time
    while True:
        #Getting the initial time of this loop iteration
        initial_time = time()
        received_data = {}
        send_data = {}
        #Obtaining data from each of the clients
        #Expecting to receive data serialized as JSON dictionary
        for connected_client in range(len(clients)):
                client_data = clients[connected_client][0].recv(1024).decode("utf-8")
                #If client stops sending data, we remove him from the list
                if not client_data :
                     del clients[connected_client]
                     del entities[connected_client]
                     break
                client_data = client_data[:client_data.find(buffer)]
                received_data[connected_client] = client_data
        print(received_data)
        for connected_client in range(len(clients)):
            if not connected_client in entities:entities[connected_client] = {"POS_X" : 0, "POS_Y" : 0}
        for data in range(len(received_data)):
            try :
                received_data[data] = json.loads(received_data[data])
            except : 
                print("Something went bad with JSON conversion...")
        for connected_client in range(len(received_data)):
            try :
                movement = False
                #Axis movement processing
                if received_data[connected_client]["UP"] == True:
                    entities[connected_client]["POS_Y"] -= speed * delta_time 
                    movement = True
                    orientation = "left"
                if received_data[connected_client]["LEFT"] == True:
                    entities[connected_client]["POS_X"] -= speed * delta_time 
                    movement = True
                if received_data[connected_client]["DOWN"] == True:
                    entities[connected_client]["POS_Y"] += speed * delta_time 
                    movement = True
                if received_data[connected_client]["RIGHT"] == True:
                    entities[connected_client]["POS_X"] += speed * delta_time 
                    movement = True
                    orientation = "right"

                #Diagonal movement processing
                if received_data[connected_client]["UP"] and received_data[connected_client]["LEFT"] :
                    entities[connected_client]["POS_Y"] -= diagonal_speed * delta_time 
                    entities[connected_client]["POS_X"] -= diagonal_speed * delta_time 
                    movement = True
                    orientation = "left"
                if received_data[connected_client]["LEFT"] and received_data[connected_client]["DOWN"] :
                    entities[connected_client]["POS_Y"] += diagonal_speed * delta_time 
                    entities[connected_client]["POS_X"] -= diagonal_speed * delta_time 
                    movement = True
                    orientation = "left"
                if received_data[connected_client]["DOWN"] and received_data[connected_client]["RIGHT"] :
                    entities[connected_client]["POS_Y"] += diagonal_speed * delta_time 
                    entities[connected_client]["POS_X"] += diagonal_speed * delta_time 
                    movement = True
                    orientation = "right"
                if received_data[connected_client]["RIGHT"] and received_data[connected_client]["UP"] :
                    entities[connected_client]["POS_Y"] -= diagonal_speed * delta_time 
                    entities[connected_client]["POS_X"] += diagonal_speed * delta_time 
                    movement = True
                    orientation = "right"
                entities[connected_client]["MOVEMENT"] = movement
                entities[connected_client]["ORIENTATION"] = orientation
            except : pass
        for connected_client in range(len(entities)):
            try :
                send_data[received_data[connected_client]["ID"]] = entities[connected_client]
            except : pass
        for connected_client in range(len(clients)):
            clients[connected_client][0].send(bytes(json.dumps(send_data),"utf-8"))

        current_time = time()
        #Calculating the delta time used for proessing game events
        delta_time = current_time - initial_time


#Starting the function responsible for processing the game status and data
#It runs as a separate thread
Thread(target=game_processing, args=(clients,)).start()

#Here the server is waiting for and accepting new connections
#The server also saves some information in a list (server logs)
while True:
    client, adress = game_server.accept()
    new_client_connected_message = f"Client with adress {adress} has sucessfully connected !"
    print(new_client_connected_message)
    log.append(new_client_connected_message)
    clients.append((client, adress))
