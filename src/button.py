from settings import *
from imports import *

class Button:
    
    longest_width = 200
    height_inflation = 25
    
    def __init__(self, text: str, pos: tuple[int, int] = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), color="purple"):
        self.font = adistro_font
        self.image = self.font.render(text, True, color)
        self.pos = pos
        self.rect = self.image.get_rect(center = self.pos)
        self.bg = pg.Surface((Button.longest_width,self.rect.h+Button.height_inflation))
        self.bg.set_alpha(25)
        self.bg.fill((255,255,255))
        self.inflated_rect = self.rect.inflate(Button.longest_width-self.rect.w, Button.height_inflation)
        self.bg_pos = self.inflated_rect.topleft
        self.pressed = False
    
    def draw(self, screen: pg.Surface):
        screen.blit(self.image, self.rect.topleft)
        if self.inflated_rect.collidepoint(pg.mouse.get_pos()):
            screen.blit(self.bg, self.bg_pos)
            if any(pg.mouse.get_pressed()):
                self.pressed = True
            else:
                self.pressed = False
        else:
            self.pressed = False
        
    def update(self, screen: pg.Surface):
        self.draw(screen)
        
        
class Link:
    def __init__(self, text: str, pos: tuple[int, int] = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), bottomright = None):
        self.font = roboto_light
        self.image = self.font.render(text, True, "white")
        self.blue_image = self.font.render(text, True, "lightblue")
        self.pos = pos
        if bottomright:
            self.rect = self.image.get_rect(bottomright = bottomright)
        else:
            self.rect = self.image.get_rect(center = self.pos)
        self.pressed = False
    
    def draw(self, screen: pg.Surface):
        if self.rect.collidepoint(pg.mouse.get_pos()):
            screen.blit(self.blue_image, self.rect.topleft)
            if any(pg.mouse.get_pressed()):
                self.pressed = True
            else:
                self.pressed = False
        else:
            screen.blit(self.image, self.rect.topleft)
            self.pressed = False
        
    def update(self, screen: pg.Surface):
        self.draw(screen)