import pygame
import random
from player import player, attack1
import game_statistics as stats
import misc
import backgroundmusic
import collisions 
from misc import resource_path

class Zombie(pygame.sprite.Sprite):
    def __init__(self, player, ground_hitbox, health = 100, strength=5):
        super().__init__()
        self.player = player
        self.health = health
        self.audiocooldown = 30
        self.strength = strength
        self.damagecooldown = 30
        self.speed = 1
        self.anim_right = []
        for i in range(1, 6):
            frame = pygame.image.load(resource_path(f"graphics/zombie/zombie{i}.png")).convert_alpha()
            frame=pygame.transform.scale(frame,(80,80))
            self.anim_right.append(pygame.transform.flip(frame,True,False))
        self.anim_left = []
        for img in self.anim_right:
            self.anim_left.append(pygame.transform.flip(img, True, False))
        self.current_sprite = 0
        self.image = self.anim_right[0]
        self.rect = self.image.get_rect(midbottom=(random.randint(0, 1500), ground_hitbox.y))

    def take_damage(self, amount):
        if self.health >= amount:
            self.health -= amount
            stats.update_stats('damage_dealt',amount)

        else:
            stats.update_stats('damage_dealt',self.health)
            self.health = 0
        

    def update(self, player, attack):
        self.audiocooldown += 1
        self.damagecooldown +=1
        
        if player.rect.x < self.rect.x:
            self.rect.x -= self.speed
            self.current_anim = self.anim_left

        else:
            self.rect.x += self.speed
            self.current_anim = self.anim_right

        if self.rect.colliderect(attack.rect) and player.is_attacking and self.damagecooldown >= 30:
            self.take_damage(player.strength)
            self.damagecooldown = 0
            
        

        if self.rect.colliderect(attack.rect) and player.is_attacking and self.audiocooldown >= 30:
            backgroundmusic.play_sound('audio/damage_hit.wav')
            self.audiocooldown = 0

        if self.rect.colliderect(player.rect):
            player.take_damage(self.strength)
            

        self.current_sprite += 0.15

        if self.current_sprite >= len(self.current_anim):
            self.current_sprite = 0

        self.image = self.current_anim[int(self.current_sprite)]
        if self.health <= 0:
            backgroundmusic.play_sound('audio/monster_death.wav')
            self.kill()

class Sentry(pygame.sprite.Sprite):
    def __init__(self, player, ground_hitbox, health=60):
        super().__init__()
        self.player = player
        
        self.audiocooldown = 30
        self.health = health
        self.maxhealth = health
        self.strength = 5
        self.animright = []
        for i in range(1, 22):
            img = pygame.image.load(resource_path(f"graphics/Skeletonsentry/Skeleton Mage{i}.png")).convert_alpha()
            img=pygame.transform.scale(img,(80,80))
            self.animright.append(img)
        self.animleft = []
        for img in self.animright:
            self.animleft.append(pygame.transform.flip(img, True, False))
        self.image = self.animright[0]
        self.rect = self.image.get_rect(center=(random.randint(1, 1500), ground_hitbox.y-32))
        self.current_sprite = 0
        self.isright = True
        self.cooldown = 0
        self.damagecooldown = 30
        self.arrows = pygame.sprite.Group()

    def take_damage(self, amt):

        if self.health >= amt:
            self.health -= amt
            stats.update_stats('damage_dealt',amt)

        else:
            stats.update_stats('damage_dealt',self.health)
            self.health = 0


    def animation(self):
        self.current_sprite += 0.15
        if self.current_sprite >= len(self.animright):
            self.current_sprite = 0
        elif self.current_sprite >= len(self.animleft):
            self.current_sprite = 0
        if self.isright:
            self.image = self.animright[int(self.current_sprite)]
        else:
            self.image = self.animleft[int(self.current_sprite)]

    def update(self, player, attack):
        self.cooldown += 1
        self.damagecooldown += 1
        if self.cooldown >= 120:
            self.cooldown = 0
            self.arrows.add(Arrow(self, player))
            backgroundmusic.play_sound('audio/sentry_shoot.wav')
        self.arrows.update(self, player)
        if self.rect.colliderect(attack.rect) and player.is_attacking and self.damagecooldown >= 30:
            self.damagecooldown = 0
            self.take_damage(player.strength)
            
        self.audiocooldown += 1

        if self.rect.colliderect(attack.rect) and player.is_attacking and self.audiocooldown >= 30:
            backgroundmusic.play_sound('audio/damage_hit.wav')
            self.audiocooldown = 0

        if self.health <= 0:
            backgroundmusic.play_sound('audio/monster_death.wav')
            self.kill()
        if player.rect.x < self.rect.x:
            self.isright = False
        else:
            self.isright = True
        self.animation()

    def animation(self):
        self.current_sprite += 0.15
        if self.current_sprite >= len(self.animright):
            self.current_sprite = 0
        elif self.current_sprite >= len(self.animleft):
            self.current_sprite = 0
        if self.isright:
            self.image = self.animright[int(self.current_sprite)]
        else:
            self.image = self.animleft[int(self.current_sprite)]

