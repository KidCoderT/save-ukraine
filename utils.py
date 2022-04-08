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


def draw_bg(offset, surf, width):
    for i in range(40):
        pygame.draw.line(
            surf,
            (46, 204, 113),
            (-10, int(i * 50 + offset - 20)),
            (width + 10, int(i * 50 - 110 + offset)),
            25,
        )
