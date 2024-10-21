
import pygame
import sys
import os
import time
from random import randint
from os import path
pygame.init() 

window = pygame.display.set_mode((800,600))

pygame.display.set_caption("Here Be Dragons")

DRAGON_IMAGE = pygame.image.load(os.path.join('assets_here_be_dragons', 'SMOK.png'))
DRAGON = pygame.transform.scale(DRAGON_IMAGE, (150, 160))

KNIGHT_IMAGE = pygame.image.load(os.path.join('assets_here_be_dragons', 'rycerz.png'))
KNIGHT = pygame.transform.flip(pygame.transform.scale(KNIGHT_IMAGE, (150, 160)),True, False)

princess_image =pygame.image.load(os.path.join('assets_here_be_dragons', 'Princess.png'))
princess_scale = pygame.transform.scale(princess_image, (70, 70))

start_time = 0

our_font = pygame.font.Font(os.path.join('assets_here_be_dragons', 'JosefinSans-Medium.ttf'), 45)

knight_sound = pygame.mixer.Sound(os.path.join('assets_here_be_dragons', 'holy_grail_bless.wav'))
dragon_sound = pygame.mixer.Sound(os.path.join('assets_here_be_dragons', 'ROAR.wav'))



class Dragon: 
    def __init__(self):
        self.x_cord = 130
        self.y_cord = 220

        self.width = 140
        self.height = 160
        self.hitbox = pygame.Rect(self.x_cord+35, self.y_cord+40, self.width, self.height)

    def tick(self,keys_pressed): 
        VELO = 10
        if keys_pressed[pygame.K_a] and self.x_cord >0:
            self.x_cord -= VELO
        if keys_pressed[pygame.K_d] and self.x_cord <650:
            self.x_cord += VELO
        if keys_pressed[pygame.K_w] and self.y_cord >5:
            self.y_cord -= VELO
        if keys_pressed[pygame.K_s] and self.y_cord <465:
            self.y_cord += VELO

        self.hitbox = pygame.Rect(self.x_cord+50, self.y_cord+25, self.width, self.height)
    def draw(self): 
        window.blit(DRAGON,(self.x_cord, self.y_cord))

        
class Knight: 
    def __init__(self):
        self.x_cord = 560
        self.y_cord = 250
        
        self.width = 140
        self.height = 160
        
        self.hitbox = pygame.Rect(self.x_cord+20, self.y_cord+40, self.width, self.height)
    
        
    def tick(self,keys_pressed): 
        VELO = 10
        if keys_pressed[pygame.K_LEFT] and self.x_cord >-43:
            self.x_cord -= VELO
        if keys_pressed[pygame.K_RIGHT] and self.x_cord <650:
            self.x_cord += VELO
        if keys_pressed[pygame.K_UP] and self.y_cord >-20:
            self.y_cord -= VELO
        if keys_pressed[pygame.K_DOWN] and self.y_cord <436:
            self.y_cord += VELO

        self.hitbox = pygame.Rect(self.x_cord+20, self.y_cord+25, self.width, self.height)
    def draw(self): 
        window.blit(KNIGHT,(self.x_cord, self.y_cord))
        
class Princess:
    def __init__(self):
        self.x_cord = randint(10,720)
        self.y_cord = randint(100,520)
        
        self.width = 70
        self.height = 70
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)
        
    def tick(self):
         
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)


    def draw(self):
        window.blit(princess_scale,(self.x_cord, self.y_cord))


def time_passing_screen():
        current_time = int(pygame.time.get_ticks() / 1000) - start_time
        if current_time <= 15:
            time_surf = our_font.render(f'{current_time}', False, (255,0,255))
            time_rect = time_surf.get_rect(center = (400,40))
            window.blit(time_surf, time_rect)
        if current_time > 15 and current_time <= 18:
            time_surf = our_font.render(f'Lets Fight!', False, (255,174,255))
            time_rect = time_surf.get_rect(center = (400,40))
            window.blit(time_surf, time_rect)


