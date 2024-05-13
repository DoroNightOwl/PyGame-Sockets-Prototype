import pygame
from math import sqrt
from time import time
from id_generator import generate_id
#Parameter "image location" -> source of the image
#Parameter "position" -> the initialized position of the object
class StaticObject:
    def __init__(self, image_location, position):
        self.texture = pygame.image.load(image_location)
        self.rect = self.texture.get_rect(topleft=position)
        self.float_x = self.rect.x
        self.float_y = self.rect.y
        self.last_x = self.float_x
        self.last_y = self.float_y

class AnimatedObject(StaticObject):
    def load_anim(self, animation_name, list_of_animation_frames):
        try :
            list_of_initialized_animation_frames = []
            for i in range(len(list_of_animation_frames)):
                list_of_initialized_animation_frames.append(pygame.image.load(list_of_animation_frames[i]))
            self.animations[animation_name] = list_of_initialized_animation_frames
            self.animations[animation_name+"_counter"] = None
            self.animations[animation_name+"_timer"] = None
        except :
            self.animations = {}
            self.load_anim(animation_name, list_of_animation_frames)

    #Used to play animations when a condition is satisfied
    def play_anim(self, animation_name, frame_cooldown):
        if self.animations[animation_name+"_timer"] == None:
            self.animations[animation_name+"_timer"] = time() + frame_cooldown
            self.animations[animation_name+"_counter"] = 0
        if time() > self.animations[animation_name+"_timer"] :
            counter = self.animations[animation_name+"_counter"] 
            self.animations[animation_name+"_timer"] = time() + frame_cooldown
            self.animations[animation_name+"_counter"] += 1
            self.texture = self.animations[animation_name][counter]
            #When an animation cycle is completed, this method will return 1
            if self.animations[animation_name+"_counter"] > len(self.animations[animation_name]) - 1:
                self.animations[animation_name+"_counter"] = 0
                return 1
    
    #Used to flip animations
    #Might not be as efficient as opposed to loading the flipped ?
    #Who knows...
    def flip_anim(self, animation_name):
        for frame in range(len(self.animations[animation_name])):
            self.animations[animation_name][frame] = pygame.transform.flip(self.animations[animation_name][frame], True, False)
            


