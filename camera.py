import pygame


#This class can be used to move the enviornment around the player
#You can pass a list of game entities or just one game entity
#Parameter "scene" -> On what surface to draw the entities
#Parameter "follow_target" -> What entity to follow?
#Parameter "target" -> Piece of enviornment

class Camera:
    def __init__(self, camera_center):
        self.camera_center = camera_center
    def display(self, follow_target, target, scene):
        if isinstance(target, list) :
            for i in range(len(target)):
                camera_x = target[i].rect.x - follow_target.rect.x + self.camera_center[0]
                camera_y = target[i].rect.y - follow_target.rect.y + self.camera_center[1]
                scene.blit(target[i].texture, (camera_x, camera_y))
        elif isinstance(target, dict) :
            for i in target :
                camera_x = target[i].rect.x - follow_target.rect.x + self.camera_center[0]
                camera_y = target[i].rect.y - follow_target.rect.y + self.camera_center[1]
                scene.blit(target[i].texture, (camera_x, camera_y))
        else :
            camera_x = target.rect.x - follow_target.rect.x + self.camera_center[0]
            camera_y = target.rect.y - follow_target.rect.y + self.camera_center[1]
            scene.blit(target.texture, (camera_x, camera_y))