class Arrow(pygame.sprite.Sprite):
    def __init__(self, sentry, player, strength=5):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill("yellow")
        self.rect = self.image.get_rect(center=sentry.rect.center)
        self.pos = pygame.Vector2(self.rect.center)
        self.speed = 10
        self.strength = strength
        direction = pygame.Vector2(player.rect.center) - pygame.Vector2(sentry.rect.center)
        self.direction = direction.normalize() if direction.length() != 0 else pygame.Vector2(0, 0)
        self.attackcooldown = 60

    def update(self, sentry, player):
        self.pos += self.direction * self.speed
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        if self.rect.colliderect(player.rect) and self.attackcooldown >= 60:
            self.attackcooldown = 0
            player.take_damage(self.strength)
            
        self.attackcooldown += 1

class Wizard(pygame.sprite.Sprite):
    def __init__(self, ground_hitbox, health=90, strength=20):
        super().__init__()
        self.health = health
        self.audiocooldown = 30
        self.damagecooldown = 30
        self.maxhealth = health
        self.strength = strength
        self.anim = []
        for i in range(1, 9):
            self.anim.append(pygame.image.load(resource_path(f"graphics/Wizard/wizard{i}.png")).convert_alpha())
        self.image = self.anim[0]
        self.rect = self.image.get_rect(midbottom=(random.randint(0, 1500), ground_hitbox.y))
        self.fireballs = pygame.sprite.Group()
        self.timer = 0
        
        self.current_sprite = 0
        
        


    def animation(self):
        self.current_sprite+=0.1
        if self.current_sprite>=len(self.anim):
            self.current_sprite=0
        self.image=self.anim[int(self.current_sprite)]
        

    def take_damage(self, amount):
        if self.health >= amount:
            self.health -= amount
            stats.update_stats('damage_dealt',amount)

        else:
            stats.update_stats('damage_dealt',self.health)
            self.health = 0

    def update(self, player, attack):
        self.timer += 1
        self.damagecooldown +=1
        
        if self.timer >= 30:
            self.timer = 0
            self.fireballs.add(Fireball(self))
        self.fireballs.update(self, player)
        if self.rect.colliderect(attack.rect) and player.is_attacking and self.damagecooldown>=30:
            
            self.take_damage(player.strength)
            self.damagecooldown = 0
            
        self.audiocooldown += 1

        if self.rect.colliderect(attack.rect) and player.is_attacking and self.audiocooldown >= 30:
            backgroundmusic.play_sound('audio/damage_hit.wav')
            self.audiocooldown = 0
        if self.health <= 0:
            backgroundmusic.play_sound('audio/monster_death.wav')
            self.kill()
        self.animation()

class Fireball(pygame.sprite.Sprite):
    def __init__(self, wizard, strength=15):
        super().__init__()
        self.image = pygame.Surface((100, 100))
        self.image.fill("orange")
        self.rect = self.image.get_rect(center=(random.randint(1, 1500), 0))
        self.pos = pygame.Vector2(self.rect.center)
        self.speed = 10
        self.strength = strength
        self.cooldown = 60

    def update(self, wizard, player):
        self.pos.y += self.speed
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        if self.rect.colliderect(player.rect) and self.cooldown >= 60:
            self.cooldown = 0
            player.take_damage(self.strength)
            
        self.cooldown += 1
        if self.rect.y > 800:
            self.kill()

