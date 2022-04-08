import sys
import pygame
from utils import draw_bg, transform_img, load_img
from tilemap import TileMap

pygame.init()

cell_size = 32
width, height = cell_size * 40, cell_size * 30
DISPLAY = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("Save Ukraine")
clock = pygame.time.Clock()

tilemap = TileMap("assets/tileset/map.tmx")
road = tilemap.get_layer(2)
blocked = tilemap.get_layer(1)


class Level:
    def __init__(self, DISPLAY, Clock):
        self.bg = tilemap.make_surface()
        self.scale = 1.0

    def _resize_images(self):
        global width, height
        self.bg = transform_img(self.bg, (width, height))

    def play(self):
        global cell_size, width, height, DISPLAY, clock
        run = True

        while run:
            DISPLAY.blit(self.bg, (0, 0))

            mx, my = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.VIDEORESIZE:
                    cell_size = event.w // 40
                    width, height = cell_size * 40, cell_size * 30
                    self.scale = cell_size / 32

                    DISPLAY = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                    self._resize_images()

            pygame.display.update()
            clock.tick(60)


level = Level(DISPLAY, clock)

if __name__ == "__main__":
    level.play()
    pygame.quit()
    sys.exit()
