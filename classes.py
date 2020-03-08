import pygame
import settings
vec = pygame.math.Vector2



class Kebab:
    def __init__(self, x, y, x_change, y_change, img):
        self.x = x
        self.y = y
        self.x_change = x_change
        self.y_change = y_change
        self.img = img


class Game_Functions():
    def __init__(self, game):
        self.game = game



    def object_collision(self, object, subject, object_dimensions, subject_dimensions):
        self.game.collided = False

        self.direction = self.game.direction
        self.object_x, self.object_y = int(object.pos.x), int(object.pos.y)
        self.subject_x, self.subject_y = int(subject.pos.x), int(subject.pos.y)

        # the hitbox of the goal:

        self.object_min_x, self.object_max_x = (self.object_x - subject_dimensions[0]), (self.object_x + (object_dimensions[0]))
        self.object_min_y, self.object_max_y = (self.object_y - subject_dimensions[1]), (self.object_y + (object_dimensions[1]))


        if (self.subject_x < self.object_max_x) and (self.subject_x > self.object_min_x):
            if (self.subject_y < self.object_max_y) and (self.subject_y > self.object_min_y):

                #print("\nObject = goal, subject = player")
                #print("object_x = {}, object_y = {}".format(self.object_x, self.object_y))
                #print("subject_x = {}, subject_y = {}".format(self.subject_x, self.subject_y))
                #print("object_min_x = {}, \n"
                #      "object_max_x = {}, difference = {}\n"
                #      "object_min_y = {}, \n"
                #      "object_max_y = {}, difference = {}\n \n".format(self.object_min_x, self.object_max_x, (self.object_max_x-self.object_min_x),
                #                                                  self.object_min_y, self.object_max_y, (self.object_max_y-self.object_min_y)))


                self.game.collided = True

class Dog_bullet(pygame.sprite.Sprite):
    def __init__(self, game, x, y, direction):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.shiba_img
        self.rect = self.image.get_rect()
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.pos = vec(x, y) * settings.tilesize
        self.friction = settings.dog_friction
        self.direction = direction
        self.time_existed = 0

        # dog hop!
        self.vel.y = -settings.dog_hop
        self.bounce_number = 0
        self.bounce_vel = 0
        self.height = 0
        self.highest_point = 0
        self.lowest_point = 0
        self.difference = 0


    # COLLISION
    def collision(self, dir):
        if dir == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y
        if dir == 's':
            print("success")

    def track_hop(self):
        if self.time_existed < 32:
            if self.vel.y > 0:
                self.highest_point = self.pos.y
        if self.time_existed > 32:
            if self.vel.y == 0:
                self.lowest_point = self.pos.y
        else:
            pass

        if self.lowest_point > 0:
            self.difference = self.lowest_point - self.highest_point
            self.bounce()
            self.lowest_point = 0

        else:
            self.bounce_vel = self.bounce_vel * 0.8

        '''print("dog y pos: {}, high: {}, low: {}, difference: {}, bounce_vel: {}".format(self.pos.y, self.highest_point,
                                                                                    self.lowest_point, self.difference,
                                                                                    self.bounce_vel))
'''
    def bounce(self):
        '''

        A ball is dropped from rest at a height ℎ𝟢 and bounces from a surface
        such that the height of the 𝑛th bounce,
        ℎ𝑛, is given by ℎ𝑛=𝛼ℎ𝑛−1, where ℎ𝑛−1 is the height of the previous, (𝑛−1)th bounce.
        The factor 𝛼 has value 0≤𝛼≤1.

        '''


        ''' The following code works, but it is not realistic. That would require measuring the height (dist between ball and floor) '''



        self.bounce_number += 1
        if self.bounce_number == 1:
            self.bounce_vel = self.difference / 32
            self.vel.y = -self.bounce_vel
        if self.bounce_number == 2:
            self.bounce_vel = self.difference / 64
            self.vel.y = -self.bounce_vel
        if self.bounce_number == 3:
            self.bounce_vel = self.difference / 98
            self.vel.y = -self.bounce_vel
        if self.bounce_number == 4:
            self.bounce_vel = self.difference / 124
            self.vel.y = -self.bounce_vel
        if self.bounce_number == 5:
            self.bounce_vel = self.difference / 160
            self.vel.y = -self.bounce_vel



    def movement(self, direction):
        self.acc = vec(0, settings.dog_gravity)
        #print(self.vel.y)
        self.acc.x = settings.dog_acc
        self.player_x_dir = self.game.player.vel.x
        if direction == "right":
            self.acc.x = self.acc.x
        if direction == "left":
            self.acc.x = -self.acc.x
        if direction == "up":
            self.acc.x = 0



    def update(self):
        self.movement(self.direction)
        self.time_existed += 1
        self.track_hop()


        # kill sprite after some time. 1 sec = 120
        if self.time_existed == 600:
            self.time_existed = 0
            self.game.bullets_in_play -= 1
            self.kill()


        # friction
        self.acc.x += self.vel.x * self.friction
        #movement
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # COLLISION
        self.rect.x = self.pos.x
        self.collision("x")
        self.rect.y = self.pos.y
        self.collision("y")

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.pos = vec(x, y) * settings.tilesize
        self.pos_tiles = vec(x, y)
        self.friction = settings.player_friction




    def jump(self):
        if self.vel.y == 0:
            self.vel.y = -16
        # if you hit the ceiling, you can actually stay there by holding down the jump key.
        # use it as a feature or debug it



    # MOVEMENT
    def get_keys(self):
        self.acc = vec(0, settings.player_gravity)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.acc.x = -settings.player_acc
            self.game.direction = "left"
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.acc.x = settings.player_acc
            self.game.direction = "right"
        if keys[pygame.K_UP] or keys[pygame.K_SPACE]:
            self.jump()




        if keys[pygame.K_r]:
            self.game.restart(self.game.level)










    # COLLISION
    def collision(self, dir):
        if dir == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y
        if dir == 's':
            print("success")



    def update(self):
        self.get_keys()

        # friction
        self.acc.x += self.vel.x * self.friction
        #movement
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.pos_tiles += (self.vel + 0.5 * self.acc) / 2
        # COLLISION
        self.rect.x = self.pos.x
        self.collision("x")
        self.rect.y = self.pos.y
        self.collision("y")

