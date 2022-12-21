import pygame
import pygame as pg
import os
from PIL import Image
import random
import math
import time
import numpy as np
import random
import matplotlib.pyplot as plt  # plotting libraries
import matplotlib.patches as patches
# from pygame.math import Vector2
pygame.font.init()

WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pilots Showdown")

# Load images
RED_SPACE_SHIP = pygame.image.load(
    os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(
    os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(
    os.path.join("assets", "pixel_ship_blue_small.png"))

# Player player
YELLOW_SPACE_SHIP = pygame.image.load(
    os.path.join("assets", "pixel_ship_yellow_crop_ps.png"))

# Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(
    os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(
    os.path.join("assets", "pixel_laser_yellow_new.png"))
MEGATRON = pygame.image.load(os.path.join("assets", "megatron.png"))
# Background
BG = pygame.transform.scale(pygame.image.load(
    os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))


class Laser:
    def __init__(self, x, y, angle, img):
        self.x = x
        self.y = y
        self.img = img
        self.angle = angle
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel * math.cos(math.radians(self.angle))
        self.x += vel * math.sin(math.radians(self.angle))

    def off_screen(self, height):
        return not (self.y <= height and self.y >= 0)

    def collision(self, obj):
        # if(self.img==MEGATRON):
        #     for las in obj:
        #         if(las!=MEGATRON):
        #             collide(self, las)
        return collide(self, obj)


class Ship:
    COOLDOWN = 30

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        # self.image_clean = (self.ship_img).copy()
        self.laser_img = None
        # self.rotation = 0
        self.lasers = []
        self.cool_down_counter = 0
        # self.offset = Vector2(50, 0)  # We shift the sprite 50 px to the right.
        self.angle = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def retalllasers(self):
        return self.lasers

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self, string, x, y, abl):
        if (type(abl) != str):
            angul = abl
        else:
            angul = self.angle
        if self.cool_down_counter == 0:
            if (string == 'normal'):
                laser = Laser(self.x, self.y, angul, self.laser_img)
            elif (string == 'megatron'):
                laser = Laser(x, y, angul, MEGATRON)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

    def rotate(self, angle):
        self.angle += angle
        colorImage = Image.open("assets/pixel_ship_yellow_crop_ps.png")
        rotated = colorImage.rotate(self.angle)
        self.ship_img = pygame.image.fromstring(
            rotated.tobytes(), rotated.size, rotated.mode)

    def laser_remover(self, laser):
        if (laser in self.lasers):
            self.lasers.remove(laser)
###############################################
"""Quadtree Implementation in Python."""


RECTANGLES = []
POINTS=[]

class Point:
    """Properties of a point."""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    # To make our object work with print function
    def __repr__(self):
        return f'{{"x": {self.x}, "y": {self.y}}}'


class Rectangle:
    """Creating a Rectangle."""

    def __init__(self, x, y, w, h):
        """Properties of the Rectangle."""
        self.x = x  # coordinates of corner
        self.y = y
        self.w = w  # width
        self.h = h  # height
        self.points = []  # list to store the contained points

    # To print boundary of this function
    def __repr__(self):
        return f'({self.x}, {self.y}, {self.w}, {self.h})'

    def contains(self, point):
        check_x = self.x < point.x <= self.x + self.w
        check_y = self.y < point.y <= self.y + self.h
        return check_x and check_y

    def insert(self, point):
        if not self.contains(point):
            return False

        self.points.append(point)
        return True


class Quadtree:
    """Creating a quadtree."""

    def __init__(self, boundary, capacity):
        """Properties for a quadtree."""
        self.boundary = boundary  # object of class Rectangle
        self.capacity = capacity  # 4
        self.divided = False  # to check if the tree is divided or not
        self.northeast = None
        self.southeast = None
        self.northwest = None
        self.southwest = None

    def subdivide(self):
        """Dividing the quadtree into four sections."""
        x, y, w, h = self.boundary.x, self.boundary.y, self.boundary.w, self.boundary.h

        north_east = Rectangle(x + w / 2, y, w / 2, h / 2)
        self.northeast = Quadtree(north_east, self.capacity)

        south_east = Rectangle(x + w / 2, y + h / 2, w / 2, h / 2)
        self.southeast = Quadtree(south_east, self.capacity)

        south_west = Rectangle(x, y + h / 2, w / 2, h / 2)
        self.southwest = Quadtree(south_west, self.capacity)

        north_west = Rectangle(x, y, w / 2, h / 2)
        self.northwest = Quadtree(north_west, self.capacity)
        self.divided = True

        for i in self.boundary.points:
            self.northeast.insert(i)
            self.southeast.insert(i)
            self.northwest.insert(i)
            self.southwest.insert(i)

    def insert(self, point):
        # If this major rectangle does not contain the point no need to check subdivided rectangle
        if not self.boundary.contains(point):
            return

        if len(self.boundary.points) < self.capacity:
            self.boundary.insert(point)  # add the point to the list if the length is less than capacity
        else:
            if not self.divided:
                self.subdivide()

            self.northeast.insert(point)
            self.southeast.insert(point)
            self.southwest.insert(point)
            self.northwest.insert(point)
    def collide(self):
        global RECTANGLES,POINTS
        if self.divided is False and len(self.boundary.points):
            # print(self.boundary)
            # print(self.boundary.points)
            RECTANGLES.append(self.boundary)
            POINTS.append(self.boundary.points)
        else:
            if self.northeast is not None:
                self.northeast.collide()
            if self.southeast is not None:
                self.southeast.collide()
            if self.northwest is not None:
                self.northwest.collide()
            if self.southwest is not None:
                self.southwest.collide()
        return Point


                        
class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def laser_remover(self, laser):
        self.lasers.remove(laser)

    def retalllasers(self):
        return self.lasers

    def megatron_attack_quad_tree(self, enemies):
        enemy_lasers = []
        our_lasers = []
        for laser in self.lasers:
            our_lasers.append(laser)
        for enemy in enemies:
            for lasers in enemy.retalllasers():
                if (lasers.img != MEGATRON):
                    temp_tuple = (lasers, enemy)
                    enemy_lasers.append(temp_tuple)

        # Main quad tree starts
        Q=Quadtree(Rectangle(0,0,WIDTH,HEIGHT),4)
        for laser in our_lasers:
            if (laser.img == MEGATRON):  # The laser which is megatron laser only cancels opposite laser
                RECTANGLES.append(Rectangle(laser.x, laser.y, 45, 45))
        for enemy_laser in enemy_lasers:
            enemy_name = enemy_laser[1]
            enemy_name_laser = enemy_laser[0]
            Q.insert(Point(enemy_name_laser.x, enemy_name_laser.y))
        Q.collide()
        # implement quad tree for removal of enemy lasers and laser#
        # Ends here

        
        for laser in our_lasers:
            if (laser.img == MEGATRON):  # The laser which is megatron laser only cancels opposite laser
                for enemy_laser in enemy_lasers:
                    enemy_name = enemy_laser[1]
                    enemy_name_laser = enemy_laser[0]
                    if (abs(enemy_name_laser.x-laser.x) <= 45 and abs(enemy_name_laser.y-laser.y) <= 45):
                        # print(enemy_name_laser.x,
                        #       enemy_name_laser.y, laser.x, laser.y)
                        enemy_name.laser_remover(enemy_name_laser)
            else:
                for enemy_laser in enemy_lasers:
                    enemy_name = enemy_laser[1]
                    enemy_name_laser = enemy_laser[0]
                    if (abs(enemy_name_laser.x-laser.x) <= 10 and abs(enemy_name_laser.y-laser.y) <= 10):
                        # print(enemy_name_laser.x,
                        #       enemy_name_laser.y, laser.x, laser.y)
                        enemy_name.laser_remover(enemy_name_laser)
                        self.laser_remover(laser)
                    

    def move_lasers(self, vel, objs):
        if not (self.laser_img == MEGATRON):
            self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser.img == MEGATRON:
                            oldx = laser.x
                            oldy = laser.y
                            laser.x = self.x
                            laser.y = self.y
                            laser.angle = -7.5
                            # self.shoot('megatron',oldx-5,oldy,laser.angle+17.5)
                            self.shoot('megatron', self.x, self.y, 7.5)
                            # self.shoot('megatron',self.x,self.y,-17.5)
                            # self.shoot('megatron',oldx+5,oldy,laser.angle+17.5)
                            # self.lasers.remove(laser)
                        elif laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0),
                         (self.x-5, self.y + 90 + 10, 100, 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x-5, self.y +
                         90 + 10, 100 * (self.health/self.max_health), 10))


