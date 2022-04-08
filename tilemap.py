import pytmx
import pygame


class TileMap:
    def __init__(self, filename: str):
        tm = pytmx.load_pygame(filename)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.pytmxdata = tm
        self.tmxdata = pytmx.TiledMap(filename)

    def render(self, surface: pygame.Surface):
        ti = self.pytmxdata.get_tile_image_by_gid
        for layer in self.pytmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.pytmxdata.tilewidth,
                                            y * self.pytmxdata.tileheight))

    def get_layer(self, index: int):
        ti = self.tmxdata.get_tile_image_by_gid
        layer = list(self.pytmxdata.visible_layers)[index]
        if not isinstance(layer, pytmx.TiledTileLayer):
            return None

        data = [[None for x in range(40)] for y in range(30)]
        for x, y, gid, in layer:
            if ti(gid):
                data[y][x] = 1

        return data

    def make_surface(self):
        temp_surface = pygame.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface
