from settings import *
import pygame as pg
import sys
import os

pg.init()
pg.mixer.init()

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
icon = pg.image.load(resource_path("assets/images/pong.png"))
ball = pg.image.load(resource_path("assets/images/ball.png"))
main_bg = pg.image.load(resource_path("assets/images/main_bg.jpg")).convert()
pause_bg = pg.image.load(resource_path("assets/images/pause_bg.jpg")).convert()
roboto = pg.font.Font(resource_path("assets/fonts/Roboto-Bold.ttf"), int(40*SCREEN_WIDTH/1280))
roboto_light = pg.font.Font(resource_path("assets/fonts/Roboto-Regular.ttf"), int(20*SCREEN_WIDTH/1280))
ape_font = pg.font.Font(resource_path("assets/fonts/Ape.ttf"), int(80*SCREEN_WIDTH/1280))