#A player class
#Provides some physics functionalities to the game entity
class Player(AnimatedObject):
    #Allows the player to change his coordinates based on movement
    def move(self, speed, delta_time):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and not keys[pygame.K_a] and not keys[pygame.K_s] and not keys[pygame.K_d] :
            self.float_y -= speed * delta_time
            self.rect.y = self.float_y
        if not keys[pygame.K_w] and keys[pygame.K_a] and not keys[pygame.K_s] and not keys[pygame.K_d] :
            self.float_x -= speed * delta_time
            self.rect.x = self.float_x
        if not keys[pygame.K_w] and not keys[pygame.K_a] and keys[pygame.K_s] and not keys[pygame.K_d] :
            self.float_y += speed * delta_time
            self.rect.y = self.float_y
        if not keys[pygame.K_w] and not keys[pygame.K_a] and not keys[pygame.K_s] and keys[pygame.K_d] :
            self.float_x += speed * delta_time
            self.rect.x = self.float_x
        #Diagonal movement speed calculated to match the horizontal/vertical movement speed
        diagonal_speed = sqrt(pow(speed,2)/2)
        if keys[pygame.K_w] and keys[pygame.K_a] and not keys[pygame.K_s] and not keys[pygame.K_d] :
            self.float_x -= speed * delta_time
            self.rect.x = self.float_x
            self.float_y -= speed * delta_time
            self.rect.y = self.float_y
        if not keys[pygame.K_w] and keys[pygame.K_a] and keys[pygame.K_s] and not keys[pygame.K_d] :
            self.float_x -= speed * delta_time
            self.rect.x = self.float_x
            self.float_y += speed * delta_time
            self.rect.y = self.float_y
        if not keys[pygame.K_w] and not keys[pygame.K_a] and keys[pygame.K_s] and keys[pygame.K_d] :
            self.float_x += speed * delta_time
            self.rect.x = self.float_x
            self.float_y += speed * delta_time
            self.rect.y = self.float_y
        if keys[pygame.K_w] and not keys[pygame.K_a] and not keys[pygame.K_s] and keys[pygame.K_d] :
            self.float_x += speed * delta_time
            self.rect.x = self.float_x
            self.float_y -= speed * delta_time
            self.rect.y = self.float_y
    def initialize_signals(self):
        self.ID = generate_id()
        self.UP = False
        self.LEFT = False
        self.DOWN = False
        self.RIGHT = False
    def send_signals(self):
        keys = pygame.key.get_pressed()
        #Axis movement signals
        if keys[pygame.K_w] and not keys[pygame.K_a] and not keys[pygame.K_s] and not keys[pygame.K_d] : 
            self.UP = True
            return {"UP" : self.UP, "LEFT" : self.LEFT, "DOWN" : self.DOWN, "RIGHT" : self.RIGHT, "ID" : self.ID}
        else : 
            self.UP = False
        if not keys[pygame.K_w] and keys[pygame.K_a] and not keys[pygame.K_s] and not keys[pygame.K_d] : 
            self.LEFT = True
            return {"UP" : self.UP, "LEFT" : self.LEFT, "DOWN" : self.DOWN, "RIGHT" : self.RIGHT, "ID" : self.ID}
        else : 
            self.LEFT = False
        if not keys[pygame.K_w] and not keys[pygame.K_a] and keys[pygame.K_s] and not keys[pygame.K_d] : 
            self.DOWN = True
            return {"UP" : self.UP, "LEFT" : self.LEFT, "DOWN" : self.DOWN, "RIGHT" : self.RIGHT, "ID" : self.ID}
        else : 
            self.DOWN = False
        if not keys[pygame.K_w] and not keys[pygame.K_a] and not keys[pygame.K_s] and keys[pygame.K_d] :
            self.RIGHT = True
            return {"UP" : self.UP, "LEFT" : self.LEFT, "DOWN" : self.DOWN, "RIGHT" : self.RIGHT, "ID" : self.ID}
        else : 
            self.RIGHT = False
        #Diagonal movement signals
        if keys[pygame.K_w] and keys[pygame.K_a] and not keys[pygame.K_s] and not keys[pygame.K_d] : 
            self.UP, self.LEFT = True, True
            return {"UP" : self.UP, "LEFT" : self.LEFT, "DOWN" : self.DOWN, "RIGHT" : self.RIGHT, "ID" : self.ID}
        else : 
            self.UP, self.LEFT = False, False
        if not keys[pygame.K_w] and keys[pygame.K_a] and keys[pygame.K_s] and not keys[pygame.K_d] : 
            self.LEFT, self.DOWN = True, True
            return {"UP" : self.UP, "LEFT" : self.LEFT, "DOWN" : self.DOWN, "RIGHT" : self.RIGHT, "ID" : self.ID}
        else :
            self.LEFT, self.DOWN = False, False
        if not keys[pygame.K_w] and not keys[pygame.K_a] and keys[pygame.K_s] and keys[pygame.K_d] : 
            self.DOWN, self.RIGHT = True, True
            return {"UP" : self.UP, "LEFT" : self.LEFT, "DOWN" : self.DOWN, "RIGHT" : self.RIGHT, "ID" : self.ID}
        else : 
            self.DOWN, self.RIGHT = False, False
        if keys[pygame.K_w] and not keys[pygame.K_a] and not keys[pygame.K_s] and keys[pygame.K_d] : 
            self.RIGHT, self.UP = True, True
            return {"UP" : self.UP, "LEFT" : self.LEFT, "DOWN" : self.DOWN, "RIGHT" : self.RIGHT, "ID" : self.ID}
        else :
            self.RIGHT, self.UP = False, False
        return {"UP" : self.UP, "LEFT" : self.LEFT, "DOWN" : self.DOWN, "RIGHT" : self.RIGHT, "ID" : self.ID}

    def collide():
        pass



