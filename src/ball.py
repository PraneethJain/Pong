from settings import *
import pygame as pg
import imports
from random import randrange, choice
from math import sin, cos, pi
from time import sleep

class Ball(pg.sprite.Sprite):
    
    def __init__(self, *groups: pg.sprite.AbstractGroup) -> None:
        super().__init__(*groups)
        self.image = pg.transform.scale(imports.ball, (25, 25))
        self.rect = self.image.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        self.speed = BALL_SPEED
        self.velocity = pg.math.Vector2()
        self.pos = pg.math.Vector2(self.rect.center)
        self.start()
        
    def start(self):
        theta = choice([randrange(30,60), randrange(120,150), randrange(210,240), randrange(300, 330)])*pi/180
        self.velocity.x = BALL_SPEED*cos(theta)
        self.velocity.y = BALL_SPEED*sin(theta)
    
    def move(self):
        
        if self.rect.right>=SCREEN_WIDTH or self.rect.left <=0:
            self.velocity.x *= -1
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.velocity.y *= -1
        
        self.pos.x += self.velocity.x
        self.pos.y += self.velocity.y
        self.rect.center = self.pos.x, self.pos.y
        
    def update(self):
        self.move()