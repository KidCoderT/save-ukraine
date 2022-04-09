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

pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))

tilemap = TileMap("assets/tileset/map.tmx")
road = tilemap.get_layer(2)
blocked = tilemap.get_layer(1)


class Level:
	def __init__(self, DISPLAY, Clock):
		self.bg = tilemap.make_surface()
		self.scale = 1.0

		self.mouse_img = {
			"okay_spot": load_img("assets/images/mouse.png"),
			"danger_spot": load_img("assets/images/mouse-red.png"),
		}

	def _resize_images(self):
		global width, height
		self.bg = transform_img(self.bg, (width, height))
		self.mouse_img["okay_spot"] = transform_img(
			self.mouse_img["okay_spot"], (cell_size * 2, cell_size * 2))
		self.mouse_img["danger_spot"] = transform_img(
			self.mouse_img["danger_spot"], (cell_size * 2, cell_size * 2))

	def play(self):
		global cell_size, width, height, DISPLAY, clock
		run = True

		while run:
			DISPLAY.blit(self.bg, (0, 0))
			mx, my = pygame.mouse.get_pos()

			try:
				position_okay = not any(
					[
						self.spot_available(my // cell_size, mx // cell_size),
						self.spot_available(
							my // cell_size + 1, mx // cell_size),
						self.spot_available(
							my // cell_size, mx // cell_size + 1),
						self.spot_available(
							my // cell_size + 1, mx // cell_size + 1),
					]
				)
			except:
				position_okay = True

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False
				if event.type == pygame.VIDEORESIZE:
					cell_size = event.w // 40
					width, height = cell_size * 40, cell_size * 30
					self.scale = cell_size / 32

					DISPLAY = pygame.display.set_mode(
						(width, height), pygame.RESIZABLE)
					self._resize_images()

			m = self.mouse_img["okay_spot"]
			if not position_okay:
				m = self.mouse_img["danger_spot"]
			DISPLAY.blit(m, ((mx // cell_size) * cell_size,
							 (my // cell_size) * cell_size))

			pygame.display.update()
			clock.tick(60)

	def spot_available(self, y, x):
		return road[y][x] == 1 or blocked[y][x] == 1


level = Level(DISPLAY, clock)

if __name__ == "__main__":
	level.play()
	pygame.quit()
	sys.exit()