class Enemy(Ship):
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel, a, b):
        if (self.ship_img == GREEN_SPACE_SHIP):
            if (b > self.x):
                self.x += vel*1.5
            elif (b < self.x):
                self.x -= vel*1.5
            self.y = 20
        else:
            self.y += vel
            if (self.y > a and self.ship_img == BLUE_SPACE_SHIP):
                self.y += vel

    def shoot(self, a, b):
        if self.cool_down_counter == 0:
            ang = 0
            if (((self.y < a)) and self.laser_img == RED_LASER):
                ang = (b-self.x)/abs(a-self.y)
            laser = Laser(self.x-20, self.y,
                          math.degrees(math.tanh(ang)), self.laser_img)
            # print(self.y-a,self.x-b,math.degrees(math.tanh(ang)))
            self.lasers.append(laser)
            self.cool_down_counter = 1


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("GAMEIT", 50)
    lost_font = pygame.font.SysFont("GAMEIT", 60)
    Megatron = 2
    enemies = []
    wave_length = 5
    enemy_vel = 1
    # tic=time.time()
    player_vel = 5
    laser_vel = 5

    player = Player(300, 630)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_window():
        WIN.blit(BG, (0, 0))
        # draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))
        megatron_label = main_font.render(
            f"Megatron: {Megatron}", 1, (255, 255, 255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        WIN.blit(megatron_label, (WIDTH - megatron_label.get_width() - 10, 700))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        if lost:
            # toc=time.time()
            # if(tic<1):
            #     talk=0
            # talk=max(toc-tic,talk)
            # tic=toc
            lost_label = lost_font.render("You Lost!!", 1, (255, 255, 255))
            # score = main_font.render(
            #     f"Score: {talk}", 1, (255, 255, 255))

            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))
            # WIN.blit(score, (WIDTH/2 - score.get_width()/2, 450))

        pygame.display.update()
    tikitiki = time.time()
    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue
        if len(enemies) == 0:
            player.health *= 1.5
            if (player.health > 100):
                player.health = 100
            level += 1
            Megatron += level//3
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(
                    50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0:  # left
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH:  # right
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0:  # up
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT:  # down
            player.y += player_vel
        if keys[pygame.K_u] and player_vel > 2:
            player_vel -= 2
        if keys[pygame.K_i] and player_vel < 15:
            player_vel += 2
        if keys[pygame.K_e]:
            player.rotate(-3)
        if keys[pygame.K_q]:
            player.rotate(3)
        if (keys[pygame.K_m]):
            tokitoki = time.time()
            if (Megatron > 0 and tokitoki-tikitiki > 1.5):
                player.shoot('megatron', player.x, player.y, 0)
                # player.shoot('megatron',player.x,player.y,7.5)
                # player.shoot('megatron',player.x,player.y,-7.5)

                Megatron -= 1
                tikitiki = tokitoki
        if keys[pygame.K_SPACE]:
            player.shoot('normal', player.x, player.y, 'temp')
        # total_las=[]
        for enemy in enemies[:]:
            enemy.move(enemy_vel, player.y, player.x)
            enemy.move_lasers(laser_vel, player)
            # for las in enemy.lasers:
            # total_las.append(las)
            if random.randrange(0, 2*60) == 1:
                enemy.shoot(player.y, player.x)

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)
        player.move_lasers(-laser_vel, enemies)
        player.megatron_attack_quad_tree(enemies)


