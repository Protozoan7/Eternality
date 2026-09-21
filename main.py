import pygame
pygame.init()
screen = pygame.display.set_mode((1500, 750))
pygame.display.set_caption("Eternality")
import game_statistics as stats
import misc
from misc import *
from backgroundmusic import *
import collisions
misc.variables()   
from player import *
from enemies import *
from waves import *
pygame.mixer.init(frequency=44100, channels=64)
stats.create_stats()
from misc import resource_path

background = pygame.image.load(resource_path("graphics/battlearena.jpg"))

backgroundmusic.play_start()

clock = pygame.time.Clock()
running = True

game_state = "menu"
deathmusicflag = True


current_wave = 0
wavecount = 1

font = pygame.font.Font(resource_path('graphics/PixeloidSans-E40en.ttf'), 40)
current_wave_text = font.render(f"Wave {wavecount}", True, (255, 255, 255))

define_waves()

def blit_game_screen():
    screen.blit(background, (0, 0))

    screen.blit(misc.ground, misc.ground_hitbox)
    screen.blit(player.image, player.rect)
    screen.blit(attack1.surf, attack1.rect)

    screen.blit(misc.border_surf_1, misc.border1)
    screen.blit(misc.border_surf_2, misc.border2)
    screen.blit(misc.platform_surf_1, misc.platform1)
    screen.blit(misc.platform_surf_2, misc.platform2)
    screen.blit(misc.platform_surf_3, misc.platform3)

    player.draw_health_bar(screen)
    screen.blit(player.strenghttext, (20, 50))
    screen.blit(current_wave_text, (650, 50))

    draw_enemies(screen)



while running:

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        
        if game_state == "menu":
            if play_button.check_click(event):
                game_state = "game"
            if quit_button.check_click(event):
                running = False
            define_waves()

        
        if player.health == 0 and game_state != "death":
            game_state = "death"

        
        if game_state == "game":
            play_battle()
            start_next_wave()
            game_state = "gamerunning"


    
    if game_state == "menu":
        
        play_button.draw(screen)
        quit_button.draw(screen)
        screen.blit(pygame.image.load(resource_path("graphics/Eternalbackground.png")), (0, 0))
        pygame.display.flip()
        continue


    
    if game_state == "death":
        screen.fill((0, 0, 0))

        if deathmusicflag:
            backgroundmusic.play_death()
            deathmusicflag = False

        gameoverfont = pygame.font.Font(resource_path('graphics/PixeloidSans-E40en.ttf'), 100)
        statsfont = pygame.font.Font(resource_path('graphics/PixeloidSans-E40en.ttf'), 50)

        game_over_text = gameoverfont.render("GAME OVER", True, (255, 0, 0))
        stats_text = statsfont.render(stats.disp_stats(), True, (255, 255, 255))
        continuetext = statsfont.render("Continue", True, (255, 255, 255))

        continuebutton = Button(650, 500, 230, 100, (0, 0, 255), "Continue")

        screen.blit(game_over_text, (400, 100))
        screen.blit(stats_text, (450, 250))
        continuebutton.draw(screen)
        screen.blit(continuetext, (650, 520))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if continuebutton.check_click(event):

                
                player.health = 100
                stats.create_stats()

                waves.clear()
                schedule.clear()
                delayed.clear()
                remaining.clear()
                wave_schedule.clear()

                for i in all_enemy_groups:
                    i.empty()

                misc.variables()
                
                

                player.__init__(ground_hitbox=misc.ground_hitbox)
                define_waves()

                
                current_wave = 0
                wavecount = 1
                current_wave_text = font.render(f"Wave {wavecount}", True, (255, 255, 255))
                
                deathmusicflag = True
                game_state = "menu"
                continue

        continue


    
    if game_state == "gamerunning":

        screen.fill((0, 0, 0))
        blit_game_screen()

        keys = pygame.key.get_pressed()
        player.movement_update(keys)
        attack1.updateplayer()

        update_enemies(screen)

        collisions.collision_platforms(misc.platform1)
        collisions.collision_platforms(misc.platform2)
        collisions.collision_platforms(misc.platform3)
        collisions.collision_platforms(misc.ground_hitbox)
        collisions.collision_mechanism(player.rect)

        update_wave_scheduler()

        if check_wave_complete(all_enemy_groups):

            flag = True
            stats.update_stats('waves_completed',1)
            backgroundmusic.play_wavecomplete()
            

            wavecount += 1
            current_wave_text = font.render(f"Wave {wavecount}", True, (255, 255, 255))

            while flag:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                increase_damage.draw(screen)
                increase_health.draw(screen)
                screen.blit(store_new, (0, 0))

                if increase_damage.check_click(event):
                    player.strength = min(100, player.strength + 10)
                    flag = False

                elif increase_health.check_click(event):
                    player.health = min(100, player.health + 30)
                    flag = False

                pygame.display.flip()
                clock.tick(60)

            start_next_wave()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
