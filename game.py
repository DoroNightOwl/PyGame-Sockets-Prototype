import pygame
import socket
import json
from time import time
from sys import exit
from threading import Thread
from id_generator import generate_id
from sprites import Player
from sprites import AnimatedObject
from camera import Camera

pygame.init()

RESOLUTIONS = [(640,360),
               (960,540),
               (1280,720),
               (1600,900)]
res_key = 0
screen = pygame.display.set_mode(RESOLUTIONS[res_key])

CAMERA_CENTER = (160-16, 90-16)

#Declaring some surfaces for drawing elements of the game or menu
game_scene = pygame.Surface((320,180))
menu_scene = pygame.Surface((960,720))

#Initializing a client socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((socket.gethostname(),9000))
#Initializing game objects
player = Player("player\\walk\\player-run-1.png",(0,0))
player.load_anim("walk",
                 ["player\\walk\\player-run-1.png",
                  "player\\walk\\player-run-2.png",
                  "player\\walk\\player-run-3.png",
                  "player\\walk\\player-run-4.png",
                  "player\\walk\\player-run-5.png",
                  "player\\walk\\player-run-6.png"])
player.flip_anim("walk")
player.load_anim("idle",
                 ["player\\idle\\player-idle-1.png",
                  "player\\idle\\player-idle-2.png",
                  "player\\idle\\player-idle-3.png",
                  "player\\idle\\player-idle-4.png"])
camera = Camera(CAMERA_CENTER)
#Defining the singleplayer scene
singeplayer_ON = False
def singleplayer_scene():
    player.move(10, delta_time)
    player.play_anim("walk",0.15)
    game_scene.fill("white")
    game_scene.blit(player.texture,player.rect)
    screen.blit(pygame.transform.scale(game_scene,(960,540)),(0,0))

#Thread for sending data
#Defining the multiplayer scene
player.initialize_signals()
buffer = "@"
multiplayer_ON = True
other_players = {}
def multiplayer_scene():
    data_to_send = player.send_signals()
    data_to_send = json.dumps(data_to_send)
    data_to_send += buffer
    client.send(bytes(data_to_send,"utf-8"))

    received_data = client.recv(1024).decode("utf-8")
    try :
        received_data = json.loads(received_data)
        if received_data[player.ID]:
            new_x = received_data[player.ID]["POS_X"]
            new_y = received_data[player.ID]["POS_Y"]
            player.float_x = new_x
            player.float_y = new_y
            player.rect.x = player.float_x
            player.rect.y = player.float_y
        player_ids = received_data.keys()
        for id in player_ids:
            if id in other_players:
                pass
            elif id == player.ID :
                pass
            else :
                other_players[id] = AnimatedObject("player\\walk\\player-run-1.png",(received_data[id]["POS_X"],received_data[id]["POS_Y"]))
                other_players[id].load_anim("walk",
                    ["player\\walk\\player-run-1.png",
                     "player\\walk\\player-run-2.png",
                     "player\\walk\\player-run-3.png",
                     "player\\walk\\player-run-4.png",
                     "player\\walk\\player-run-5.png",
                     "player\\walk\\player-run-6.png"])
                other_players[id].load_anim("idle",
                    ["player\\idle\\player-idle-1.png",
                     "player\\idle\\player-idle-2.png",
                     "player\\idle\\player-idle-3.png",
                     "player\\idle\\player-idle-4.png"])
        for id in other_players:
            #game_scene.blit(id.texture, id.rect)
            new_x = received_data[id]["POS_X"]
            new_y = received_data[id]["POS_Y"]
            other_players[id].float_x = new_x
            other_players[id].float_y = new_y
            other_players[id].rect.x = other_players[id].float_x
            other_players[id].rect.y = other_players[id].float_y
            if received_data[id]["MOVEMENT"] == True :
                other_players[id].play_anim("walk",0.15)
            else :
                other_players[id].play_anim("idle",0.15)
        camera.display(player,other_players,game_scene)
    except :
        pass
    if player.UP or player.LEFT or player.RIGHT or player.DOWN :
        player.play_anim("walk",0.15)
    else :
        player.play_anim("idle",0.20)
    print(received_data)
    game_scene.fill("white")
    game_scene.blit(player.texture,(CAMERA_CENTER[0], CAMERA_CENTER[1]))
    camera.display(player, other_players, game_scene)
    screen.blit(pygame.transform.scale(game_scene,RESOLUTIONS[res_key]),(0,0))



#Initializing the delta time variables
initial_time = time()
current_time = time()
delta_time = current_time - initial_time
while True :
    #Calculating the initial time
    initial_time = time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    if singeplayer_ON : singleplayer_scene()
    if multiplayer_ON : multiplayer_scene()

    pygame.display.flip()
    #Calculating the current time
    current_time = time()
    #Calculating the delta time
    delta_time = current_time - initial_time

