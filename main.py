import sys
import pygame
from utils import transform_img, load_img
from tilemap import TileMap


class Main:
    def __init__(self):
        pygame.init()

        self.cell_size = 32
        self.width, self.height = self.cell_size * 40, self.cell_size * 30
        self.DISPLAY = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        pygame.display.set_caption("Save Ukraine")
        self.clock = pygame.time.Clock()

        self.background_offset = 0

    def _resize_images(self):
        pass

    def mainloop(self):
        run = True

        while run:
            self.DISPLAY.fill((44, 196, 108))

            self.background_offset = (self.background_offset + 0.50) % 30
            for i in range(50):
                pygame.draw.line(
                    self.DISPLAY,
                    (46, 204, 113),
                    (-10, int(i * 30 + self.background_offset - 20)),
                    (self.width + 10, int(i * 30 - 110 + self.background_offset)),
                    15,
                )

            mx, my = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.VIDEORESIZE:
                    self.cell_size = event.w // 40
                    self.width, self.height = self.cell_size * 40, self.cell_size * 30
                    self.scale = self.cell_size / 32

                    self.DISPLAY = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
                    self._resize_images()

            pygame.display.update()
            self.clock.tick(60)

    @property
    def cx(self):
        return self.width / 2

    @property
    def cy(self):
        return self.height / 2


if __name__ == "__main__":
    main = Main()
    main.mainloop()
    pygame.quit()
    sys.exit()