class Sun_Shiba (pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x
        self.y = y
        self.image = game.shiba_img
        self.rect = self.image.get_rect()
        self.rect.x = x*settings.tilesize
        self.rect.y = y*settings.tilesize
        self.pos = vec(x, y) * settings.tilesize
        self.game_functions = Game_Functions(game)


    def update(self):
        self.game_functions.object_collision(self, self.game.player, (64, 64), (64, 64))
        if self.game.collided == True:
            self.game.ammo += 1
            self.kill()


class Goal_flat(pygame.sprite.Sprite):
    def __init__(self, game, x, y, direction):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x
        self.y = y
        self.direction = direction
        self.pos = vec(x, y) * settings.tilesize
        self.game_functions = Game_Functions(game)
        if self.direction == "right":
            self.image = game.goal_flat_img_right #width, height
            self.dimensions = (64, 192)
        if self.direction == "down":
            self.image = game.goal_flat_img_down
            self.dimensions = (192, 64)
        if self.direction == "left":
            self.image = game.goal_flat_img_left
            self.dimensions = (64, 192)
        if direction == "up":
            self.image = game.goal_flat_img_up
            self.dimensions = (192, 64)
        self.rect = self.image.get_rect()
        self.rect.x = x * settings.tilesize
        self.rect.y = y * settings.tilesize



    def update(self):
        self.game_functions.object_collision(self, self.game.player, self.dimensions, (64, 64))
        #                                   object, subject, object_dimensions, subj_dimensions, direction
        if self.game.collided == True:
            self.game.level += 1
            self.game.restart(self.game.level)





class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename, "rt") as f:
            for line in f:
                self.data.append(line.strip()) # .strip() fjerner "new line" karakterer

        self.tilewidth = len(self.data[0])  # Så mange tiles bred er mappen
        self.tileheight = len(self.data)
        self.width = self.tilewidth * settings.tilesize
        self.height = self.tileheight * settings.tilesize

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height) # 0, 0 = offset, offset
        self.width = width
        self.height = height


    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)


    def update(self, target):
        x = -target.rect.x + int(settings.display_width / 2)
        y = -target.rect.y + int(settings.display_height / 2)

        # Limit scrolling to map size
        x = min(0, x) # Left
        y = min(0, y) # Top
        x = max(-(self.width - settings.display_width), x) # Right
        y = max(-(self.height - settings.display_height), y) # Bottom
        self.camera = pygame.Rect(x, y, self.width, self.height)

class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y, type):
        self.groups = game.all_sprites, game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x
        self.y = y
        self.pos_pixels = vec(self.x * settings.tilesize, self.y * settings.tilesize)

        # type
        if type == "grass":
            self.image = game.grass_tile_img
        if type == "dirt":
            self.image = game.dirt_tile_img
        self.rect = self.image.get_rect()

        self.rect.x = x * settings.tilesize
        self.rect.y = y * settings.tilesize





class Enemy (pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x
        self.y = y
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.rect.x = x*settings.tilesize
        self.rect.y = y*settings.tilesize
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.pos = vec(x, y) * settings.tilesize
        self.friction = settings.dog_friction

        # animation
        self.turning = False
        self.turning_frames = []
        self.current_frame = 0
        self.frames_passed = 0
        self.load_images()



    def load_images(self):

        self.turning_frames = [pygame.image.load('img/swordsman_1.png'),
                               pygame.image.load('img/swordsman_2.png'),
                               pygame.image.load('img/swordsman_3.png'),
                               pygame.image.load('img/swordsman_4.png'),
                               pygame.image.load('img/swordsman_5.png'),
                               pygame.image.load('img/swordsman_6.png'),
                               pygame.image.load('img/swordsman_7.png'),
                               ]
        for frame in self.turning_frames:
            frame.set_colorkey(settings.white)

    # COLLISION
    def collision(self, dir):
        if dir == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y
        if dir == 's':
            print("success")



    def animate(self):
        print(self.frames_passed, self.current_frame)


        if self.frames_passed % 70 == 0:
            self.frames_passed = 0
            self.current_frame = 0
            self.frames_passed += 1
        if self.frames_passed % 10 == 0:
            self.current_frame += 1
            self.frames_passed += 1
        else:
            self.frames_passed += 1
        self.image = self.turning_frames[self.current_frame]



    def movement(self):
        self.acc.x += self.vel.x * self.friction
        self.acc = vec(0, settings.dog_gravity)
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

    def make_path(self):
        #if self.frames_passed < 70:
            #print(self.frames_passed, self.current_frame)
        pass

    def update(self):
        # animation
        self.animate()
        self.movement()
        self.make_path()



        # COLLISION
        self.rect.x = self.pos.x
        self.collision("x")
        self.rect.y = self.pos.y
        self.collision("y")









