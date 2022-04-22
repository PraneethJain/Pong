from settings import *
from imports import *

class Stick(pg.sprite.Sprite):
    def __init__(self, pos, *groups: pg.sprite.AbstractGroup) -> None:
        super().__init__(*groups)
        self.image = pg.Surface((SCREEN_WIDTH/54, SCREEN_HEIGHT/6))
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect(center = pos)
        self.speed = PLAYER_SPEED
        self.dir = pg.math.Vector2()
        
    def bounds(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Player(Stick):
    
    def control(self):
        pressed = pg.key.get_pressed()
        up = pressed[pg.K_UP] or pressed[pg.K_w]
        down = pressed[pg.K_DOWN] or pressed[pg.K_s]
        if up or down:
            if up and down:
                self.dir.y = 0
            elif up:
                self.dir.y = -1
            elif down:
                self.dir.y = +1
        else:
            self.dir.y=0
            
        self.rect.y += self.dir.y*self.speed

    def update(self):
        self.control()
        self.bounds()
        
class Computer(Stick):
    def control(self, ball_pos):
        x, y = ball_pos
        if x>=SCREEN_WIDTH/2:
            if self.rect.centery > y:
                self.dir.y = -1
            elif self.rect.centery < y:
                self.dir.y = +1
        else:
            self.dir.y = 0
        self.rect.y += self.dir.y*self.speed
        self.bounds()
