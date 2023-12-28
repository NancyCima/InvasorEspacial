import pygame
import math
import random
from pygame import mixer

# Initialize pygame
pygame.init()

# Create the screen
width = 800
height = 600
screen = pygame.display.set_mode((width, height))

# Background
background = pygame.image.load('Assets/background.png')

# Background music
mixer.music.load('Assets/background.wav')
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption('Invasion Espacial')
icon = pygame.image.load('Assets/ufo.png')
pygame.display.set_icon(icon)

# Score
score_value = 0


# Function to show text
def draw_text(surface, text, size, x, y):
    font = pygame.font.SysFont("serif", size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


# Menu
def show_menu():
    screen.blit(background, [0, 0])
    draw_text(screen, 'INVASION ESPACIAL', 65, width // 2, height / 4)
    draw_text(screen, '¡Protege a la Tierra de los invasores alienígenas!', 27, width // 2, height // 2)
    draw_text(screen, 'Presione una tecla para comenzar', 17, width // 2, height * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False


# Player
class Player:
    def __init__(self):
        self.image = pygame.image.load('Assets/player.png')
        self.x = 370
        self.y = 480
        self.X_change = 0

    def show(self):
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.x += self.X_change
        if self.x <= 0:
            self.x = 0
        elif self.x >= 736:
            self.x = 736


# Enemy
class Enemy:
    def __init__(self):
        self.image = pygame.image.load('Assets/enemy.png')
        self.x = random.randint(0, 736)
        self.y = random.randint(50, 150)
        self.x_change = 4
        self.y_change = 40

    def show(self):
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.x += self.x_change
        if self.x <= 0:
            self.x_change = 4
            self.y += self.y_change
        elif self.x >= 736:
            self.x_change = -4
            self.y += self.y_change


# Laser

class Laser:
    # Ready - The laser is ready to be shot, but you can't see the laser on the screen
    # Fire - The laser was shot and is currently moving
    def __init__(self):
        self.image = pygame.image.load('Assets/laser.png')
        self.x = 0
        self.y = 480
        self.x_change = 0
        self.y_change = 10
        self.state = "ready"

    def fire(self):
        self.state = "fire"
        screen.blit(self.image, (self.x + 35, self.y + 15))

    def move(self):
        if self.y <= 0:
            self.y = 480
            self.state = "ready"

        if self.state is "fire":
            self.fire()
            self.y -= self.y_change


def isCollision(enemy_x, enemy_y, laser_x, laser_y):
    distance = math.sqrt(math.pow(enemy_x - laser_x, 2) + (math.pow(enemy_y - laser_y, 2)))
    if distance < 27:
        return True
    else:
        return False


player = Player()
laser = Laser()

num_of_enemies = 4
enemies = []
for i in range(num_of_enemies):
    enemies.append(Enemy())

# Game Loop
game_over = True
running = True
while running:
    screen.blit(background, (0, 0))
    if game_over:
        show_menu()
        game_over = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.X_change = -10
            if event.key == pygame.K_RIGHT:
                player.X_change = 10
            if event.key == pygame.K_SPACE:
                if laser.state is "ready":
                    laserSound = mixer.Sound("Assets/laser.wav")
                    laserSound.play()
                    # Get the current x coordinate of the spaceship
                    laser.x = player.x
                    laser.fire()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.X_change = 0

        player.move()

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemies[i].y > 420:
            for j in range(num_of_enemies):
                enemies[j].y = 2000
            draw_text(screen, 'GAME OVER', 64, 400, 200)
            break

        enemies[i].move()

        # Collision
        collision = isCollision(enemies[i].x, enemies[i].y, laser.x, laser.y)
        if collision:
            explosionSound = mixer.Sound("Assets/explosion.wav")
            explosionSound.play()
            laser.y = 480
            laser.laser_state = "ready"
            score_value += 1
            enemies[i].x = random.randint(0, 736)
            enemies[i].y = random.randint(50, 150)

        enemies[i].show()

    laser.move()
    player.show()
    draw_text(screen, 'Score : ' + str(score_value), 32, 65, 10)
    pygame.display.update()
