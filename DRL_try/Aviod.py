#@Time：2018/10/28 19:13
#@Author：Lee
#@File:Aviod.py
# Game target：Avoid falling bricks
import sys
import time
import pygame
from random import randint
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400
GAP_WIDTH = 10
TOP_WIDTH = 10
bg_color=(255,255,255)
ANIMATE_CYCLE = 10
planeS_posI = [WINDOW_WIDTH // 3, (3 * WINDOW_HEIGHT) // 4]
planeS_posS = [WINDOW_WIDTH // 3, (3 * WINDOW_HEIGHT) // 4]
plane= pygame.image.load('Pic/plane.jpg')
planeS = pygame.transform.smoothscale(plane, (WINDOW_WIDTH//4, WINDOW_HEIGHT//4))
BZ = pygame.image.load('Pic/BZ.jpg')
BZS = pygame.transform.smoothscale(BZ, (WINDOW_WIDTH//4, WINDOW_HEIGHT//4))
hero_surface=[]
hero_surface.append(planeS)
hero_surface.append(BZS)
hero_surface.append(planeS)
hero_surface.append(BZS)
hero_surface.append(planeS)
hero_surface.append(BZS)
#砖头
ZT= pygame.image.load('Pic/ZT.jpg')
enemy1_group = pygame.sprite.Group()
enemy1_surface=pygame.transform.smoothscale(ZT, (WINDOW_WIDTH//4, WINDOW_HEIGHT//4))
def ReturnName():
    return 'Aviod'

def Return_Num_Action():
    return 3

clock = pygame.time.Clock()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_surface, enemy_init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.smoothscale(ZT, (WINDOW_WIDTH//4, WINDOW_HEIGHT//4))
        self.rect = self.image.get_rect()
        self.rect.topleft = enemy_init_pos
        self.speed = 1
        self.score = 0
        FPS_CLOCK = pygame.time.Clock()
    def update(self):
        self.rect.top += self.speed
        if self.rect.top > WINDOW_HEIGHT:
           self.kill()
           self.score+=1
pygame.init()
group = pygame.sprite.Group()

class Plane(pygame.sprite.Sprite):
    def __init__(self, hero_surface, hero_init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.start_time = time.time()
        self.image = hero_surface
        self.speed = WINDOW_HEIGHT/20
        self.rect = self.image.get_rect()
        self.hero_index = 1
        self.rect.topleft = hero_init_pos
        self.is_hit = False
    def move(self, offset1):

        x = self.rect.left + offset1
        if x < 0:
            self.rect.left = 0
        elif x > WINDOW_WIDTH - self.rect.width:
            self.rect.left = WINDOW_WIDTH - self.rect.width
        else:
            self.rect.left = x
class GameState:
    def __init__(self):
        global FPS_CLOCK, screen, BASIC_FONT
        pygame.init()
        FPS_CLOCK = pygame.time.Clock()
        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Bricks Aviod')
        BASIC_FONT = pygame.font.Font('freesansbold.ttf', 16)
        self.my_score = 0
        # Set initial parameters
        self.init = True
        self.start_time = time.time()
        self.my_score = 0
    def frame_step(self,input):
        if self.init == True:
            pygame.init()
            pygame.display.set_caption('Bricks Aviod')  # 设置窗口标题
            global hero,ticks,screen
            ticks = 0
            screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])  # 初始化窗口
            hero = Plane(hero_surface[0], planeS_posS)
            screen.fill(bg_color)
            pygame.display.flip()
            self.reward=0
            self.terminalnum = 1
            screen.blit(hero.image, hero.rect)
            self.init = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.terminate()
        if input[1] == 1:
            offset2 = hero.speed
            hero.move(offset2)
        elif input[2] == 1:
            offset3 = - hero.speed
            hero.move(offset3)
        if (ticks%WINDOW_HEIGHT) == 10:
            enemy = Enemy(enemy1_surface,[randint(0, WINDOW_WIDTH - enemy1_surface.get_width()), -enemy1_surface.get_height()])
            enemy1_group.add(enemy)
        enemy1_group.update()
        enemy1_group.draw(screen)
        screen.blit(hero.image, hero.rect)
        pygame.display.update()
        ticks+=1
        self.reward = 0
        if ticks >= WINDOW_HEIGHT:
            self.reward = 1
            self.score = 1
            self.init = True
            self.terminalnum=0
        else:
            self.reward= 0
            self.terminalnum = 1
        enemy1_down_list = pygame.sprite.spritecollide(hero, enemy1_group, True)
        if len(enemy1_down_list) > 0:  # 不空
           hero.is_hit = True
        if hero.is_hit:
            self.terminalnum = 0#0 for ture
            self.reward = 0
            self.init = True
            #Explosion animation
          # if self.ticks % ANIMATE_CYCLE == 0:
          #    hero.hero_index += 1
          #    hero.image = hero_surface[hero.hero_index]
          #    if hero.hero_index == 2:
          #       hero.hero_index=0
        if self.terminalnum==0:
            terminal = True
        else:
            terminal = False
        pygame.display.update()
        reward=self.reward
        image_data = pygame.surfarray.array3d(pygame.display.get_surface())
        return image_data, reward, terminal
    def terminate(self):
        pygame.quit()
        sys.exit()
if __name__ == '__main__':
     agent = GameState()
     while True:
       agent.frame_step([0,1,0])
