import pygame
from enemies import *
from misc import *
from player import *
import random
import backgroundmusic
from misc import resource_path

current_wave = 0
global wavecount
wavecount = 1
waves = []
wave_schedule = []
wave_running = False
waiting_for_wipe = False   
wave_delay_timer = 0
font = pygame.font.Font(resource_path('graphics/PixeloidSans-E40en.ttf'), 50)
current_wave_text = font.render(f"Wave {wavecount}", True, (255, 255, 255))

schedule=[]
delayed=[]
remaining=[]

def define_waves():
    global waves, current_wave

    enemyspawns = [spawn_wizard, spawn_sentry, spawn_zombie, spawn_ghost,spawn_rush]
    current_wave = 0
    waves = []
    enemynumber = 4

    for x  in range(1,100):
        enemylist = []
        
        for y in range(1,enemynumber):
            tup = (y*3000,random.choice(enemyspawns))
            enemylist.append(tup)
        
        waves.append(enemylist)
        
        enemynumber+=2
            
def start_next_wave():
    global current_wave, waves, wave_schedule, wave_running, waiting_for_wipe
    waiting_for_wipe = False
    
      
    if current_wave >= len(waves):
        print("All waves complete!")
        return

    wave_running = True
    backgroundmusic.play_battle()
    now = pygame.time.get_ticks()
    print(f"---- WAVE {current_wave + 1} START ----")
    

    schedule = waves[current_wave]
    delayed = []

    for offset, fn in schedule:
        if offset == 0:
            fn()
        else:
            delayed.append((now + offset, fn))

    wave_schedule = delayed
    current_wave += 1

def update_wave_scheduler():
    global wave_schedule, wave_running
    now = pygame.time.get_ticks()
    remaining = []
    for trigger_time, fn in wave_schedule:
        if now >= trigger_time:
            fn()
        else:
            remaining.append((trigger_time, fn))

    wave_schedule = remaining

    
    if not wave_schedule:
        wave_running = False

def check_wave_complete(all_enemy_groups):
    global waiting_for_wipe, wave_delay_timer

    
    if wave_running:
        return False

    
    enemies_alive = any(len(group) > 0 for group in all_enemy_groups)

    if enemies_alive:
        waiting_for_wipe = True
        return False

    
    if waiting_for_wipe:
        waiting_for_wipe = False
        return True

    return False
