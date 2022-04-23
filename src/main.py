from settings import *
from stick import Player, Computer
from ball import Ball
from scores import Score
import pygame as pg
import imports
import sys


class Game:
    
    def __init__(self):
        pg.display.set_caption("Pong")
        pg.display.set_icon(imports.icon)
        self.all_sprites = pg.sprite.Group()
        self.players_group = pg.sprite.Group()
        self.ball_group = pg.sprite.GroupSingle()
        self.scores = pg.sprite.Group()
        self.player = Player((SCREEN_WIDTH/50, SCREEN_HEIGHT/2), self.players_group, self.all_sprites)
        self.computer = Computer((49*SCREEN_WIDTH/50, SCREEN_HEIGHT/2), self.players_group, self.all_sprites)
        self.player_score = Score(True,self.scores)
        self.computer_score = Score(False, self.scores)
        self.ball = Ball(self.ball_group, self.all_sprites)
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pg.time.Clock()
        self.FPS = FPS
        self.score_player = 0
        self.score_computer = 0

    def collide_check(self):
        if pg.sprite.spritecollideany(self.ball, self.players_group):
            if self.ball.velocity.x > 0:
                self.ball.velocity.x += FORCE
            else:
                self.ball.velocity.x -= FORCE
            self.ball.velocity.x *= -1
            
        if self.ball.rect.right >= SCREEN_WIDTH:
            self.score_player += 1
            self.player_score.update(self.score_player)
            pg.time.delay(250)
            self.reset()
            
        if self.ball.rect.left <=0:
            self.score_computer += 1
            self.computer_score.update(self.score_computer)
            pg.time.delay(250)
            self.reset()
        
    def run(self):
        while True:
            
            self.screen.fill("black")
            self.handle_events(pg.event.get())
            
            self.scores.draw(self.screen)
            
            pg.draw.line(self.screen, "white", (SCREEN_WIDTH/2, 0), (SCREEN_WIDTH/2, SCREEN_HEIGHT))
            self.all_sprites.update()
            self.collide_check()
            self.computer.control(self.ball.rect.center)
            self.all_sprites.draw(self.screen)
            
            self.clock.tick(self.FPS)
            pg.display.update()
            
    @staticmethod
    def handle_events(events: list[pg.event.Event]):
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
                
    def reset(self):
        self.all_sprites = pg.sprite.Group()
        self.players_group = pg.sprite.Group()
        self.ball_group = pg.sprite.GroupSingle()
        self.player = Player((SCREEN_WIDTH/50, SCREEN_HEIGHT/2), self.players_group, self.all_sprites)
        self.computer = Computer((49*SCREEN_WIDTH/50, SCREEN_HEIGHT/2), self.players_group, self.all_sprites)
        self.ball = Ball(self.ball_group, self.all_sprites)
                
if __name__ == "__main__":
    game = Game()
    game.run()