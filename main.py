from Lava import Lava, lava_group
from coin import coin_group, Coin
from config import tile_size
import json
from door import Door, door_group
from random import randint
import pygame

pygame.init()
width = 800
height = 800
clock = pygame.time.Clock()
fps = 60
game_over = 0
level = 1
max_level = 4
lives = 3
score = 0

with open("levels/level1.json", "r") as file:
    world_data = json.load(file)

randomy = randint(0, height)
randomx = randint(0, width)

music_jump = pygame.mixer.Sound("music/jump.wav")
music_game_over = pygame.mixer.Sound("music/game_over.wav")
music_coin = pygame.mixer.Sound("music/coin.wav")


def draw_text(text, color, size, x, y):
    font = pygame.font.SysFont('Arial', size)
    img = font.render(text, True, color)
    display.blit(img, (x, y))


class Player:
    def __init__(self):
        self.image = pygame.image.load('images/player1.png')
        self.image = pygame.transform.scale(self.image, (35, 70))
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = height - 200
        self.gostimage = pygame.image.load('images/ghost.png')
        self.gravity = 0
        self.wight = self.image.get_width()
        self.height = self.image.get_height()
        self.jumped = True
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        self.direction = 0
        for num in range(1, 3):
            img_right = pygame.image.load(f'images/player{num}.png')
            img_right = pygame.transform.scale(img_right, (35, 70))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.image = self.images_right[self.index]

    def update(self):
        global lives
        global game_over
        x = 0
        y = 0
        walk_speed = 10
        if game_over == 0:
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False:
                self.gravity = -15
                self.jumped = True
                music_jump.play()
            if key[pygame.K_a]:
                x -= 5
                self.direction = -1
                self.counter += 1
            if key[pygame.K_d]:
                x += 5
                self.direction = 1
                self.counter += 1
            if self.counter > walk_speed:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                else:
                    self.image = self.images_left[self.index]

            self.gravity += 1
            if self.gravity > 10:
                self.gravity = 10
            y += self.gravity
            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x + x, self.rect.y, self.wight, self.height):
                    x = 0
                if tile[1].colliderect(self.rect.x, self.rect.y + y,
                                       self.wight, self.height):
                    if self.gravity < 0:
                        y = tile[1].bottom - self.rect.top
                        self.gravity = 0
                    elif self.gravity >= 0:
                        y = tile[1].top - self.rect.bottom
                        self.gravity = 0
                        self.jumped = False

            if self.rect.bottom > height:
                self.rect.bottom = height
            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over = -1
            if pygame.sprite.spritecollide(self, door_group, False):
                game_over = 1

        # self.gravity = 0
        self.rect.x += x
        self.rect.y += y

        # if lives == 0:
        #     game_over = -1
        if game_over == -1:
            # music_game_over.play()

            self.image = self.gostimage
            # if self.rect.y > 0:
            self.rect.y -= 5

        display.blit(self.image, self.rect)


def reset_level():
    froggy.rect.x = 100
    froggy.rect.y = height - 130
    lava_group.empty()
    door_group.empty()
    coin_group.empty()
    with open(f'levels/level{level}.json', 'r') as file:
        world_data = json.load(file)
    world = World(world_data)
    return world


class Button:
    def __init__(self, x, y, image):
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self):
        action = False
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
                # print("hello")
        display.blit(self.image, self.rect)
        return action


class World:
    def __init__(self, data):
        dirt_img = pygame.image.load("images/dirt.png")
        grass_img = pygame.image.load("images/grass.png")
        self.tile_list = []
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1 or tile == 2:
                    images = {1: dirt_img, 2: grass_img}
                    img = pygame.transform.scale(images[tile], (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                elif tile == 3:
                    lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                    lava_group.add(lava)
                elif tile == 5:
                    door = Door(col_count * tile_size, row_count * tile_size + (tile_size * 1.5))
                    door_group.add(door)
                elif tile == 6:
                    coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    coin_group.add(coin)
                col_count += 1
            row_count += 1

    def draw(self):
        for img, rect in self.tile_list:
            display.blit(img, rect)


froggy = Player()
world = World(world_data)
restart = Button(randomx, randomy, "images/restart_btn.png")
start = Button(randomx, randomy, "images/start_btn.png")
exit = Button(width // 2, height // 2, "images/exit_btn.png")

display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Platformer")

bg_image = pygame.image.load("images/bg7.png")
bg_rect = bg_image.get_rect()

run = True
main_menu = True
while run:
    clock.tick(fps)
    display.blit(bg_image, bg_rect)
    if main_menu:
        if start.draw():
            main_menu = False
            level = 1
            score = 0
            lives = 3
            world = reset_level()
        if exit.draw():
            run = False
    else:
        world.draw()
        lava_group.draw(display)
        lava_group.update()
        door_group.draw(display)
        coin_group.draw(display)
        draw_text(str(score), (255, 255, 255), 30, 10, 10)
        froggy.update()
        if pygame.sprite.spritecollide(froggy, coin_group, True):
            score += 1
            print(score)
        if game_over == -1:
            if restart.draw():
                lives -= 1
                print(lives)
                if lives == 0:
                    main_menu = True
                froggy = Player()
                world = reset_level()
                game_over = 0
        if game_over == 1:
            game_over = 0
            if level < max_level:
                level += 1
                world = reset_level()
            else:
                main_menu = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

pygame.quit()
