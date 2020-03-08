import pygame
from os import path
import random
import time
import classes
import settings
import sys
vec = pygame.math.Vector2


'''

    TO-DO LIST:
        1) Make ammo counter GUI thing
        2) Make a path for the enemy
        3) Learn how to make cool paths?    

'''







gameDisplay = pygame.display.set_mode((settings.display_width, settings.display_height))
pygame.display.set_caption('The baobei game')
clock = pygame.time.Clock()

class Game:
    def __init__(self):
        pygame.init()
        self.gameDisplay = pygame.display.set_mode((settings.display_width, settings.display_height))
        pygame.display.set_caption(settings.title)
        self.game_folder = path.dirname(__file__)  # Denne mappe
        self.img_folder = path.join(self.game_folder, "img")
        self.clock = pygame.time.Clock()
        self.font_name = pygame.font.match_font(settings.font_name)
        self.load_data()
        self.level = 0

        self.direction = "right"
        self.collided = False

        self.ammo = 0
        self.bullets_in_play = 0





    def load_data(self):
        # splash screens
        self.start_screen_img = pygame.image.load(path.join(self.img_folder, settings.start_screen_img)).convert()


        # BG. Perhaps this should have its own class
        self.bg_img = pygame.image.load('img/bg_1.jpg').convert()
        self.bg_img_pos = (0, 0)

        self.start_screen_bg = pygame.image.load(path.join(self.img_folder, settings.start_screen_bg))


        # img
        self.player_img = pygame.image.load(path.join(self.img_folder, settings.player_img)).convert()
        self.grass_tile_img = pygame.image.load(path.join(self.img_folder, settings.grass_tile)).convert()
        self.dirt_tile_img = pygame.image.load(path.join(self.img_folder, settings.dirt_tile)).convert()

        self.shiba_img = pygame.image.load(path.join(self.img_folder, settings.shiba_img)).convert()
        self.shiba_img.set_colorkey(settings.black)

        self.goal_flat_img_right = pygame.image.load(path.join(self.img_folder, settings.goal_flat_img_right)).convert()
        self.goal_flat_img_down = pygame.image.load(path.join(self.img_folder, settings.goal_flat_img_down)).convert()
        self.goal_flat_img_left = pygame.image.load(path.join(self.img_folder, settings.goal_flat_img_left)).convert()
        self.goal_flat_img_up = pygame.image.load(path.join(self.img_folder, settings.goal_flat_img_up)).convert()






    def events(self):
        # if quit
        self.player_pos = vec(self.player.pos.x / settings.tilesize, self.player.pos.y / settings.tilesize)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            # shoot
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.show_pause_screen()
                if event.key == pygame.K_s:
                    if self.ammo > 0:
                        self.bullet = classes.Dog_bullet(self, self.player_pos.x, self.player_pos.y, self.direction)
                        self.bullets_in_play += 1
                        self.ammo -= 1







    def draw(self):
        self.gameDisplay.blit(self.bg_img, self.bg_img_pos)
        for sprite in self.all_sprites:
            self.gameDisplay.blit(sprite.image, self.camera.apply(sprite))
        pygame.display.flip()


    def show_start_screen(self):
        # game splash/start screen
        #self.gameDisplay.fill(settings.bg_color)
        self.gameDisplay.blit(self.start_screen_bg, (0, 0))
        self.gameDisplay.blit(self.start_screen_img, (192, 104))
        '''
        self.draw_text(settings.title, 48, settings.white, settings.display_width / 2, settings.display_height / 4)
        self.draw_text("Arrow keys to move, space to jump", 22, settings.white, settings.display_width / 2, settings.display_height / 2)
        self.draw_text("Press any key to play", 22, settings.white, settings.display_width / 2, settings.display_height * 3 / 4)
        '''
        pygame.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        # press any key to start playing
        self.waiting = True
        while self.waiting:
            self.clock.tick(settings.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.waiting = False
                    self.playing = False
                if event.type == pygame.KEYUP:
                    self.waiting = False

    def restart(self, level):
        self.new(level)



    def draw_text(self, text, size, color, x, y):
        self.font = pygame.font.Font(self.font_name, size)
        self.text_surface = self.font.render(text, True, color)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.midtop = (x, y)
        self.gameDisplay.blit(self.text_surface, self.text_rect)

    def show_go_screen(self):
        # game over/continue
        pass

    def new(self, level):
        # start a new game
        self.map_name = "map%d.txt" % level
        self.map = classes.Map(path.join(self.game_folder, "maps/{}".format(self.map_name)))


        self.parse_map_grid(self.map)






    def parse_map_grid(self, map):
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        for row, tiles in enumerate(map.data):  # Enumerate giver både index og value. Index her er altså min tiles y-værdi
            for col, tile in enumerate(tiles):  # Enumerate for hver linje, således at index her er x-værdien af mit tile

                # platforms
                if tile == "1":
                    self.wall = classes.Wall(self, col, row, "grass")
                if tile == "2":
                    classes.Wall(self, col, row, "dirt")

                # persons
                if tile == "P":
                    self.player = classes.Player(self, col, row)  # Spawn player udfra tekstfilen
                if tile == "E":
                    self.enemy = classes.Enemy(self, col, row)

                # goals
                if tile == "S":
                    self.dog = classes.Sun_Shiba(self, col, row)
                if tile == "r":
                    self.goal_right = classes.Goal_flat(self, col, row, "right")
                if tile == "d":
                    self.goal_down = classes.Goal_flat(self, col, row, "down")
                if tile == "l":
                    self.goal_left = classes.Goal_flat(self, col, row, "left")
                if tile == "u":
                    self.goal_down = classes.Goal_flat(self, col, row, "up")

        self.camera = classes.Camera(map.width, map.height)



    def quit(self):
        pygame.quit()
        sys.exit()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(settings.fps) / 1000
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        self.camera.update(self.player)






level = 0
g = Game()

g.show_start_screen()
while True:
    # test a level:
    #g.new(4)

    # run normally:
    g.new(level)

    g.run()
    g.show_go_screen()


pygame.quit()
quit()