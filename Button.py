import pygame


class Button:
    def __init__(self, screen, w, h, sound=None):
        self.width = w
        self.height = h
        self.inactive_clr = (0, 0, 255)
        self.active_clr = (100, 100, 210)
        self.screen = screen
        self.sound = sound

    def draw(self, x, y, msg, action=None, font_size=30):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(self.screen, self.active_clr, (x, y, self.width, self.height))

            if click[0] == 1:
                if self.sound is not None:
                    pygame.mixer.Sound.play(self.sound)
                    pygame.time.delay(300)
                if action is not None:
                    print(0)
                    action()

        else:
            pygame.draw.rect(self.screen, self.inactive_clr, (x, y, self.width, self.height))
        self._print_text(msg=msg, x=x, y=y, font_size=font_size)

    def _print_text(self, msg, x, y, font_color=(0, 0, 0), font_type=pygame.font.match_font('verdana'), font_size=30):
        font_type = pygame.font.Font(font_type, font_size)
        text = font_type.render(msg, True, font_color)
        text_size = text.get_size()
        blit_pos = (x + (self.width - text_size[0]) // 2, y + (self.height - text_size[1]) // 2)
        self.screen.blit(text, blit_pos)
