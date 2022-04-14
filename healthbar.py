import pygame


class BasicHealthBar:
    def __init__(self, max_width, max_height, max_value, cx, cy, scale, color):
        self.current_value = max_value
        self.max_value = max_value

        self.og_size = {"width": max_width, "height": max_height}
        self.og_pos = {"x": cx, "y": cy}

        self.width = max_width * scale
        self.height = max_height * scale

        self.scale = scale

        self.bg_rect: pygame.Rect = pygame.Rect(0, 0, self.width, self.height)
        self.bg_rect.centerx = self.og_pos["x"]
        self.bg_rect.centery = self.og_pos["y"]

        self.color = color

    def update_values(self, new_value, change=False):
        if change is True:
            self.current_value += new_value
        else:
            self.current_value = new_value

    def render(self, surface, scale):
        if self.scale != scale:
            self.width = self.og_size["width"] * scale
            self.height = self.og_size["height"] * scale
            self.bg_rect = pygame.Rect(0, 0, self.width, self.height)
            self.bg_rect.centerx = self.og_pos["x"] * scale
            self.bg_rect.centery = self.og_pos["y"] * scale
            self.scale = scale

        pygame.draw.rect(surface, (190, 190, 190), self.bg_rect)

        percent = self.current_value / self.max_value
        bar = pygame.Rect(
            self.bg_rect.x,
            self.bg_rect.y,
            self.width * percent,
            self.bg_rect.height,
        )

        pygame.draw.rect(surface, self.color, bar)
        pygame.draw.rect(surface, (0, 0, 0), self.bg_rect, width=int(5 * self.scale))


# TODO: finish this
class AnimHealthBar(BasicHealthBar):
    def __init__(
        self, max_width, max_height, max_value, cx, cy, scale, color, change_speed
    ):
        super().__init__(max_width, max_height, max_value, cx, cy, scale, color)
        self.change_speed = change_speed
        self.ui_value = self.current_value

    def render(self, surface, scale):
        if self.scale != scale:
            self.width = self.og_size["width"] * scale
            self.height = self.og_size["height"] * scale
            self.bg_rect = pygame.Rect(0, 0, self.width, self.height)
            self.bg_rect.centerx = self.og_pos["x"] * scale
            self.bg_rect.centery = self.og_pos["y"] * scale
            self.scale = scale

        pygame.draw.rect(surface, (190, 190, 190), self.bg_rect)

        self.ui_value += (
            self.change_speed
            if self.current_value > self.ui_value
            else -self.change_speed
        )
        percent = self.ui_value / self.max_value
        bar = pygame.Rect(
            self.bg_rect.x,
            self.bg_rect.y,
            self.width * percent,
            self.bg_rect.height,
        )
        pygame.draw.rect(surface, (250, 100, 100), bar)

        percent = self.current_value / self.max_value
        bar = pygame.Rect(
            self.bg_rect.x,
            self.bg_rect.y,
            self.width * percent,
            self.bg_rect.height,
        )

        pygame.draw.rect(surface, self.color, bar)
        pygame.draw.rect(surface, (0, 0, 0), self.bg_rect, width=int(5 * self.scale))
