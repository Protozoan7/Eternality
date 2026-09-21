from player import player
from misc import *



def collision_platforms(body):
    if player.rect.colliderect(body):
        
        if player.yspeed >= 0 and player.rect.bottom - player.yspeed <= body.top:
            player.rect.bottom = body.top
            player.yspeed = 0
            player.onground = True
        
        elif player.yspeed < 0 and player.rect.top - player.yspeed >= body.bottom:
            player.rect.top = body.bottom
            player.yspeed = 0

def collision_mechanism(body):
    if body.colliderect(border1):
        body.right=border1.left
    if body.colliderect(border2):
        body.left=border2.right      
        
