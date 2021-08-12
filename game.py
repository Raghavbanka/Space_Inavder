""" Authour: Raghav Banka. SpaceInvader"""

import random
import pygame
import math
from pygame.colordict import THECOLORS
from pygame import mixer

SCREEN_SIZE = (800, 600)
PLAYER_CORD = (400, 600)
PLAYER_IMG = pygame.image.load("battleship.png")
ENEMY_IMG = pygame.image.load("enemy1.png")
BACKGROUND_IMG = pygame.image.load("space_2.jpg")
BULLET = pygame.image.load("bullet.png")
ASTEROID = pygame.image.load("rock.png")
_FIRE_STATE = False


def initialise_screen(allowed=None) -> pygame.Surface:
    """ Initialize pygame and the display window."""
    if allowed is None:
        allowed = []
    pygame.display.init()
    pygame.font.init()
    pygame.mixer.init()
    scr = pygame.display.set_mode(SCREEN_SIZE)
    scr.fill(THECOLORS['black'])
    pygame.display.flip()

    pygame.event.clear()
    pygame.event.set_blocked(None)
    pygame.event.set_allowed([pygame.QUIT] + allowed)

    return scr


class Bullet:
    """ Class representing the bullet movement"""
    x: int
    y: int

    def __init__(self) -> None:
        self.x = 0
        self.y = 0

    def pos_change(self) -> None:
        """ change the position of bullet"""
        self.y -= 10

    def display(self) -> None:
        """ Display the image of bullet"""
        screen.blit(BULLET, (self.x, self.y))


class SpaceShip:
    """ Class representing the spaceship"""
    x: int
    y: int
    bullet: Bullet
    fire_state: bool

    def __init__(self) -> None:
        self.x = 350
        self.y = 510
        self.bullet = Bullet()
        self.fire_state = False

    def initialise_bullet(self) -> None:
        """ Initialise the postion of the bullet"""
        self.bullet.x = self.x + 15
        self.bullet.y = self.y - 20

    def change_pos(self, ch: int) -> None:
        """ Function to change the position of spaceship"""
        self.x += ch
        if self.x <= 0:
            self.x = 0
        if self.x >= 735:
            self.x = 735

    def bullet_fire_state(self) -> None:
        """ firestate of bullet"""
        if self.fire_state:
            self.change_bullet()
            self.display_bullet()
            if self.bullet.y <= 0:
                self.fire_state = not self.fire_state

    def display_bullet(self) -> None:
        """ display bullet image"""
        self.bullet.display()

    def change_bullet(self) -> None:
        """ change bullet position"""
        self.bullet.pos_change()

    def display_ship(self) -> None:
        """ display ship"""
        screen.blit(PLAYER_IMG, (self.x, self.y))


class Asteroid:
    """ Class representing the asteroids of game"""
    x: int
    y: int

    def __init__(self) -> None:
        self.x = random.randint(150, 650)
        self.y = 20

    def movement(self) -> None:
        """ To stimulate the movement of asteroid
        """
        self.y += 4

    def display(self) -> None:
        """ Function to display the asteroid"""
        screen.blit(ASTEROID, (self.x, self.y))

    def collision(self, ship: SpaceShip) -> bool:
        """ Function to detect collison"""
        if abs(self.x - ship.x) < 55 and abs(self.y - ship.y) < 64:
            return True
        return False

    def bullet_collision(self, bullet: Bullet) -> bool:
        """ Function to detect collison"""
        if abs(self.x - bullet.x + 20) < 40 and abs(self.y - bullet.y) < 20:
            return True
        return False


class List_of_Asteroid:
    """ Class to manage random generation of asteroids"""
    num_asteroids: int
    list_of_asteroids: list[Asteroid]

    def __init__(self) -> None:
        self.list_of_asteroids = []
        self.num_asteroids = 0

    def generate(self) -> None:
        """ Function to generate list of asteroids
        """
        num = random.randint(0, 250)
        if num < 1:
            aster = Asteroid()
            self.num_asteroids += 1
            self.list_of_asteroids.append(aster)

    def check_collision(self, ship: SpaceShip) -> bool:
        """ Function to check if any asteroid collided"""
        for item in self.list_of_asteroids:
            if item.collision(ship):
                return True
        return False

    def check_bullet_collision(self, ship: SpaceShip) -> None:
        """ Function to check if any asteroid collided"""
        for item in self.list_of_asteroids:
            if item.bullet_collision(ship.bullet) and ship.fire_state:
                s = mixer.Sound("explosion.wav")
                s.set_volume(0.15)
                s.play()
                self.list_of_asteroids.remove(item)
                ship.fire_state = False

    def movement(self) -> None:
        """ Function to implement asteroid movement"""
        for item in self.list_of_asteroids:
            item.movement()
            if item.y >= 600:
                self.list_of_asteroids.remove(item)

    def display(self) -> None:
        """ Function to display the spaceships"""
        for item in self.list_of_asteroids:
            item.display()


