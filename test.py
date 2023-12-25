# for generating random height of pipes
import random
import sys
import pygame
from pygame.locals import *

# Global variables for the game
window_width = 600
window_height = 499

# set height and width of window
window = pygame.display.set_mode((window_width, window_height))
elevation = window_height * 0.8
game_images = {}
framepersecond = 32
pipeimage = 'pipe.png'
background_image = 'background.jpg'
birdplayer_image = 'bird.png'
sealevel_image = 'base.jfif'


def flappygame():
    your_score = 0
    horizontal = int(window_width / 5)
    vertical = int(window_height / 2)
    ground = 0
    bird_flapped = False

    # Generating two pipes for blitting on the window
    first_pipe = createPipe()
    second_pipe = createPipe()

    # List containing lower pipes
    down_pipes = [
        {
            'x': window_width + 300,
            'y': first_pipe[1]['y']
        },
        {
            'x': window_width + 300 + (window_width / 2),
            'y': second_pipe[1]['y']
        },
    ]

    # List containing upper pipes
    up_pipes = [
        {
            'x': window_width + 300,
            'y': first_pipe[0]['y']
        },
        {
            'x': window_width + 300 + (window_width / 2),
            'y': second_pipe[0]['y']
        }
    ]

    # pipe velocity along x
    pipeVelX = -4

    bird_velocity_y = -9
    bird_Max_Vel_Y = 10
    bird_Min_Vel_Y = -8
    birdAccY = 1

    # velocity while flapping
    bird_flap_velocity = -8

    while True:
        # Handling the key pressing events
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if vertical > 0:
                    bird_velocity_y = bird_flap_velocity
                    bird_flapped = True

        # This function will return true if the flappy bird is crashed
        game_over = isGameOver(horizontal, vertical, up_pipes, down_pipes)
        if game_over:
            return your_score

        # check for your score
        playerMidPos = horizontal + game_images['flappybird'].get_width() / 2
        for pipe in up_pipes:
            pipeMidPos = pipe['x'] + game_images['pipeimage'][0].get_width() / 2
            if pipeMidPos - 10 <= playerMidPos < pipeMidPos + 10:
                # printing the score
                your_score += 1
            
           

        if bird_velocity_y < bird_Max_Vel_Y and not bird_flapped:
            bird_velocity_y += birdAccY
        if bird_flapped:
            bird_flapped = False
        playerHeight = game_images['flappybird'].get_height()
        vertical = vertical + min(bird_velocity_y, elevation - vertical - playerHeight)

        # moves pipes to the left
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Add a new pipe when the first pipe is about to cross the leftmost part of the screen
        if 0 < up_pipes[0]['x'] < 5:
            newpipe = createPipe()
            up_pipes.append(newpipe[0])
            down_pipes.append(newpipe[1])

        # if the pipe is out of the screen, remove it
        if up_pipes[0]['x'] < -game_images['pipeimage'][0].get_width():
            up_pipes.pop(0)
            down_pipes.pop(0)
        window.blit(game_images['background'], (0, 0))

        # let's blit our game images now
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
            window.blit(game_images['pipeimage'][0], (upperPipe['x'], upperPipe['y']))
            window.blit(game_images['pipeimage'][1], (lowerPipe['x'], lowerPipe['y']))
        window.blit(game_images['sea_level'], (ground, elevation))
        window.blit(game_images['flappybird'], (horizontal, vertical))

        # fetching the digits of score
        numbers = [int(x) for x in list(str(your_score))]
        width = 0

        # fetching the width of score images from numbers
        for num in numbers:
            width += game_images['scoreimages'][str(num)].get_width()
        Xoffset = (window_width - width) / 2

        # Blitting the images on the window
        for num in numbers:
            window.blit(game_images['scoreimages'][str(num)], (Xoffset, window_width * 0.02))
            Xoffset += game_images['scoreimages'][str(num)].get_width()

        # Refreshing the game window and displaying the score
        pygame.display.update()

        # Set the refreshment
        framepersecond_clock.tick(framepersecond)

def isGameOver(horizontal, vertical, up_pipes, down_pipes):
    # Checking if the bird is above the sea level
    if vertical > elevation - 25 or vertical < 0:
        return True

    # Checking if bird hits the upper pipe or not
    for pipe in up_pipes:
        pipeHeight = game_images['pipeimage'][0].get_height()
        if (vertical < pipeHeight + pipe['y'] and
                abs(horizontal - pipe['x']) < game_images['pipeimage'][0].get_width()):
            return True

    # Checking if bird hits the lower pipe or not
    for pipe in down_pipes:
        if (vertical + game_images['flappybird'].get_height() > pipe['y'] and
                abs(horizontal - pipe['x']) < game_images['pipeimage'][0].get_width()):
            return True

    return False


def createPipe():
    offset = window_height / 3
    pipeHeight = game_images['pipeimage'][0].get_height()

    # generating random height of pipes
    y2 = offset + random.randrange(0, int(window_height - game_images['sea_level'].get_height() - 1.2 * offset))
    pipeX = window_width + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        # upper pipe
        {'x': pipeX, 'y': -y1},

        # lower pipe
        {'x': pipeX, 'y': y2}
    ]

    return pipe
def load_images():
    try:
        game_images['scoreimages'] = {
            '0': pygame.image.load('0.png').convert_alpha(),
            '1': pygame.image.load('1.png').convert_alpha(),
            '2': pygame.image.load('2.png').convert_alpha(),
            '3': pygame.image.load('3.png').convert_alpha(),
            '4': pygame.image.load('4.png').convert_alpha(),
            '5': pygame.image.load('5.png').convert_alpha(),
            '6': pygame.image.load('6.png').convert_alpha(),
            '7': pygame.image.load('7.png').convert_alpha(),
            '8': pygame.image.load('8.png').convert_alpha(),
            '9': pygame.image.load('9.png').convert_alpha()
        }
        game_images['flappybird'] = pygame.image.load(birdplayer_image).convert_alpha()
        game_images['sea_level'] = pygame.image.load(sealevel_image).convert_alpha()
        game_images['background'] = pygame.image.load(background_image).convert_alpha()
        game_images['pipeimage'] = (
            pygame.image.load(pipeimage).convert_alpha(),
            pygame.transform.rotate(pygame.image.load(pipeimage).convert_alpha(), 180)
        )
        return True
    except pygame.error as e:
        print("Error loading images:", e)
        return False

if __name__ == "__main__":
    # For initializing modules of pygame library
    pygame.init()
    framepersecond_clock = pygame.time.Clock()

    # Sets the title on top of the game window
    pygame.display.set_caption('Flappy Bird Game')

    
    if not load_images():
        sys.exit()

    print("WELCOME TO THE FLAPPY BIRD GAME")
    print("Press space or enter to start the game")

    while True:
        # Set the coordinates of flappy bird
        horizontal = int(window_width / 5)
        vertical = int((window_height - game_images['flappybird'].get_height()) / 2)

        # For sealevel
        ground = 0
        bird_flapped = False

        for event in pygame.event.get():
            # If user clicks on the cross button, close the game:
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                # Exit the program
                sys.exit()

            # If the user presses space or up key, start the game
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                score = flappygame()
                print(f'Your score is {score}')

                break  # exit the loop when the game is finished

        window.blit(game_images['background'], (0, 0))
        window.blit(game_images['flappybird'], (horizontal, vertical))
        window.blit(game_images['sea_level'], (ground, elevation))

        # Refresh the screen
        pygame.display.update()

        # Set the rate of frame per second
        framepersecond_clock.tick(framepersecond)



