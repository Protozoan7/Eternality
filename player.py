import pygame
from misc import *
import backgroundmusic
import game_statistics as stats
from misc import resource_path

pygame.font.init()
font = pygame.font.Font(resource_path('graphics/PixeloidSans-E40en.ttf'),30)

class player_char(pygame.sprite.Sprite):

    def __init__(self, strength = 40, speed=7, health=100, ground_hitbox=None):
        super().__init__()

        self.is_attacking = False
        self.is_jumping = False
        self.facing_right = True
        self.yspeed = 0
        self.onground = False

        self.speed = speed
        self.strength = strength
        self.maxhealth = health
        self.health = health
        self.take_damage_cooldown = 0
        self.attack_cooldown = 0

        self.animations = {
            "idle_right": [],
            "idle_left": [],
            "walk_right": [],
            "walk_left": [],
            "jump_right": [],
            "jump_left": [],
            "attack_right": [],
            "attack_left": [],
            
        }

        self.preload_images()

        self.current_anim = "idle_right"
        self.current_sprite = 0
        self.image = self.animations[self.current_anim][0]
        self.rect = self.image.get_rect(midbottom=(750, 300))

        self.gravity = 1
        self.ground_hitbox = ground_hitbox


        self.font = pygame.font.Font(resource_path('graphics/PixeloidSans-E40en.ttf'), 28)
        self.health_bar_width = 300
        self.health_bar_height = 25
        self.strenghttext= font.render(f"Strength: {self.strength}", True, (255, 255, 255))

        
    def preload_images(self):

        i = 1
        while i < 10:
            path = resource_path("graphics/idle animationz/AnimationSheet_Character" + str(i) + ".png")
            img = pygame.image.load(path).convert_alpha()
            self.animations["idle_right"].append(img)
            self.animations["idle_left"].append(pygame.transform.flip(img, True, False))
            i += 1

        i = 1
        while i < 9:
            path = resource_path("graphics/soldierwalk/Animationwalk_Character" + str(i) + ".png")
            img = pygame.image.load(path).convert_alpha()
            self.animations["walk_right"].append(img)
            self.animations["walk_left"].append(pygame.transform.flip(img, True, False))
            i += 1

        i = 1
        while i < 9:
            path = resource_path("graphics/Charjump/charjump" + str(i) + ".png")
            img = pygame.image.load(path).convert_alpha()
            self.animations["jump_right"].append(img)
            self.animations["jump_left"].append(pygame.transform.flip(img, True, False))
            i += 1

        i = 3
        while i < 6:
            path = resource_path("graphics/Charattack/Charattack" + str(i) + ".png")
            img = pygame.image.load(path).convert_alpha()
            self.animations["attack_right"].append(img)
            self.animations["attack_left"].append(pygame.transform.flip(img, True, False))
            i += 1
        
        

    def set_animation(self, anim_name):
        direction = "right" if self.facing_right else "left"
        full_name = anim_name + "_" + direction
        
        if self.current_anim != full_name:
            self.current_anim = full_name
            self.current_sprite = 0

    def animation(self):
        self.current_sprite += 0.2
        frames = self.animations[self.current_anim]

        if self.current_sprite >= len(frames):
            self.current_sprite = 0
            if self.is_attacking:
                self.is_attacking = False
                self.set_animation("idle")
            

        self.image = frames[int(self.current_sprite)]

    def start_attack(self):
        if not self.is_attacking:
            self.is_attacking = True
            self.set_animation("attack")
            backgroundmusic.play_sound('audio/attack_sound.wav')

    def movement_update(self, keys):
        self.take_damage_cooldown+=1
        self.attack_cooldown+=1

        if keys[pygame.K_h] and self.attack_cooldown > 30:
            self.start_attack()
            self.attack_cooldown = 0



        if self.is_attacking:
            self.animation()
            return

        walking = False

        if keys[pygame.K_d]:
            self.rect.x += self.speed
            self.facing_right = True
            self.set_animation("walk")
            walking = True

        elif keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.facing_right = False
            self.set_animation("walk")
            walking = True

        if not walking:
            self.set_animation("idle")

        if keys[pygame.K_SPACE] and self.onground:
            self.yspeed = -25
            self.set_animation("jump")
            self.onground = False
            backgroundmusic.play_sound('audio/jump_sound.wav')

        
        
        self.yspeed+=self.gravity
        self.rect.y += self.yspeed




        self.strenghttext= font.render(f"Strength: {self.strength}", True, (255, 255, 255))
        

        self.animation()

    def take_damage(self, amount):

        if self.take_damage_cooldown > 60:
            if self.health >= amount:
                stats.update_stats("damage_taken",amount)
            else:
                stats.update_stats("damage_taken",self.health)

            self.health -= amount
            
            
            backgroundmusic.play_sound('audio/damage_voice.wav')
            self.take_damage_cooldown = 0

        if self.health <= 0:
            self.health = 0
            
            


            
                    

    
    def draw_health_bar(self, surface):
        ratio = self.health / self.maxhealth

        pygame.draw.rect(surface, (60, 0, 0),(20, 20, self.health_bar_width, self.health_bar_height))

        pygame.draw.rect(surface, (200, 0, 0),(20, 20, int(self.health_bar_width * ratio), self.health_bar_height))

        text = self.font.render(str(self.health) + "/" + str(self.maxhealth), True, (255, 255, 255))
        text_rect = text.get_rect(center=(20 + self.health_bar_width // 2,20 + self.health_bar_height // 2))
        surface.blit(text, text_rect)



class attack(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.surf = pygame.surface.Surface((80, 32), pygame.SRCALPHA)
        self.player = player
        self.rect = self.surf.get_rect(center=(self.player.rect.centerx + 32, self.player.rect.centery))

    def updateplayer(self):
        if not self.player.facing_right:
            self.rect.center = (self.player.rect.centerx - 32, self.player.rect.centery)
        else:
            self.rect.center = (self.player.rect.centerx + 32, self.player.rect.centery)


player = player_char(ground_hitbox = ground_hitbox)
attack1 = attack(player)
