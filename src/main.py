from settings import *
from stick import Player, Computer
from ball import Ball
from button import Button, Link
from scores import Score
from enums import Scene
import pygame as pg
import imports
import sys
import webbrowser

class Game:
    
    def __init__(self):
        pg.display.set_caption("Pong")
        pg.display.set_icon(imports.icon)
        self.scene = Scene.main_menu
        self.create_main_menu()
        self.all_sprites = pg.sprite.Group()
        self.players_group = pg.sprite.Group()
        self.ball_group = pg.sprite.GroupSingle()
        self.scores = pg.sprite.Group()
        self.player = Player((SCREEN_WIDTH/50, SCREEN_HEIGHT/2), self.players_group, self.all_sprites)
        self.computer = Computer((49*SCREEN_WIDTH/50, SCREEN_HEIGHT/2), self.players_group, self.all_sprites)
        self.player_score = Score(True,self.scores)
        self.computer_score = Score(False, self.scores)
        self.ball = Ball(self.ball_group, self.all_sprites)
        self.screen = imports.screen
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
    
    def scene_manager(self):
        while True:
            
            self.handle_events(pg.event.get())
            
            match self.scene:
                
                case Scene.main_menu:
                    self.main_menu()
                    
                case Scene.run:
                    self.run()

            self.clock.tick(self.FPS)
            pg.display.update()

    def create_main_menu(self):
        self.play_button = Button("Play", (SCREEN_WIDTH//2, SCREEN_HEIGHT//3))
        self.settings_button = Button("Settings", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.exit_button = Button("Exit", (SCREEN_WIDTH//2, 2*SCREEN_HEIGHT//3))
        self.source_link = Link("https://github.com/PraneethJain/Pong", bottomright=(SCREEN_WIDTH, SCREEN_HEIGHT)) 
        self.title = imports.ape_font.render("Pong!", True, "blue")
        self.version = imports.roboto_light.render(f"V{imports.VERSION}", True, "white")
    
    def main_menu(self):
        self.screen.blit(imports.background, (0, 0))
        self.screen.blit(self.title, (SCREEN_WIDTH//2-self.title.get_width()//2, SCREEN_HEIGHT//10))
        self.screen.blit(self.version, (0, SCREEN_HEIGHT-self.version.get_height()))
        self.source_link.update(self.screen)
        self.play_button.update(self.screen)
        self.settings_button.update(self.screen)
        self.exit_button.update(self.screen)
        
        if self.play_button.pressed:
            self.scene = Scene.run
            pg.time.delay(250)
            
        if self.settings_button.pressed:
            self.scene = Scene.settings_menu
            
        if self.exit_button.pressed:
            pg.quit()
            sys.exit()
        
        if self.source_link.pressed:
            webbrowser.open("https://github.com/PraneethJain/Pong")
            pg.time.delay(250)
        
    def run(self):

        self.screen.fill("black")
        
        
        self.scores.draw(self.screen)
        
        pg.draw.line(self.screen, "white", (SCREEN_WIDTH/2, 0), (SCREEN_WIDTH/2, SCREEN_HEIGHT))
        self.all_sprites.update()
        self.collide_check()
        self.computer.control(self.ball.rect.center)
        self.all_sprites.draw(self.screen)
        
        
            
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
    game.scene_manager()