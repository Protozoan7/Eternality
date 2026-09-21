import pygame
pygame.mixer.init()
import random
from misc import resource_path




def play_battle():
    start_time = random.choice([0.0,18.3,55.2])
    pygame.mixer.music.load(resource_path('audio/battle_theme.wav'))
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(loops = -1, start = start_time)
    

def play_wavecomplete():
    pygame.mixer.music.load(resource_path('audio/wavecomplete.wav'))  
    pygame.mixer.music.play()

def play_start():
    pygame.mixer.music.load(resource_path('audio/shop theme_final.wav'))
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(loops = -1)
    

def play_death():
    pygame.mixer.music.load(resource_path('audio/eternal.wav'))
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(loops = -1)

def play_sound(filepath):
    fx = pygame.mixer.Sound(resource_path(filepath))
    fx.play()