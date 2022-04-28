from settings import *
from stick import Player, Computer
from ball import Ball
from button import Button, Link
from slider import Slider
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
        self.create_pause_menu()
        self.create_main_settings_menu()
        self.create_pause_settings_menu()
        self.all_sprites = pg.sprite.Group()
        self.players_group = pg.sprite.Group()
        self.ball_group = pg.sprite.GroupSingle()
        self.scores = pg.sprite.Group()
        self.player = Player(
            (SCREEN_WIDTH / 50, SCREEN_HEIGHT / 2), self.players_group, self.all_sprites
        )
        self.computer = Computer(
            (49 * SCREEN_WIDTH / 50, SCREEN_HEIGHT / 2),
            self.players_group,
            self.all_sprites,
        )
        self.player_score = Score(True, self.scores)
        self.computer_score = Score(False, self.scores)
        self.round = 1
        self.round_surf = imports.roboto.render(
            f"Round {self.round}", True, (255, 255, 255)
        )
        self.points = 0
        self.ball = Ball(self.ball_group, self.all_sprites)
        self.screen = imports.screen
        self.clock = pg.time.Clock()
        self.FPS = FPS
        self.score_player = 0
        self.score_computer = 0
        self.bg_volume = 100
        self.bg_sound = 100
        pg.mixer.music.play(-1)
        pg.mixer.music.set_volume(self.bg_sound / 100)

    def collide_check(self):
        if pg.sprite.spritecollideany(self.ball, self.players_group):
            if self.ball.velocity.x > 0:
                self.ball.velocity.x += FORCE
            else:
                self.ball.velocity.x -= FORCE
            imports.hit_sound.play()
            self.ball.velocity.x *= -1

    def score(self):
        if self.ball.rect.right >= SCREEN_WIDTH:
            self.score_player += 1
            self.computer.enlarge(1.1)
            imports.score_sound.play()
            self.player_score.update(self.score_player)
            pg.time.delay(250)
            self.points += self.round * 10
            if self.score_player == SCORE_TO_WIN:
                self.round += 1
                self.update_round()
                self.score_player = 0
                self.score_computer = 0
                self.player_score.update(self.score_player)
                self.computer_score.update(self.score_computer)
                self.computer.unenlarge()
                self.computer.speed_up(1)
            self.reset()

        if self.ball.rect.left <= 0:
            self.score_computer += 1
            imports.comp_score_sound.play()
            self.computer_score.update(self.score_computer)
            self.reset()
            if self.score_computer == SCORE_TO_WIN:
                self.round = 1
                self.update_round()
                self.create_game_over()
                self.scene = Scene.game_over
            pg.time.delay(250)

    def update_round(self):
        self.round_surf = imports.roboto.render(
            f"Round {self.round}", True, (255, 255, 255)
        )

    def update_volume(self):
        pg.mixer.music.set_volume(self.bg_volume / 100 * self.bg_sound / 100)

    def scene_manager(self):
        while True:

            self.handle_events(pg.event.get())

            match self.scene:

                case Scene.main_menu:
                    if self.bg_volume < 100:
                        self.bg_volume += 1
                        self.update_volume()
                    self.main_menu()

                case Scene.run:
                    if self.bg_volume > 50:
                        self.bg_volume -= 1
                        self.update_volume()
                    if self.bg_volume < 50:
                        self.bg_volume += 1
                        self.update_volume()
                    self.run()

                case Scene.pause_menu:
                    if self.bg_volume < 100:
                        self.bg_volume += 1
                        self.update_volume()
                    self.pause_menu()

                case Scene.game_over:
                    if self.bg_volume > 0:
                        self.bg_volume -= 1
                        self.update_volume()
                    self.game_over()

                case Scene.main_settings_menu:
                    self.main_settings_menu()

                case Scene.pause_settings_menu:
                    self.pause_settings_menu()

            self.clock.tick(self.FPS)
            pg.display.update()

    def create_main_menu(self):
        self.play_button = Button(
            "Play", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3), (17, 138, 178)
        )
        self.settings_button = Button(
            "Settings", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), (17, 138, 178)
        )
        self.exit_button = Button(
            "Exit", (SCREEN_WIDTH // 2, 2 * SCREEN_HEIGHT // 3), (17, 138, 178)
        )
        self.source_link = Link(
            "https://github.com/PraneethJain/Pong",
            bottomright=(SCREEN_WIDTH, SCREEN_HEIGHT),
        )
        self.title = imports.ape_font.render("Pong!", True, (239, 71, 111))
        self.version = imports.roboto_light.render(f"V{imports.VERSION}", True, "white")

    def main_menu(self):
        self.screen.blit(imports.main_bg, (0, 0))
        self.screen.blit(
            self.title,
            (SCREEN_WIDTH // 2 - self.title.get_width() // 2, SCREEN_HEIGHT // 10),
        )
        self.screen.blit(self.version, (0, SCREEN_HEIGHT - self.version.get_height()))
        self.source_link.update(self.screen)
        self.play_button.update(self.screen)
        self.settings_button.update(self.screen)
        self.exit_button.update(self.screen)

        if self.play_button.pressed:
            self.scene = Scene.run

        if self.settings_button.pressed:
            self.scene = Scene.main_settings_menu

        if self.exit_button.pressed:
            self.quit()

        if self.source_link.pressed:
            webbrowser.open("https://github.com/PraneethJain/Pong")
            pg.time.delay(250)

    @staticmethod
    def sound_effect_volume(volume):
        for sound in imports.sounds:
            sound.set_volume(volume / 100)

    def create_main_settings_menu(self):
        self.volume_surf = imports.roboto_small.render(
            "Background music", True, (193, 121, 2)
        )
        self.volume_slider = Slider(250, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3))
        self.volume_percent_surf = imports.roboto_small.render(
            f"{self.volume_slider.current}", True, (193, 121, 2)
        )
        self.sound_surf = imports.roboto_small.render(
            "Sound effects", True, (193, 121, 2)
        )
        self.sound_slider = Slider(250, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.sound_percent_surf = imports.roboto_small.render(
            f"{self.sound_slider.current}", True, (193, 121, 2)
        )
        self.go_back_button = Button(
            "Go back", (SCREEN_WIDTH / 2, 2 * SCREEN_HEIGHT / 3), (193, 121, 2)
        )

    def main_settings_menu(self):

        self.screen.blit(imports.main_bg, (0, 0))
        # Background Volume Slider
        self.screen.blit(
            self.volume_surf,
            (
                self.volume_slider.rect.left - self.volume_surf.get_width() - 10,
                SCREEN_HEIGHT / 3 - self.volume_surf.get_height() / 2,
            ),
        )
        self.screen.blit(
            self.volume_percent_surf,
            (
                self.volume_slider.rect.right + 10,
                SCREEN_HEIGHT / 3 - self.volume_percent_surf.get_height() / 2,
            ),
        )
        self.volume_slider.update()
        if self.volume_slider.pressed:
            self.bg_sound = self.volume_slider.current
            self.update_volume()
            self.volume_percent_surf = imports.roboto_small.render(
                f"{self.volume_slider.current}", True, (193, 121, 2)
            )

        # Sound Effects Slider
        self.screen.blit(
            self.sound_surf,
            (
                self.sound_slider.rect.left - self.sound_surf.get_width() - 10,
                SCREEN_HEIGHT / 2 - self.sound_surf.get_height() / 2,
            ),
        )
        self.screen.blit(
            self.sound_percent_surf,
            (
                self.sound_slider.rect.right + 10,
                SCREEN_HEIGHT / 2 - self.sound_percent_surf.get_height() / 2,
            ),
        )
        self.sound_slider.update()
        if self.sound_slider.pressed:
            self.sound_effect_volume(self.sound_slider.current)
            self.sound_percent_surf = imports.roboto_small.render(
                f"{self.sound_slider.current}", True, (193, 121, 2)
            )

        # Go Back Button
        self.go_back_button.update(self.screen)
        if self.go_back_button.pressed:
            self.scene = Scene.main_menu
            pg.time.delay(100)

    def create_pause_settings_menu(self):
        pass

    def pause_settings_menu(self):
        self.screen.blit(imports.pause_bg, (0, 0))
        self.screen.blit(
            self.volume_surf,
            (
                self.volume_slider.rect.left - self.volume_surf.get_width() - 10,
                SCREEN_HEIGHT / 3 - self.volume_surf.get_height() / 2,
            ),
        )
        self.screen.blit(
            self.volume_percent_surf,
            (
                self.volume_slider.rect.right + 10,
                SCREEN_HEIGHT / 3 - self.volume_percent_surf.get_height() / 2,
            ),
        )
        self.volume_slider.update()
        if self.volume_slider.pressed:
            self.bg_sound = self.volume_slider.current
            self.update_volume()
            self.volume_percent_surf = imports.roboto_small.render(
                f"{self.volume_slider.current}", True, (193, 121, 2)
            )

        # Sound Effects Slider
        self.screen.blit(
            self.sound_surf,
            (
                self.sound_slider.rect.left - self.sound_surf.get_width() - 10,
                SCREEN_HEIGHT / 2 - self.sound_surf.get_height() / 2,
            ),
        )
        self.screen.blit(
            self.sound_percent_surf,
            (
                self.sound_slider.rect.right + 10,
                SCREEN_HEIGHT / 2 - self.sound_percent_surf.get_height() / 2,
            ),
        )
        self.sound_slider.update()
        if self.sound_slider.pressed:
            self.sound_effect_volume(self.sound_slider.current)
            self.sound_percent_surf = imports.roboto_small.render(
                f"{self.sound_slider.current}", True, (193, 121, 2)
            )

        # Go Back Button
        self.go_back_button.update(self.screen)
        if self.go_back_button.pressed:
            pg.time.delay(100)
            self.scene = Scene.pause_menu

    def pause_to_run(self):
        for alpha in range(255):
            self.current_screen.set_alpha(alpha)
            self.screen.blit(self.current_screen, (0, 0))
            pg.display.update()
        self.scene = Scene.run

    def run(self):
        self.screen.fill("black")
        self.scores.draw(self.screen)

        pg.draw.line(
            self.screen,
            "white",
            (SCREEN_WIDTH / 2, 0),
            (SCREEN_WIDTH / 2, SCREEN_HEIGHT),
        )

        self.screen.blit(
            self.round_surf, (SCREEN_WIDTH - self.round_surf.get_width(), 0)
        )

        self.all_sprites.update()
        self.collide_check()
        self.score()
        self.computer.control(self.ball.rect.center)
        self.all_sprites.draw(self.screen)

    def create_game_over(self):
        self.over_surf = imports.thorn_font.render(f"You Lose", True, (164, 22, 26))
        self.score_title = imports.roboto.render("Score", True, (229, 229, 229))
        self.score_surf = imports.roboto.render(f"{self.points}", True, (229, 229, 229))
        self.restart_button = Button("Restart", color=(252, 163, 17))

    def game_over(self):
        self.screen.blit(imports.over_bg, (0, 0))
        self.screen.blit(
            self.over_surf,
            (SCREEN_WIDTH / 2 - self.over_surf.get_width() / 2, SCREEN_HEIGHT / 20),
        )
        self.screen.blit(
            self.score_title,
            (
                SCREEN_WIDTH / 2 - self.score_title.get_width() / 2,
                14 * SCREEN_HEIGHT / 20,
            ),
        )
        self.screen.blit(
            self.score_surf,
            (
                SCREEN_WIDTH / 2 - self.score_surf.get_width() / 2,
                16 * SCREEN_HEIGHT / 20,
            ),
        )
        self.restart_button.update(self.screen)
        if self.restart_button.pressed:
            self.reset()
            self.score_player = 0
            self.score_computer = 0
            self.player_score.update(self.score_player)
            self.computer_score.update(self.score_computer)
            self.scene = Scene.run

    def create_pause_menu(self):
        self.pause_resume_button = Button(
            "Resume", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3), (83, 179, 203)
        )
        self.pause_settings_button = Button(
            "Settings", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), (83, 179, 203)
        )
        self.pause_exit_button = Button(
            "Exit", (SCREEN_WIDTH // 2, 2 * SCREEN_HEIGHT // 3), (83, 179, 203)
        )
        self.paused_surf = imports.ape_font.render("Paused", True, (224, 26, 79))

    def run_to_pause(self):
        self.pause_bg_alpha = 0
        self.scene = Scene.pause_menu

    def pause_menu(self):
        if self.pause_bg_alpha <= 100:

            imports.pause_bg.set_alpha(self.pause_bg_alpha)
            self.pause_bg_alpha += 1
            self.screen.blit(imports.pause_bg, (0, 0))

        elif self.pause_bg_alpha > 100:

            self.screen.blit(imports.pause_bg, (0, 0))
            self.screen.blit(
                self.paused_surf,
                (
                    SCREEN_WIDTH / 2 - self.paused_surf.get_width() / 2,
                    SCREEN_HEIGHT / 20,
                ),
            )

            self.pause_resume_button.update(self.screen)
            self.pause_settings_button.update(self.screen)
            self.pause_exit_button.update(self.screen)

            if self.pause_resume_button.pressed:
                self.pause_to_run()

            if self.pause_settings_button.pressed:
                self.scene = Scene.pause_settings_menu

            if self.pause_exit_button.pressed:
                self.quit()

    def handle_events(self, events: list[pg.event.Event]):
        for event in events:
            if event.type == pg.QUIT:
                self.quit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    if self.scene == Scene.run:
                        self.current_screen = self.screen.copy()
                        self.run_to_pause()
                    elif self.scene == Scene.pause_menu:
                        self.pause_to_run()

    def reset(self):
        self.ball.kill()
        self.player.reset()
        self.computer.reset()
        self.ball = Ball(self.all_sprites, self.ball_group)

    def quit(self):
        pg.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.scene_manager()
