from pygame import *
from pygame.locals import *
import numpy as np
import sys

#? Color Codes
gray = (100, 100, 100)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
orange = (255, 128, 0)
purple = (255, 0, 255)
cyan = (0, 255, 255)
black = (0, 0, 0)

#? Game Class
class ZombieSurvival():
    def __init__(self):
        self.screen_dimensions = [700, 700] #* Width, Height 
        self.disp = display.set_mode((self.screen_dimensions[0], self.screen_dimensions[1]), 0, 32)
        self.bullet_cooldown_timer = 30
        self.bullet_cooldown = 0
        self.character_move_speed = 10
        self.zombie_move_speed = 1
        self.bullet_speed = 20
        self.bullet_dimensions = 5
        self.bullet_color = black
        self.bullet_list = []
        self.character_dimensions = 50
        self.initial_character_position = (int(self.screen_dimensions[0]/2 - self.character_dimensions/2), int(self.screen_dimensions[1] - self.character_dimensions))
        self.barricade_width = 30
        self.zombie_dimensions = 50
        self.character_color = blue
        self.zombie_color = red
        self.barricade_color = yellow
        self.background_color = green
        self.random_number_key = 50
        self.random_number_key_2 = 500

        self.character_position = list(self.initial_character_position)
        self.zombie_list = []
        self.zombie_list_rect = []
        self.points = 0

    #generate_zombies -> step -> check collision -> blit

    def blit(self):
        self.disp.fill(self.background_color)
        self.barricade_rect = draw.rect(self.disp, self.barricade_color, (0, self.screen_dimensions[1]-self.character_dimensions-self.barricade_width, self.screen_dimensions[0], self.barricade_width))
        draw.rect(self.disp, self.character_color, (self.character_position[0], self.character_position[1], self.character_dimensions, self.character_dimensions))
        self.zombie_list_rect = []; self.bullet_list_rect = []
        for zombie_coor in self.zombie_list:
            self.zombie_list_rect.append(draw.rect(self.disp, self.zombie_color, (zombie_coor[0], zombie_coor[1], self.zombie_dimensions, self.zombie_dimensions)))
        for bullet_coor in self.bullet_list:
            self.bullet_list_rect.append(draw.rect(self.disp, self.bullet_color, (bullet_coor[0], bullet_coor[1], self.bullet_dimensions, self.bullet_dimensions)))
        display.update()

    def step(self):
        #? Close game
        for e in event.get():
            if e.type==QUIT:
                quit()
                sys.exit()

        keys = key.get_pressed()
        if keys[K_LEFT]:
            self.character_position[0] -= self.character_move_speed
        elif keys[K_RIGHT]:
            self.character_position[0] += self.character_move_speed
        if keys[K_a]:
            if self.bullet_cooldown == 0:
                self.shoot_bullet()

        if self.bullet_cooldown != 0:
            self.bullet_cooldown -= 1
        if self.character_position[0] < 0:
            self.character_position[0] = 0
        elif self.character_position[0] > self.screen_dimensions[0]-self.character_dimensions:
            self.character_position[0] = self.screen_dimensions[0]-self.character_dimensions

        self.bullet_list = [[bullet[0], bullet[1] - self.bullet_speed] for bullet in self.bullet_list]
        self.zombie_list = [[zombie[0], zombie[1] + self.zombie_move_speed] for zombie in self.zombie_list]
        
    def reset(self):
        self.zombie_list = []
        self.bullet_list = []
        self.character_position = list(self.initial_character_position)
        self.points = 0

    def generate_zombies(self):
        if np.random.randint(0,self.random_number_key) == 1:
            if len(self.zombie_list) == 0:
                self.zombie_list.append([np.random.randint(0,self.screen_dimensions[0]-self.zombie_dimensions), 0-self.zombie_dimensions])
            else:
                self.zombie_list.append([self.zombie_list[-1][0] + np.random.randint(-self.random_number_key_2, self.random_number_key_2), 0-self.zombie_dimensions])
                while self.zombie_list[-1][0] > self.screen_dimensions[0]-self.zombie_dimensions or self.zombie_list[-1][0] < 0:
                    self.zombie_list[-1][0] = self.zombie_list[-2][0] + np.random.randint(-self.random_number_key_2, self.random_number_key_2)

    def check_collision(self):
        for index_bullet, bullet_rect in enumerate(self.bullet_list_rect):
            for index_zombie, zombie_rect in enumerate(self.zombie_list_rect):
                if bullet_rect.colliderect(zombie_rect):
                    self.points += 1
                    try:
                        self.bullet_list.remove(self.bullet_list[index_bullet])
                        self.zombie_list.remove(self.zombie_list[index_zombie])
                    except IndexError:
                        pass
            try:
                if self.bullet_list[index_bullet] in self.bullet_list and self.bullet_list[index_bullet][1] <= -self.bullet_dimensions:
                    self.bullet_list.remove(self.bullet_list[index_bullet])
            except IndexError:
                pass

        for index_zombie, zombie_rect in enumerate(self.zombie_list_rect):
            if zombie_rect.colliderect(self.barricade_rect):
                self.zombie_list.remove(self.zombie_list[index_zombie])
                return True
        return False

    def shoot_bullet(self):
        self.bullet_list.append([int(self.character_position[0]+self.character_dimensions/2-self.bullet_dimensions/2), int(self.screen_dimensions[1]-self.character_dimensions-self.bullet_dimensions)])
        self.bullet_cooldown = self.bullet_cooldown_timer

