import pygame


WIDTH, HEIGHT = 1600, 900
ENEMY_WIDTH, ENEMY_HEIGHT = 180, 100
ENEMY_SPEED = 0.3
ENEMY_SPEED_FLOOR = 0.1
ENEMY_SPEED_CEIL = 0.23

RATE_OF_FIRE = 170

LIFES = 7


TIME = 90


SPAWN_EVENT = pygame.USEREVENT + 1
COUNT_SECONDS = pygame.USEREVENT + 2
HEAT_TIMER = pygame.USEREVENT + 3
GUN_OVERHEATED = pygame.USEREVENT + 4
COOLING_DOWN = pygame.USEREVENT + 5

OVERHEAT_TIME = 3000

ROTATE_NONE = 0
ROTATE_CLOCKWISE = 1
ROTATE_COUNTERCLOCKWISE = 2

SHOOTING_ON = 3
SHOOTING_NONE = 5


PREGAME_TEXT = "Задача: не пропускать монстров к границе \nдо прибытия помощи"
WINNING_TEXT = "Прилетела подмога, отличная работа!!!\nПора убираться...\n"
HELP_TEXT = "Управление - мышью (двигать - поворот пушки, ЛКМ - стрелять)\nЦель - не допустить существам достичь " \
            "правой границы определенное время.\nПулемет может перегреваться, если стрелять слишком долго, он не " \
            "будет стрелять \n3 секунды в этом случае.\n" \
            "Поэтому необходимо переодически отпускать ЛКМ"
ABOUT_TEXT = "Игра \"Стальные демоны\"\nСоздатель - Кондратьев Леонид (10А)\nПроект Pygame в Яндекс Лицей\n" \
             "Версия 1.0\n\nМузыка: Cheshyre - The Animal"


GAME_ACTIVE = 100
GAME_PAUSED = 101
GAME_LOST = 102
GAME_WIN = 103

BULLET_VELOCITY = 2
