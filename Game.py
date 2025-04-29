import pygame.display

from utils import *
import random
from GunTower import GunTower
from Enemy import Enemy
from Button import Button


class Game:
    def __init__(self):
        self._init_pygame()
        self.bullets = []
        self.enemies = []
        self.bg = pygame.transform.scale(load_sprite("green.png", False), (WIDTH, HEIGHT))
        self.title = pygame.transform.scale(load_sprite("title.png", False), (WIDTH, HEIGHT))
        self.game_over_screen = pygame.transform.scale(load_sprite("game_over.png", False), (WIDTH, HEIGHT))
        self.win_screen = pygame.transform.scale(load_sprite('win.png', False), (WIDTH, HEIGHT))
        self.guntower = GunTower(denormalize2(WIDTH, HEIGHT, 0.96, 0.5), load_sprite("tankhead.png"), (0.55, 0.735),
                                 RATE_OF_FIRE, self.bullets.append, scale=denormalize2(WIDTH, HEIGHT, 0.1, 0.3))
        self.clock = pygame.time.Clock()
        self.tick = 0
        self.rotation = ROTATE_NONE
        self.shooting = SHOOTING_NONE
        self.music = load_sound("music")
        self.overheat_sound = load_sound("overheat")
        self.music.set_volume(0.4)
        self.music.play(-1)
        self.gameCondition = GAME_PAUSED

        self.heat_timer = 0

        self.score = 0
        self.lifes = LIFES

        self.time_remaining = TIME
        self.start_btn = Button(self.screen, 600, 100)
        self.help_btn = Button(self.screen, 600, 100)
        self.about_btn = Button(self.screen, 600, 100)
        self.exit_btn = Button(self.screen, 600, 100)

        pygame.time.set_timer(SPAWN_EVENT, 300)
        pygame.time.set_timer(COUNT_SECONDS, 1000)
        pygame.time.set_timer(COOLING_DOWN, 200)

    def _init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption('ee')

    def main_loop(self):
        if self.gameCondition == GAME_ACTIVE:
            self.tick = self.clock.tick(60)
            self._handle_input()
            self._process_game_logic()
            self._render()
        elif self.gameCondition == GAME_PAUSED:
            self._process_menu()
        elif self.gameCondition == GAME_LOST:
            self._process_game_end(self.game_over_screen, denormalize(WIDTH, 13/17), denormalize(HEIGHT, 2/9),
                                   (255, 0, 0))
        elif self.gameCondition == GAME_WIN:
            self._process_game_end(self.win_screen, denormalize(WIDTH, 1/700), denormalize(HEIGHT, 13/18), (0, 0, 0))

    def start_help(self):
        self._make_cutscene(HELP_TEXT, font_size=35)

    def start_about(self):
        self._make_cutscene(ABOUT_TEXT, font_size=35)

    def _process_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._close_application()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self._close_application()

        self.screen.blit(self.title, (0, 0))
        print_text(self.screen, msg="ESC - выйти из игры", x=denormalize(WIDTH, 0.80), y=denormalize(HEIGHT, 0.95),
                   font_size=25, font_color=(255, 255, 255))
        self.start_btn.draw(denormalize(WIDTH, 0.61), denormalize(HEIGHT, 0.15), 'Начать', font_size=50,
                            action=self.start_game)
        self.help_btn.draw(denormalize(WIDTH, 0.61), denormalize(HEIGHT, 0.30), 'Помощь', font_size=50,
                           action=self.start_help)
        self.help_btn.draw(denormalize(WIDTH, 0.61), denormalize(HEIGHT, 0.45), 'О нас', font_size=50,
                           action=self.start_about)
        self.exit_btn.draw(denormalize(WIDTH, 0.61), denormalize(HEIGHT, 0.60), 'ВЫХОД', font_size=50,
                           action=self._close_application)

        pygame.display.update()

    def _process_game_end(self, background, scorex, scorey, scorecolor=(255, 0, 0)):
        self.screen.blit(background, (0, 0))
        print_text(self.screen, f"Настреляли {self.score} зомби", font_color=scorecolor, x=scorex,
                   y=scorey)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._close_application()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_SPACE:
                    self._clear_game()
                    self.gameCondition = GAME_ACTIVE
                else:
                    self._clear_game()
                    self.gameCondition = GAME_PAUSED
        pygame.display.update()

    def start_game(self):
        self._make_cutscene(PREGAME_TEXT, 50)
        self.gameCondition = GAME_ACTIVE

    def spawn_enemy(self, x, y):
        self.enemies.append(Enemy((x, y), load_sprite('zombie_1.png'),
                                  min(max(ENEMY_SPEED_FLOOR, random.random()), ENEMY_SPEED_CEIL),
                                  scale=(ENEMY_WIDTH * 1.4, ENEMY_HEIGHT * 1.4),
                                  deathSound=load_sound('death'), cols=3, rows=1))

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == SPAWN_EVENT:
                self.spawn_enemy(0, random.randint(0, HEIGHT - ENEMY_HEIGHT))
            if event.type == COUNT_SECONDS:
                self.time_remaining -= 1
                if self.time_remaining <= 0:
                    self._make_cutscene(WINNING_TEXT, 50)
                    self.gameCondition = GAME_WIN
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.shooting = SHOOTING_ON
                    pygame.time.set_timer(HEAT_TIMER, 200)
            if event.type == COOLING_DOWN:
                self.heat_timer -= 0.1
                self.heat_timer = max(0, self.heat_timer)
            if event.type == HEAT_TIMER:
                self.heat_timer += 0.2
                if self.heat_timer > 4:
                    self.overheat_gun()
            if event.type == GUN_OVERHEATED:
                self.guntower.overheated = False
                pygame.time.set_timer(GUN_OVERHEATED, 0)
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.shooting = SHOOTING_NONE
                    pygame.time.set_timer(HEAT_TIMER, 0)
                    self.heat_timer = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._clear_game()
                    self.gameCondition = GAME_PAUSED

    def overheat_gun(self):
        self.overheat_sound.play()
        self.guntower.overheated = True
        self.heat_timer = 0
        pygame.time.set_timer(GUN_OVERHEATED, OVERHEAT_TIME)

    def _make_cutscene(self, text, font_size):
        self.screen.fill((0, 0, 0))
        print_text(screen=self.screen, x=0, y=0, msg=text, font_size=font_size, font_color=(255, 255, 255))
        print_text(screen=self.screen, x=denormalize(WIDTH, 0), y=denormalize(HEIGHT, 0.94),
                   msg='space чтобы продолжить',
                   font_size=20, font_color=(255, 255, 255))
        pygame.display.flip()
        wait = True
        while wait:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or \
                   (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    wait = False

    def _process_game_logic(self):
        self.guntower.rotate()
        self.guntower.cooldown += self.tick
        if self.shooting == SHOOTING_ON:
            self.guntower.shoot()

        for enemy in self.enemies:
            for bullet in self.bullets:
                if enemy.collides_with(bullet):
                    self.bullets.remove(bullet)
                    if enemy in self.enemies:
                        enemy.death()
                        self.enemies.remove(enemy)
                        self.score += 1
        for enemy in self.enemies:
            enemy.move(self.tick)
            if enemy.pos.x > WIDTH:
                self.enemies.remove(enemy)
                self.lifes -= 1
                if self.lifes <= 0:
                    self.gameCondition = GAME_LOST
                continue
            if not self.screen.get_rect().collidepoint(enemy.pos):
                self.enemies.remove(enemy)

        for bullet in self.bullets:
            bullet.move(self.tick)
            if not self.screen.get_rect().collidepoint(bullet.pos):
                self.bullets.remove(bullet)

    def _render(self):
        self.screen.blit(self.bg, (0, 0))
        self.guntower.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)

        print_text(screen=self.screen, msg=f'очков: {self.score}', x=denormalize(WIDTH, 0.02),
                   y=denormalize(HEIGHT, 0.01))
        print_text(screen=self.screen, msg=f'Оборона: {self.lifes}', x=denormalize(WIDTH, 0.85),
                   y=denormalize(HEIGHT, 0.01))
        print_text(screen=self.screen, msg=f'{self.time_remaining}', x=denormalize(WIDTH, 0.5),
                   y=denormalize(HEIGHT, 0.01), font_size=60)
        if self.heat_timer > 2.5:
            print_text(screen=self.screen, msg=f'ОСТОРОЖНО, ПЕРЕГРЕВ', x=denormalize(WIDTH, 0.02),
                       y=denormalize(HEIGHT, 0.05), font_size=30, font_color=(255, 0, 0))

        pygame.display.update()

    def _clear_game(self):
        self.enemies.clear()
        self.bullets.clear()
        self.score = 0
        self.lifes = LIFES
        self.time_remaining = TIME

    @staticmethod
    def _close_application():
        pygame.quit()
        quit()


def main():
    game = Game()
    while True:
        game.main_loop()


main()
