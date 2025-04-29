from pygame.image import load
from pygame.mixer import Sound
from config import *


def load_sound(name):
    path = f"Assets/Sounds/{name}.wav"
    return Sound(path)


def load_sprite(name, alpha=True):
    path = f"Assets/Sprites/{name}"
    sprite = load(path)
    if not alpha:
        return sprite.convert()
    else:
        return sprite.convert_alpha()


def rotate(img, pos, angle):
    w, h = img.get_size()
    img2 = pygame.Surface((w * 2, h * 2), pygame.SRCALPHA)
    img2.blit(img, (w - pos[0], h - pos[1]))
    return pygame.transform.rotate(img2, angle)


def denormalize(size, value):
    return round(size * value)


def denormalize2(sizex, sizey, valuex, valuey):
    return round(sizex * valuex), round(sizey * valuey)


def normalize(size, value):
    return round(value / size)


def normalize2(sizex, sizey, valuex, valuey):
    return round(valuex / sizex), round(valuey / sizey)


def isInBound(w, h, x, y):
    return (0 <= x <= w) and (0 <= y <= h)


def print_text(screen, msg, x, y, font_color=(0, 0, 0), font_type=pygame.font.match_font('verdana'), font_size=30):
    font_type = pygame.font.Font(font_type, font_size)
    msg = msg.split('\n')
    texts = [font_type.render(i, True, font_color) for i in msg]
    for i in enumerate(texts):
        screen.blit(i[1], (x, y + i[0] * font_size))
