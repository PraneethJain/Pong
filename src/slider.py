from settings import *
from imports import *


class Slider:
    def __init__(
        self,
        width: int = 250,
        pos: tuple[int, int] = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2),
    ):
        self.image = pg.Surface((width, 5))
        self.image.fill((100, 100, 100))
        self.rect = self.image.get_rect(center=pos)
        self.current = 100
        self.filled = pg.Surface(
            (self.current * self.image.get_width() / 100, self.image.get_height())
        )
        self.filled.fill((0, 128, 128))
        self.filled_rect = self.filled.get_rect(topleft=self.rect.topleft)
        self.pressed = False

    def draw(self):
        screen.blit(self.image, self.rect.topleft)
        screen.blit(self.filled, self.filled_rect.topleft)
        pg.draw.circle(
            screen,
            (0, 128, 128),
            (self.rect.left + self.current / 100 * self.rect.width, self.rect.centery),
            8,
        )

    def value(self):
        x, y = pg.mouse.get_pos()
        if any(pg.mouse.get_pressed()):
            if self.rect.collidepoint(x, y):
                self.current = (x - self.rect.left) * 100 / self.rect.w
                self.pressed = True
            if self.pressed:
                if x > self.rect.right:
                    self.current = 100
                elif x < self.rect.left:
                    self.current = 0

            self.filled = pg.Surface(
                (self.current * self.image.get_width() / 100, self.image.get_height())
            )
            self.filled.fill((0, 128, 128))
            self.filled_rect = self.filled.get_rect(topleft=self.rect.topleft)
        else:
            self.pressed = False

    def update(self):
        self.draw()
        self.value()
