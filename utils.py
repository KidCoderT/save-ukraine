import pygame
from pygame.image import load


def load_img(filename: str):
    img = load(filename)
    img.convert()
    return img


def transform_img(img: pygame.Surface, size: tuple | float):
    n_img = pygame.transform.scale(img, size)
    n_img.convert()
    return n_img
