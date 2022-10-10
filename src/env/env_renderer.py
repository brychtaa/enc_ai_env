# file: env_renderer.py
# author: Adam Brychta

from time import sleep

import pygame
from pygame.locals import (
    K_x,
    RLEACCEL,
    K_UP,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_SPACE
)

from env.robot_env import *

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600


class EnvSprite(pygame.sprite.Sprite):
    def __init__(self, row, col, file_path_image, pixels_height, pixels_width):
        super(EnvSprite, self).__init__()
        self.surf = pygame.image.load(file_path_image).convert()
        self.surf = pygame.transform.scale(self.surf, (pixels_height, pixels_width))
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.row_center = row * pixels_width
        self.col_center = col * pixels_height
        self.rect = self.surf.get_rect(topleft=[self.col_center, self.row_center])


def pygame_quit():
    pygame.quit()


def get_keyboard_action():
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return turn_off
                if event.key == K_UP:
                    return move_forward
                if event.key == K_LEFT:
                    return rotate_left
                if event.key == K_RIGHT:
                    return rotate_right
                if event.key == K_SPACE:
                    return clean
                if event.key == K_x:
                    return turn_off
            elif event.type == QUIT:
                return turn_off
        sleep(0.03)


class EnvRenderer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

        # Objekty na plose.
        self.sprites = None
        self.env = None
        self.pixels_width = None
        self.pixels_height = None

    def reset(self, env):
        self.sprites = []
        self.env = env
        self.pixels_width = SCREEN_WIDTH / env.rows
        self.pixels_height = SCREEN_HEIGHT / env.cols

    def update(self, state):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return False
            elif event.type == QUIT:
                return False

        for sprite in self.sprites:
            sprite.kill()
        self.sprites = []

        # Podle stavu prostredi vytvori objekty.
        for index_row in range(len(state)):
            for index_col in range(len(state[index_row])):
                # Nalezne typ objektu.
                env_object_with_char = self.env.get_env_object_type_char(state[index_row][index_col])
                self.sprites.append(EnvSprite(index_row, index_col, env_object_with_char.img, self.pixels_height,
                                              self.pixels_width))
        return True

    def render(self):
        # Pozadi.
        self.screen.fill((20, 20, 20))
        for entity in self.sprites:
            self.screen.blit(entity.surf, entity.rect)
        pygame.display.flip()
