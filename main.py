import sys
import pygame
from utils import *
from enemies import Soldier, Zombie
from tilemap import TileMap
from healthbar import AnimHealthBar, BasicHealthBar
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
coin_img_file = "assets/images/coins.png"
killed_counter_img_file = "assets/images/KILLED.png"

UI_font = pygame.font.Font("assets/fonts/BungeeFont/Bungee-Regular.ttf", 32)


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

        self.shop_bg = pygame.Rect(
            0, 0, self.info_rect.width * 0.87, self.info_rect.height * 0.6
        )
        self.bg_offset = 0

        self.barrier_health = AnimHealthBar(
            32 * 15 * 0.95,
            32 * 15 * 0.9 * 0.14,
            500,
            32 * 47.5,
            50,
            1,
            (38, 238, 83),
            1,
        )

        self.ui_font_size = int(32 * self.scale)

        self.coin = load_img(coin_img_file)
        self.coin_icon_rect = self.coin.get_rect()
        self.money = 0

        self.killed_icon = load_img(killed_counter_img_file)
        self.killed_icon_rect = self.killed_icon.get_rect()
        self.killed = 0

        self._resize_images()

    def _resize_images(self):
        global width, height, cell_size
        self.bg = transform_img(tilemap.make_surface(), (cell_size * 40, height))
        self.mouse = transform_img(mouse_file, self.scale)
        self.mouse_rect = self.mouse.get_rect()

        self.info_rect.x = cell_size * 40
        self.info_rect.width = cell_size * 15
        self.info_rect.height = cell_size * 30

        self.shop_bg.width = int(self.info_rect.width * 0.87)
        self.shop_bg.height = int(self.info_rect.height * 0.65)
        self.shop_bg.centerx = self.info_rect.centerx
        self.shop_bg.centery = int(self.info_rect.centery)

        self.ui_font_size = int(32 * self.scale)

        self.coin = transform_img(coin_img_file, self.scale)
        self.coin_icon_rect = self.coin.get_rect()

        self.killed_icon = transform_img(killed_counter_img_file, self.scale)
        self.killed_icon_rect = self.killed_icon.get_rect()

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

            # Info Panel ------------------------------------------
            pygame.draw.rect(DISPLAY, (36, 175, 66), self.info_rect)
            pygame.draw.line(
                DISPLAY,
                (0, 0, 0),
                (cell_size * 40, -5),
                (cell_size * 40, height + 5),
                int(self.scale * 5),
            )

            self.barrier_health.render(DISPLAY, self.scale)

            self.coin_icon_rect.centerx = int(self.info_rect.x + 50 * self.scale)
            self.coin_icon_rect.centery = int(
                self.barrier_health.bg_rect.bottom + 45 * self.scale
            )
            DISPLAY.blit(self.coin, self.coin_icon_rect.topleft)

            self.killed_icon_rect.x = int(self.coin_icon_rect.right + 130 * self.scale)
            self.killed_icon_rect.centery = self.coin_icon_rect.centery
            DISPLAY.blit(self.killed_icon, self.killed_icon_rect.topleft)

            # The Shop ----------------------------------------------------------------
            pygame.draw.rect(
                DISPLAY, (97, 95, 212), self.shop_bg, border_radius=int(40 * self.scale)
            )
            pygame.draw.rect(
                DISPLAY,
                (0, 0, 0),
                self.shop_bg,
                int(9 * self.scale),
                int(40 * self.scale),
            )

            # Panel Text -------------------------------------------------
            self.money_text = UI_font.render(
                ": " + str(self.money).rjust(4, "0"), True, (255, 255, 255)
            )
            self.money_text = transform_img(self.money_text, self.scale)

            self.money_text_rect = self.money_text.get_rect()
            self.money_text_rect.centery = self.coin_icon_rect.centery
            self.money_text_rect.x = int(self.coin_icon_rect.right + 8 * self.scale)
            DISPLAY.blit(self.money_text, self.money_text_rect.topleft)

            self.killed_text = UI_font.render(
                ": " + str(self.killed).rjust(3, "0"), True, (255, 255, 255)
            )
            self.killed_text = transform_img(self.killed_text, self.scale)

            self.killed_text_rect = self.killed_text.get_rect()
            self.killed_text_rect.centery = self.killed_icon_rect.centery
            self.killed_text_rect.x = int(self.killed_icon_rect.right + 8 * self.scale)
            DISPLAY.blit(self.killed_text, self.killed_text_rect.topleft)

            # The Mouse
            DISPLAY.blit(self.mouse, self.mouse_rect.topleft)
            pygame.display.update()
            clock.tick(60)


level = Level(DISPLAY, clock)

if __name__ == "__main__":
    level.play()
    pygame.quit()
    sys.exit()
