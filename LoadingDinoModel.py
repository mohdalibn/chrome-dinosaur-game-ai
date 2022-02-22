import pygame
import os 
import random
import sys
import neat
import math
import numpy as np
import pickle # use this module to save the best bird into a file and then you can load in the file and use the neural network associated with it


pygame.init()

# Global Constanst
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

FONT = pygame.font.Font('freesansbold.ttf', 20)

RUNNING = [pygame.image.load(os.path.join("ChromeDinoGame/Assets/Dino", "DinoRun1.png")),
pygame.image.load(os.path.join("ChromeDinoGame/Assets/Dino", "DinoRun2.png"))]

JUMPING = pygame.image.load(os.path.join("ChromeDinoGame/Assets/Dino", "DinoJump.png"))

DUCKING = [pygame.image.load(os.path.join("ChromeDinoGame/Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("ChromeDinoGame/Assets/Dino", "DinoDuck2.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("ChromeDinoGame/Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("ChromeDinoGame/Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("ChromeDinoGame/Assets/Cactus", "SmallCactus3.png"))]

LARGE_CACTUS = [pygame.image.load(os.path.join("ChromeDinoGame/Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("ChromeDinoGame/Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("ChromeDinoGame/Assets/Cactus", "LargeCactus3.png"))]

BIRD = [pygame.image.load(os.path.join("ChromeDinoGame/Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("ChromeDinoGame/Assets/Bird", "Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("ChromeDinoGame/Assets/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("ChromeDinoGame/Assets/Other", "Track.png"))


class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self, img=RUNNING[0]):
        self.image = img
        self.dino_run = True
        self.dino_jump = False
        self.dino_duck = False
        self.jump_vel = self.JUMP_VEL
        self.rect = pygame.Rect(self.X_POS, self.Y_POS, img.get_width(), img.get_height())
        self.step_index = 0
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


        # self.duck_img = DUCKING
        # self.run_img = RUNNING
        # self.jump_img = JUMPING
        # self.dino_duck = False
        # self.image = self.run_img[0]
        # self.dino_rect = self.image.get_rect()
        # self.dino_rect.x = self.X_POS
        # self.dino_rect.y = self.Y_POS

    def update(self):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        # if userInput[pygame.K_UP] and not self.dino_jump:
        #     self.dino_duck = False
        #     self.dino_run = False
        #     self.dino_jump = True
        # elif userInput[pygame.K_DOWN] and not self.dino_jump:
        #     self.dino_duck = True
        #     self.dino_run = False
        #     self.dino_jump = False
        # elif not (self.dino_jump or userInput[pygame.K_DOWN]):
        #     self.dino_duck = False
        #     self.dino_run = True
        #     self.dino_jump = False

    def duck(self):
        self.image = DUCKING[self.step_index // 5]
        #self.rect = self.image.get_rect()
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = RUNNING[self.step_index // 5]
        # self.dino_rect = self.image.get_rect()
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = JUMPING
        if self.dino_jump:
            self.rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.dino_jump = False
            self.dino_run = True
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))
        # draws the hitbox around the dinosaurs
        pygame.draw.rect(SCREEN, self.color, (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 2)

        # loops over the obstacles list and draws a line of sight from the dinosaur
        # 54 and 12 are offsets that puts the line at the center of the dinosaur's eye
        for obstacle in obstacles:
            pygame.draw.line(SCREEN, self.color, (self.rect.x + 54, self.rect.y + 12), obstacle.rect.center, 2)


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(000, 1000)
        self. y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        # resets the coords when the cloud moves off the screen
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, number_of_cacti):
        self.image = image
        self.type = number_of_cacti
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

class SmallCactus(Obstacle):
    def __init__(self, image, number_of_cacti):
        #self.number_of_cacti = random.randint(0, 2)
        super().__init__(image, number_of_cacti)
        self.rect.y = 325

class LargeCactus(Obstacle):
    def __init__(self, image, number_of_cacti):
        #self.number_of_cacti = random.randint(0, 2)
        super().__init__(image, number_of_cacti)
        self.rect.y = 300

class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1



def remove(index): # removes the dinosaurs that run into an obstacle
    dinosaurs.pop(index)
    ge.pop(index)
    nets.pop(index)


def distance(pos_a, pos_b):
    dx = pos_a[0] - pos_b[0]
    dy = pos_a[1] - pos_b[1]
    
    return math.sqrt(dx**2 + dy**2)


# renamed this function from main to eval_genomes
def eval_genomes(genomes, config):
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, dinosaurs, ge, nets

    clock = pygame.time.Clock()
    cloud = Cloud()

    obstacles = []
    dinosaur = Dinosaur()

    # ge is short for genomes
    ge = [] # this list is going to store dictionaries. Within these dictionaries, there is going to be information on each individual dinosaur such as its fitness level, its nodes, and its connections

    nets = [] # going to store the neural net object of each individual dinosaur

    # to fill the dinosaurs, ge, and nets lists we use the following for loop
    for genome_id, genome in genomes:
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)

        # initially, we want the genome to start with a fitness level of 0, we use the following line of code
        genome.fitness = 0

    points = 0
    x_pos_bg = 0
    y_pos_bg = 380
    game_speed = 20

    def score():
        global points, game_speed

        points += 1
        if points % 100 == 0:
            game_speed += 1
        text = FONT.render("Score: " + str(points), True, (0, 0, 0))
        SCREEN.blit(text, (950, 50))



    def background():
        global x_pos_bg, y_pos_bg

        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            x_pos_bg = 0
        x_pos_bg -= game_speed



    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

        SCREEN.fill((255, 255, 255))

        
        dinosaur.update()
        dinosaur.draw(SCREEN)

        # if len(dinosaur) ==0:
        #     break

        if len(obstacles) == 0:
            rand_int = random.randint(0, 2)
            if rand_int == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS, random.randint(0, 2)))

            elif rand_int == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS, random.randint(0, 2)))

            elif rand_int == 2:
                obstacles.append(Bird(BIRD))


        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()


            if dinosaur.rect.colliderect(obstacle.rect):
                # decreases the fitness by 1 for the dinosaur that hits an obstacle
                ge[0].fitness -= 1
                remove(i)
                break
            else:
                ge[0].fitness += 1


        # the following line of code was the original method of manual input
        #user_input = pygame.key.get_pressed()

        # we need to pass the inputs of each individual dinosaur which are its y position, and its distance to the next obstacle into its neural net
        output = nets[0].activate((
            dinosaur.rect.y,
            distance((dinosaur.rect.x, dinosaur.rect.y), obstacle.rect.midtop) 
        ))

        # replaced the old manual if statement with the new one
        # if the output is higher is 0.5 and the dinosaur is not currrently jumping, we initial the jump by executing the lines below the if statement
        if output[0] > 0.5 and dinosaur.rect.y == dinosaur.Y_POS :
            dinosaur.dino_jump = True
            dinosaur.dino_duck = False
            dinosaur.dino_run = False
        elif output[1] > 0.5 and not dinosaur.dino_jump:
            dinosaur.dino_duck = True
            dinosaur.dino_jump = False
            dinosaur.dino_run = False


        score()
        background()
        cloud.draw(SCREEN)
        cloud.update()

        clock.tick(30)
        pygame.display.update() # updates the display



#CODE TO USE FOR USING A SAVED GENOME

def replay_genome(config_path, genome_path="DinoWinner"):
    # Load requried NEAT config
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    # Unpickle saved winner
    with open(genome_path, "rb") as f: # the 'b' in rb stands for binary cuz the file is binary
        genome = pickle.load(f)

    # Convert loaded genome into required data structure
    genomes = [(1, genome)]

    # Call game with only the loaded genome
    eval_genomes(genomes, config)




if __name__ == "__main__":
    local_dir = os.path.dirname(__file__) # this gives us the path to our local/working/current directory
  
    config_path = os.path.join(local_dir, 'config.txt')


    #Testing the saved model
    genome_path = os.path.join(local_dir, 'DinoWinner')
    replay_genome(config_path, genome_path="DinoWinner")
