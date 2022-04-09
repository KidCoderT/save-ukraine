import pygame
from random import choice
from utils import transform_img, load_img

paths = [
    [
        (2, -2),
        (2, 25),
        (14, 25),
        (14, 27),
        (23, 27),
        (23, 16),
        (11, 16),
        (11, 4),
        (35, 4),
        (35, 10),
        (30, 10),
        (30, 27),
        (40, 27),
    ],
    [
        (1, -2),
        (1, 26),
        (13, 26),
        (13, 28),
        (24, 28),
        (24, 15),
        (12, 15),
        (12, 5),
        (34, 5),
        (34, 9),
        (29, 9),
        (29, 28),
        (40, 28),
    ],
    [
        (3, -2),
        (3, 24),
        (15, 24),
        (15, 26),
        (22, 26),
        (22, 17),
        (10, 17),
        (10, 3),
        (36, 3),
        (36, 11),
        (31, 11),
        (31, 26),
        (40, 26),
    ],
]


class Enemy:
    def __init__(self, speed, health, filename):
        self.path = choice(paths)
        self.next = 1
        self.cx, self.cy = self.path[0][0], self.path[0][1]
        self.speed = speed * 0.05
        self.image = load_img(filename)
        self.filename = filename
        self.image.convert()
        self.direction = "DOWN"
        self._ = -10
        self.frames = 10
        self.health = health
        self.tile_size = 32
        self.scale = 1.0

        self.damaged = False
        self.knockback = False

    def update(self, tile_size):
        if tile_size != self.tile_size:
            scale_percent = tile_size / 32

            img = transform_img(self.filename, scale_percent)
            self.scale = scale_percent
            self.tile_size = tile_size
            self.image = img
        try:
            inc = 0.2 if self.knockback else 0
            diff_x, diff_y = self.path[self.next][0] - self.cx, self.path[self.next][1] - self.cy
            if diff_x > 0:
                self.cx += self.speed - inc
                self.direction = "RIGHT"
            elif diff_x < 0:
                self.cx += -self.speed + inc
                self.direction = "LEFT"
            elif diff_y > 0:
                self.cy += self.speed - inc
                self.direction = "DOWN"
            else:
                self.cy += -self.speed + inc
                self.direction = "UP"

            if self.knockback:
                self.knockback = False

            min_ = 0.4
            if abs(self.cx - self.path[self.next][0]) <= min_ and abs(self.cy - self.path[self.next][1]) <= min_:
                self.cx = self.path[self.next][0]
                self.cy = self.path[self.next][1]
                self.next += 1

            if self.health < 1:
                return True
        except:
            return True

    def render(self, surf):
        image = self.image
        if self.direction == "UP":
            image = pygame.transform.rotate(image, 90 + self._)
        elif self.direction == "LEFT":
            image = pygame.transform.rotate(image, 180 + self._)
        elif self.direction == "DOWN":
            image = pygame.transform.rotate(image, -90 + self._)
        else:
            image = pygame.transform.rotate(image, 0 + self._)

        if self.damaged:
            try:
                image.fill((200, 100, 0, 100), special_flags=pygame.BLEND_RGB_MULT)
            except:
                self.damaged = False

        surf.blit(
            image,
            (
                (self.cx * self.tile_size) + self.scale * 16 - image.get_width() / 2,
                (self.cy * self.tile_size) + self.scale * 16 - image.get_height() / 2,
            ),
        )

        self.frames -= 1
        if self.frames <= 0:
            self._ *= -1
            self.frames = 10

    def damage(self, damage):
        self.health -= damage
        self.damaged = True
        self.knockback = True

    @property
    def x(self):
        return self.cx * self.tile_size

    @property
    def y(self):
        return self.cy * self.tile_size


class Zombie(Enemy):
    def __init__(self):
        super().__init__(speed=1.8, health=10, filename="assets/images/enemies/zombie.png")


class Soldier(Enemy):
    def __init__(self):
        super().__init__(speed=1.5, health=15, filename="assets/images/enemies/soldier.png")
