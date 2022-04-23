from settings import *
import pygame as pg
import sys
import os

pg.init()

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

icon = pg.image.load(resource_path("assets/images/pong.png"))
ball = pg.image.load(resource_path("assets/images/ball.png"))
roboto = pg.font.Font(resource_path("assets/fonts/Roboto-Bold.ttf"), int(40*SCREEN_WIDTH/1280))