class Ghost(pygame.sprite.Sprite):
    def __init__(self, ground_hitbox, health=20, strength=25):
        super().__init__()
        self.health = health
        self.strength = strength
        self.anim = []
        for i in range(1, 16):
            self.anim.append(pygame.image.load(resource_path(f"graphics/Ghost/Ghost{i}.png")).convert_alpha())
        self.image = self.anim[0]
        self.rect = self.image.get_rect(center=(random.randint(1, 1500), ground_hitbox.y - 32))
        self.t = 0
        self.cooldown = 60
        self.audiocooldown = 30

        self.current_sprite = 0


    def take_damage(self, amount):
        if self.health >= amount:
            self.health -= amount
            stats.update_stats('damage_dealt',amount)

        else:
            stats.update_stats('damage_dealt',self.health)
            self.health = 0


    def animation(self):
        self.current_sprite += 0.15
        if self.current_sprite >= len(self.anim):
            self.current_sprite = 0
        self.image = self.anim[int(self.current_sprite)]

    def update(self, player, attack):
        self.t += 1
        self.cooldown += 1

        collisions.collision_mechanism(self.rect)
        

        if self.t <= 120:
            self.rect.x += 1
        elif self.t <= 360:
            self.rect.x -= 1
        else:
            self.t = 0

        if self.rect.colliderect(attack.rect) and player.is_attacking:
            self.cooldown = 0
            self.take_damage(player.strength)
            
        if self.rect.colliderect(player.rect) and self.cooldown >= 60:
            self.cooldown = 0
            player.take_damage(self.strength)
            
        self.audiocooldown += 1

        if self.rect.colliderect(attack.rect) and player.is_attacking and self.audiocooldown >= 30:
            backgroundmusic.play_sound('audio/damage_hit.wav')
            self.audiocooldown = 0

        if self.health <= 0:
            backgroundmusic.play_sound('audio/monster_death.wav')
            self.kill()
        
        self.animation()

class Rush(pygame.sprite.Sprite):
    def __init__(self, ground_hitbox):
        super().__init__()
        self.image = pygame.transform.rotate(pygame.image.load(resource_path("graphics/bulletrush.png")).convert_alpha(),180)
        self.rect = self.image.get_rect(midright=(0, ground_hitbox.y - 32))
        self.speed = 15
        self.t = 0
        self.ind = None
        self.strength = 40
        self.cooldown = 60
        self.audioflag = True
        

    def update(self, screen, ground_hitbox,attack):
        self.t += 1
        self.cooldown += 1
        if self.t < 120:
            self.ind = Indicator(ground_hitbox)
            screen.blit(self.ind.image, self.ind.rect)
        else:
            self.rect.x += self.speed

        if self.t>120 and self.audioflag:
            backgroundmusic.play_sound('audio/bullet_rush.wav')
            self.audioflag = False
            
        if self.rect.x > 1600:
            self.kill()
        
        if self.rect.colliderect(player.rect) and self.cooldown >= 60:
            self.cooldown = 0
            player.take_damage(self.strength)
            

class Indicator(pygame.sprite.Sprite):
    def __init__(self, ground_hitbox):
        super().__init__()
        self.image = pygame.Surface((32, 64))
        self.image.fill("Red")
        self.rect = self.image.get_rect(midbottom=(10, misc.ground_hitbox.y))

zombies = pygame.sprite.Group()
sentries = pygame.sprite.Group()
wizards = pygame.sprite.Group()
ghosts = pygame.sprite.Group()
rushes = pygame.sprite.Group()

all_enemy_groups = [zombies, sentries, wizards, ghosts, rushes]
all_projectiles = pygame.sprite.Group()

def spawn_zombie():
    z = Zombie(player, misc.ground_hitbox)
    zombies.add(z)

def spawn_sentry():
    s = Sentry(player, misc.ground_hitbox)
    sentries.add(s)

def spawn_wizard():
    w = Wizard(misc.ground_hitbox)
    backgroundmusic.play_sound('audio/witch laugh.wav')
    wizards.add(w)

def spawn_ghost():
    g = Ghost(misc.ground_hitbox)
    ghosts.add(g)

def spawn_rush():
    r = Rush(misc.ground_hitbox)
    rushes.add(r)

def update_enemies(screen):
    all_projectiles.empty()
    for group in all_enemy_groups:
        for enemy in group:
            if hasattr(enemy, "ind"):
                enemy.update(screen, misc.ground_hitbox,attack1)
            else:  
                enemy.update(player, attack1)
                if hasattr(enemy, "arrows"):
                    for a in enemy.arrows:
                        all_projectiles.add(a)
                if hasattr(enemy, "fireballs"):
                    for f in enemy.fireballs:
                        all_projectiles.add(f)
            
                
            
                

def draw_enemies(screen):
    for group in all_enemy_groups:
        group.draw(screen)
    all_projectiles.draw(screen)