class Enemy:
    """ Class representing an enemy of the game"""
    _pos: tuple
    fire_pos: tuple
    x: int
    y: int
    hit: bool
    num_asteroids: int
    ast: list

    def __init__(self) -> None:
        self._pos = (random.randint(50, 700), random.randint(60, 200))
        self._fire_pos = (0, 0)
        self.x = 4
        self.y = -38
        self.hit = False
        self.num_asteroids = 0
        self.ast = []

    def reposition(self) -> None:
        """ Repositioning of enemy after getting hit"""
        self._pos = (random.randint(150, 550), random.randint(60, 200))

    def collide(self, ship: SpaceShip) -> bool:
        """ Return whether the bullet collided with enemy"""
        dist = math.sqrt((self._pos[0] - ship.bullet.x + 30) ** 2 + (self._pos[1]
                                                                     - ship.bullet.y + 15) ** 2)
        if dist < 32:
            return True
        return False

    def movement(self) -> None:
        """Function to stimulate enemy movement"""
        x_pos, y_pos = self._pos
        x_pos += self.x
        if x_pos <= 0:
            if self.x < 0:
                self.x = -self.x
            y_pos -= self.y
        if x_pos >= 720:
            if self.x > 0:
                self.x = -self.x
            y_pos -= self.y
        self._pos = x_pos, y_pos

    def y_pos(self) -> int:
        """ Return y pos"""
        return self._pos[1]

    def display(self) -> None:
        """ Display enemy """
        screen.blit(ENEMY_IMG, self._pos)


screen = initialise_screen([pygame.KEYDOWN, pygame.KEYUP, pygame.K_SPACE])
var = True
change = 0
score = 0
list_of_enemy = []
for _ in range(0, 6):
    b = Enemy()
    list_of_enemy.append(b)
player = SpaceShip()
font = pygame.font.Font('freesansbold.ttf', 32)
asteroid = List_of_Asteroid()
mixer.music.load("background.wav")
pygame.mixer.music.set_volume(0.15)
mixer.music.play(-1)


while var:

    screen.fill(THECOLORS['black'])
    screen.blit(BACKGROUND_IMG, (0, 0))
    pygame.draw.line(screen, THECOLORS['black'], (0, 490), (800, 490), 5)
    text = font.render('Score : ' + str(score), True, THECOLORS['red'])
    text_rect = text.get_rect()
    text_rect.center = (700, 50)
    screen.blit(text, text_rect)

    for enemy in list_of_enemy:
        if not enemy.hit:
            enemy.hit = True
    for enemy in list_of_enemy:
        if enemy.y_pos() + 50 >= 490:
            var = False
    if asteroid.check_collision(player):
        var = False
    if var is False:
        pygame.mixer.music.stop()
        break
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            var = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                change = -5
            if event.key == pygame.K_RIGHT:
                change = 5
            if event.key == pygame.K_SPACE:
                if not player.fire_state:
                    sound = mixer.Sound("shoot.wav")
                    sound.set_volume(0.15)
                    sound.play()
                    player.fire_state = True
                    player.initialise_bullet()
                    player.display_bullet()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                change = 0

    asteroid.generate()
    player.change_pos(change)
    for enemy in list_of_enemy:
        enemy.movement()
    asteroid.movement()

    asteroid.check_bullet_collision(player)

    for enemy in list_of_enemy:
        if enemy.collide(player) and player.fire_state:
            sound = mixer.Sound("invaderkilled.wav")
            sound.set_volume(0.15)
            sound.play()
            score += 1
            player.fire_state = False
            enemy.reposition()
            enemy.hit = False

    player.bullet_fire_state()
    asteroid.display()
    player.display_ship()
    for enemy in list_of_enemy:
        if enemy.hit:
            enemy.display()
    pygame.display.update()

screen.blit(BACKGROUND_IMG, (0, 0))
mixer.Sound("ship_explosion.wav").play()
font2 = pygame.font.Font('freesansbold.ttf', 60)
text = font2.render('Game Over', True, THECOLORS['red'])
text2 = font.render("Your Score is " + str(score), True, THECOLORS['red'])
text_rect = text.get_rect()
text_rect_2 = text2.get_rect()
text_rect.center = (400, 250)
text_rect_2.center = (400, 325)
screen.blit(text, text_rect)
screen.blit(text2, text_rect_2)
pygame.display.update()
