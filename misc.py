import pygame


import sys, os

def resource_path(rel_path):
    base = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base, rel_path)


#borders

border_surf_1=pygame.Surface((1,750),pygame.SRCALPHA)
border1=border_surf_1.get_rect(topright=(1500,0))
border_surf_2=pygame.Surface((1,750),pygame.SRCALPHA)
border2=border_surf_2.get_rect(topleft=(0,0))

#platforms 

platform_surf_1=pygame.Surface((200,20))
platform_surf_2=pygame.Surface((200,20))
platform_surf_3=pygame.Surface((200,20))
platform_surf_1.fill("#747474")
platform_surf_2.fill('#747474')
platform_surf_3.fill('#747474')
platform2=platform_surf_1.get_rect(midbottom=(650,250))
platform3=platform_surf_2.get_rect(midbottom=(950,400))
platform1 = platform_surf_3.get_rect(midbottom=(300,450))

#ground 

ground=pygame.Surface((1500,200))
ground.fill("#0e142e")
ground_hitbox=ground.get_rect(midtop=(750,600))

#shop surf

store = pygame.Surface((0,0))
store_hitbox=ground.get_rect(midtop=(0,0))


deathmusicflag = True



class Button:
    def __init__(self, x, y, w, h, colour, text="", alpha=255):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = colour
        self.text = text
        self.alpha = alpha

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def check_click(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)
    
    
    
    def set_opacity(self, alpha):
            self.alpha = alpha
            
    
def screen_menu(screen, buttons):
    screen.fill((50, 120, 200))
    for i in buttons:
        i.draw(screen)

def screen_game(screen):
    screen.fill((50, 200, 80))  


def variables():
    global border1
    global border2
    global ground
    global platform1
    global platform2
    global platform3
    global ground_hitbox
    global border_surf_1
    global border_surf_2
    global platform_surf_1
    global platform_surf_2
    global platform_surf_3
    global menu_surf_1
    global menu1
    global deathmusicflag
   


    menu_surf_1 = pygame.Surface((500,250))
    menu1 = menu_surf_1.get_rect(midtop=(500,250))


#Menu

play_button = Button(650, 325, 200, 80, (0, 255, 0), "Play")
quit_button = Button(650, 475, 200, 80, (255, 0, 0), "Quit")


#SHOP

increase_health = Button(300, 250, 455, 434,(255, 255, 255, 128), "Increase Damage")
increase_damage = Button(800, 250, 455, 434, (255, 255, 255, 128), "Increase Health")
store_new = pygame.image.load(resource_path("graphics/shop.png"))



