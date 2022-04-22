from settings import *
from imports import *

class Score(pg.sprite.Sprite):
    
    def __init__(self, player: bool, *groups: pg.sprite.AbstractGroup) -> None:
        super().__init__(*groups)
        self.size = int(40*SCREEN_WIDTH/1280)
        self.font = pg.font.Font(resource_path("assets/fonts/Roboto-Bold.ttf"), self.size)
        self.image = self.font.render("0",True,"white")
        if player:
            self.rect = self.image.get_rect(topright=(14/15*SCREEN_WIDTH/2,SCREEN_HEIGHT/40))
        else:
            self.rect = self.image.get_rect(topleft=(16/15*SCREEN_WIDTH/2,SCREEN_HEIGHT/40))
    
    def update(self, score: int):
        self.image = self.font.render(f"{score}",True,"white")    