def main_menu():
    title_font = pygame.font.SysFont("GAME_IT", 34)
    run = True
    while run:
        WIN.blit(BG, (0, 0))
        title_label_1 = title_font.render(
            "Press mouse to begin", 1, (255, 255, 255))
        title_label_2 = title_font.render(
            "I button to increase speed", 1, (255, 255, 255))
        title_label_3 = title_font.render(
            "U button to decrease speed", 1, (255, 255, 255))
        title_label_4 = title_font.render(
            "Default buttons- A,W,S,D,Q,E", 1, (255, 255, 255))
        title_label_5 = title_font.render(
            "Press M for megatron laser", 1, (255, 255, 255))
        title_label_6 = title_font.render(
            "Discover Other mechanics Yourself!!", 1, (255, 255, 255))
        WIN.blit(title_label_1, (WIDTH/2 - title_label_1.get_width()/2, 250))
        WIN.blit(title_label_2, (WIDTH/2 - title_label_2.get_width()/2, 400))
        WIN.blit(title_label_6, (WIDTH/2 - title_label_6.get_width()/2, 500))
        WIN.blit(title_label_3, (WIDTH/2 - title_label_3.get_width()/2, 350))
        WIN.blit(title_label_4, (WIDTH/2 - title_label_4.get_width()/2, 450))
        WIN.blit(title_label_5, (WIDTH/2 - title_label_5.get_width()/2, 300))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()


if __name__ == "__main__":
    main_menu()
