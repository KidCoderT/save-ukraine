import pygame
from pygame.image import load


def load_img(filename: str):
    img = load(filename)
    img.convert()
    return img


def transform_img(img: pygame.surface.Surface | str, size: tuple | float):
    if isinstance(size, float) and isinstance(img, str):
        n_img = load_img(img)
        new_w = n_img.get_width() * size
        new_h = n_img.get_height() * size
        n_img = pygame.transform.scale(n_img, (new_w, new_h))
        n_img.convert()
        return n_img
    elif isinstance(size, float):
        n_img = img
        new_w = n_img.get_width() * size  # type: ignore
        new_h = n_img.get_height() * size  # type: ignore
        n_img = pygame.transform.scale(n_img, (new_w, new_h))  # type: ignore
        n_img.convert()
        return n_img

    n_img = pygame.transform.scale(img, size)  # type: ignore
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
