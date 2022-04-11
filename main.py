import sys
import pygame
from utils import *
from enemies import Soldier, Zombie
from tilemap import TileMap
from healthbar import BasicHealthBar
import random

pygame.init()

cell_size = 23  # Best for small screen size
width, height = cell_size * 55, cell_size * 30
DISPLAY = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("Save Ukraine")
clock = pygame.time.Clock()

pygame.mouse.set_cursor(
    (8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0)
)

tilemap = TileMap("assets/tileset/map.tmx")
road = tilemap.get_layer(2)
blocked = tilemap.get_layer(1)
mouse_file = "assets/images/mouse.png"


class Level:
    def __init__(self, DISPLAY, Clock):
        self.bg = tilemap.make_surface()
        self.scale = cell_size / 32

        self.wave = {"soldiers": 50, "robots": 0, "zombies": 50, "zombie-robots": 0}

        self.enemies: list[Soldier | Zombie] = []

        self.last_spawned = pygame.time.get_ticks()
        self.spawn_wait_time = 100
        self.rand_pause = 0

        self.mouse = load_img(mouse_file)
        self.mouse_rect = self.mouse.get_rect()
        self.DISPLAY = pygame.Surface((cell_size * 40, cell_size * 30))

        # Info Place
        self.info_rect = pygame.Rect(cell_size * 40, 0, cell_size * 15, cell_size * 30)
        self.bg_offset = 0

        self.barrier_health = BasicHealthBar(
            32 * 15 * 0.9, 32 * 15 * 0.9 * 0.14, 500, 32 * 47.5, 50, 1, (38, 238, 83)
        )

        self._resize_images()

    def _resize_images(self):
        global width, height, cell_size
        self.bg = transform_img(tilemap.make_surface(), (cell_size * 40, height))
        self.mouse = transform_img(mouse_file, self.scale)
        self.mouse_rect = self.mouse.get_rect()

        self.info_rect.x = cell_size * 40
        self.info_rect.width = cell_size * 15
        self.info_rect.height = cell_size * 30

        self.DISPLAY = pygame.Surface((cell_size * 40, cell_size * 30))

    def play(self):
        global cell_size, width, height, DISPLAY, clock
        run = True

        while run:
            self.DISPLAY.blit(self.bg, (0, 0))
            mx, my = pygame.mouse.get_pos()
            self.mouse_rect.centerx = mx
            self.mouse_rect.centery = my

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.VIDEORESIZE:
                    cell_size = event.w // 55
                    width, height = cell_size * 55, cell_size * 30
                    self.scale = cell_size / 32

                    DISPLAY = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                    self._resize_images()

            to_remove = []
            for enemy in self.enemies:
                report = enemy.update(cell_size)
                enemy.render(self.DISPLAY)
                if report is not None:
                    if report == "hit":
                        self.barrier_health.update_values(
                            -enemy.barrier_damage, change=True
                        )
                    to_remove.append(enemy)

            for enemy in to_remove:
                self.enemies.remove(enemy)

            if (
                pygame.time.get_ticks() - self.last_spawned
                > self.spawn_wait_time + self.rand_pause
            ):
                if sum(self.wave.values()) > 0:
                    remaining_spawns = {k: v for k, v in self.wave.items() if v > 0}
                    key = random.choice(list(remaining_spawns.keys()))
                    if key == "soldiers":
                        self.enemies.append(Soldier())
                    elif key == "zombies":
                        self.enemies.append(Zombie())
                    self.wave[key] -= 1
                self.last_spawned = pygame.time.get_ticks()
                self.rand_pause = random.randint(-10, 200)

            DISPLAY.blit(self.DISPLAY, (0, 0))
            pygame.draw.rect(DISPLAY, (36, 175, 66), self.info_rect)
            pygame.draw.line(
                DISPLAY,
                (0, 0, 0),
                (cell_size * 40, -5),
                (cell_size * 40, height + 5),
                int(self.scale * 5),
            )

            # total_healthbar_width = self.info_rect.width * 0.90
            # healthbar_bg = pygame.Rect(
            #     0, 0, total_healthbar_width, total_healthbar_width * 0.14
            # )
            # healthbar_bg.centerx = self.info_rect.centerx
            # healthbar_bg.centery = int(50 * self.scale)

            # health_percent = 94 / 100
            # healthbar_health = pygame.Rect(
            #     healthbar_bg.x,
            #     healthbar_bg.y,
            #     total_healthbar_width * health_percent,
            #     healthbar_bg.height,
            # )

            # pygame.draw.rect(DISPLAY, (255, 255, 255), healthbar_bg)
            # pygame.draw.rect(DISPLAY, (38, 238, 83), healthbar_health)
            # pygame.draw.rect(DISPLAY, (0, 0, 0), healthbar_bg, int(5 * self.scale))

            self.barrier_health.render(DISPLAY, self.scale)

            DISPLAY.blit(self.mouse, self.mouse_rect.topleft)
            pygame.display.update()
            clock.tick(60)


level = Level(DISPLAY, clock)

if __name__ == "__main__":
    level.play()
    pygame.quit()
    sys.exit()
