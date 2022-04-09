import sys
import pygame
from utils import *
from enemies import Soldier, Zombie
from tilemap import TileMap
import random

pygame.init()

cell_size = 23 # Best for small screen size
width, height = cell_size * 55, cell_size * 30
DISPLAY = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("Save Ukraine")
clock = pygame.time.Clock()

pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))

tilemap = TileMap("assets/tileset/map.tmx")
road = tilemap.get_layer(2)
blocked = tilemap.get_layer(1)
mouse_file = "assets/images/mouse.png"


class Level:
	def __init__(self, DISPLAY, Clock):
		self.bg = tilemap.make_surface()
		self.scale = cell_size / 32

		self.wave = {
			"soldiers": 50,
			"robots": 0,
			"zombies": 50,
			"zombie-robots": 0
		}

		self.enemies = []

		self.last_spawned = pygame.time.get_ticks()
		self.spawn_wait_time = 100
		self.rand_pause = 0

		self.mouse = load_img(mouse_file)
		self.mouse_rect = self.mouse.get_rect()

		self._resize_images()

	def _resize_images(self):
		global width, height, cell_size
		self.bg = transform_img(tilemap.make_surface(), (cell_size*40, height))
		self.mouse = transform_img(mouse_file, self.scale)
		self.mouse_rect = self.mouse.get_rect()

	def play(self):
		global cell_size, width, height, DISPLAY, clock
		run = True

		while run:
			DISPLAY.blit(self.bg, (0, 0))
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

					DISPLAY = pygame.display.set_mode(
						(width, height), pygame.RESIZABLE)
					self._resize_images()

			to_remove = []
			for enemy in self.enemies:
				is_dead = enemy.update(cell_size)
				enemy.render(DISPLAY)
				if is_dead:
					to_remove.append(enemy)

			for enemy in to_remove:
				self.enemies.remove(enemy)
			
			if pygame.time.get_ticks() - self.last_spawned > self.spawn_wait_time + self.rand_pause:
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

			DISPLAY.blit(self.mouse, self.mouse_rect.topleft)
			pygame.display.update()
			clock.tick(60)


level = Level(DISPLAY, clock)

if __name__ == "__main__":
	level.play()
	pygame.quit()
	sys.exit()