def main():
    run = True
    
    background = pygame.image.load(os.path.join('assets_here_be_dragons', 'tlo_GOTOWE.png'))
    #background_music = pygame.mixer.Sound(os.path.join('assets_here_be_dragons', 'background_music_done.wav'))
    dragon=Dragon()
    knight=Knight()

    dragon_power = 0
    knight_power = 0

    able_attack_dragon = True
    able_attack_knight = True
    
    current_time = 0
    clock = 0
    able_attack_dragon_timer = 0
    able_attack_knight_timer = 0
    
    princesses = []


    while run:
        clock += pygame.time.Clock().tick(600)/1000
        pygame.time.Clock().tick(600)
        
        
        
        keys_pressed= pygame.key.get_pressed()
        
        if clock >= 0.05:
            clock = 0
            princesses.append(Princess())
        
        dragon.tick(keys_pressed)
        knight.tick(keys_pressed)
        for p in princesses:
            p.tick()

        
        
        for p in princesses:
            if dragon.hitbox.colliderect(p.hitbox):
                princesses.remove(p)
                dragon_power +=1
        for p in princesses:
            if knight.hitbox.colliderect(p.hitbox):
                princesses.remove(p)
                knight_power +=1

        
        #atak smoka
        if keys_pressed[pygame.K_LCTRL] and dragon_power >= 1 and dragon.hitbox.colliderect(knight.hitbox) and current_time > 16000:
            if able_attack_dragon == True:
                knight_power = knight_power - 3
                dragon_power = dragon_power - 1
            able_attack_dragon = False
            able_attack_dragon_timer += pygame.time.Clock().tick(600)/1000
            if able_attack_dragon_timer >= 0.005:
                able_attack_dragon = True
                able_attack_dragon_timer = 0
        #atak rycerza
        if keys_pressed[pygame.K_RCTRL] and knight_power >=1 and knight.hitbox.colliderect(dragon.hitbox) and current_time > 16000:
            if able_attack_knight == True:
                knight_power = knight_power - 1
                dragon_power = dragon_power - 3
                
            able_attack_knight = False
            able_attack_knight_timer += pygame.time.Clock().tick(600)/1000
            if able_attack_knight_timer >= 0.005:
                able_attack_knight = True
                able_attack_knight_timer = 0

        dragon_power_image = our_font.render(f"Dragon: {dragon_power}", True, (0,0,0))
        knight_power_image = our_font.render(f"Knight: {knight_power}", True, (0,0,0))
        

        window.blit(background,(0,0))
        window.blit(dragon_power_image,(40,15))
        window.blit(knight_power_image,(550,15))

        
        time_passing_screen()
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
                
        
        dragon.draw()
        knight.draw()

        for p in princesses:
            p.draw()
        current_time = pygame.time.get_ticks()


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LCTRL:
                DRAGON_WIN_IMAGE = pygame.image.load(os.path.join('assets_here_be_dragons', 'SMOK_win.png')) #SMOK
                DRAGON_WIN = pygame.transform.scale(DRAGON_WIN_IMAGE, (240, 280))
                window.blit(DRAGON_WIN,(dragon.x_cord-50, dragon.y_cord-70))
                    
            if event.key == pygame.K_RCTRL:
                KNIGHT_IMAGE = pygame.image.load(os.path.join('assets_here_be_dragons', 'rycerz_win.png'))
                KNIGHT = pygame.transform.flip(pygame.transform.scale(KNIGHT_IMAGE, (250, 270)),True, False)
                window.blit(KNIGHT,(knight.x_cord-39, knight.y_cord-49))
        
 
        #unable attack - zly czas  
        if keys_pressed[pygame.K_LCTRL] and current_time <= 16000: #SMOK
            write_attack_failed_dragon_time = our_font.render(f"Not Yet!", False, (0,0,0))
            window.blit(write_attack_failed_dragon_time, (40, 60))

        if keys_pressed[pygame.K_RCTRL] and current_time <= 16000: #RYCERZ
            write_attack_failed_knight_time = our_font.render(f" Not Yet!", True, (0,0,0))
            window.blit(write_attack_failed_knight_time, (535, 60))

        #unable attack - za daleko
        if keys_pressed[pygame.K_LCTRL] and current_time > 16000: #SMOK
            if not dragon.hitbox.colliderect(knight.hitbox):
                write_attack_failed_dragon = our_font.render(f"Get Closer!", False, (0,0,0))
                window.blit(write_attack_failed_dragon, (40, 60))

        if keys_pressed[pygame.K_RCTRL] and current_time > 16000: #RYCERZ
            if not knight.hitbox.colliderect(dragon.hitbox):
                write_attack_failed_knight = our_font.render(f"Get Closer!", True, (0,0,0))
                window.blit(write_attack_failed_knight, (535, 60))

        
        if knight_power <= 0 and current_time > 16000: #RYCERZ POKONANY
                pygame.mixer.Sound.play(dragon_sound)
                
                pygame.mixer.music.stop()
                who_wins_text = our_font.render('DRAGON WINS!', True, (200, 200, 200))
                window.fill((0, 0, 0))
                window.blit(who_wins_text, (235, 260))

                DRAGON_WIN_IMAGE = pygame.image.load(os.path.join('assets_here_be_dragons', 'SMOK_win.png'))
                DRAGON_WIN = pygame.transform.scale(DRAGON_WIN_IMAGE, (520, 540))
                window.blit(DRAGON_WIN,(-50, 300))
                
                pygame.display.update()
                time.sleep(5)
                pygame.quit()
                sys.exit()
                
        if dragon_power <= 0 and current_time > 16000: #SMOK POKONANY
                pygame.mixer.Sound.play(knight_sound)
                pygame.mixer.music.stop()
                pygame.mixer.music.stop()
                who_wins_text = our_font.render('KNIGHT WINS!', True, (200, 200, 200))
                window.fill((0, 0, 0))
                window.blit(who_wins_text, (235, 260))

                KNIGHT_IMAGE = pygame.image.load(os.path.join('assets_here_be_dragons', 'rycerz_win.png'))
                KNIGHT = pygame.transform.flip(pygame.transform.scale(KNIGHT_IMAGE, (500, 530)),True, False)
                window.blit(KNIGHT, (390, 260))
                
                pygame.display.update()
                time.sleep(5)
                pygame.quit()
                sys.exit()
                
        
 
        pygame.display.flip()
        pygame.display.update()

        

if __name__ == "__main__":
    main()