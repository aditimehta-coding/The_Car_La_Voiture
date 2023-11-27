import time
import random
import pygame

pygame.init()
display_width = 800
display_height = 600
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('La Voiture')
icon = pygame.image.load('media/images/mycar.png')
icon = pygame.transform.scale(icon, (32, 32))
booster_image = pygame.image.load('media/images/booster.png')
booster_image = pygame.transform.scale(booster_image, (50, 50))
pygame.display.set_icon(icon)
# initialize colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (200, 0, 0)
green = (0, 200, 0)
dark_red = (150, 0, 0)
dark_green = (0, 150, 0)
blue = (0, 0, 255)
golden = (255, 201, 14)
clock = pygame.time.Clock()
bg = pygame.image.load("media/images/milkyway.jpg")
bg = pygame.transform.scale(bg, (display_width, display_height))
pause = False
game_music_volume = 0.1
obs_width = 40
obs_height = 50


# change_volume(1)for volume increase , change_volume(0) for decrease
def change_volume(increase:bool):
    global game_music_volume
    if increase:
        if game_music_volume <= 0.9:
            game_music_volume += 0.1
        else:
            game_music_volume = 1
    else:
        if game_music_volume >= 0.1:
            game_music_volume -= 0.1
        else:
            game_music_volume = 0


def game_controls():
    global bg
    gameDisplay.blit(bg, (0, 0))
    message_display("Move Car Left:  Left Arrow Key\n Move Car Right:  Right Arrow Key\n Move Car Up:  Up Arrow Key\n Move Car Down:  Down Arrow Key\nPause the Game : Press P\n Increase Music Volume: '=' key\n Decrease Music Volume: '-' key"
                    , white)
    back_button = Button("Back", green, dark_green, (350, 20, 100, 50), lambda:start_menu('Start'))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_warning()
            back_button.HoverEffect()
            back_button.onclick()
            clock.tick(120)

def start_menu(play_button_text):
    intro = True
    global bg
    gameDisplay.blit(bg, (0, 0))
    tile = pygame.image.load('media/images/Title_Font.png')
    tile = pygame.transform.scale(tile, (300, 50))
    gameDisplay.blit(tile, (250, 300))
    logo = pygame.image.load('media/images/mycar.png')
    logo = pygame.transform.scale(logo, (100, 100))
    gameDisplay.blit(logo, (350, 350))
    start_b = Button(play_button_text, green, dark_green, [50, 20, 120, 50], game_loop)
    start_b.Draw()
    quit_b = Button("Quit", red, dark_red, [650, 20, 120, 50], quit_warning)
    quit_b.Draw()
    controls_b = Button("Controls",green, dark_green, [340, 100, 120, 50], game_controls)
    pygame.display.update()
    while intro:
        if play_button_text == 'Resume':
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_warning()
        start_b.HoverEffect()
        quit_b.HoverEffect()
        start_b.onclick()
        quit_b.onclick()
        controls_b.HoverEffect()
        controls_b.onclick()
        clock.tick(120)


def unpause():
    global pause
    pause = False
    pygame.mixer.music.set_volume(game_music_volume)
    pygame.mixer.music.play()

def pixel_overlap(obj1, obj2, obj1_pos, obj2_pos):
    mask1 = pygame.mask.from_surface(obj1)
    mask2 = pygame.mask.from_surface(obj2)
    overlap_area = mask1.overlap_area(mask2, (obj2_pos[0] - obj1_pos[0], obj2_pos[1] - obj1_pos[1]))
    if overlap_area > 0:
        return True
    else:
        return False

# Button Class
class Button:
    def __init__(self, text, color, hover_color, rect, clickhandler):
        self.text = text
        self.color = color
        self.rect = rect
        self.hover_color = hover_color
        self.activeColor = self.color
        self.clickhandler = clickhandler

    def Draw(self):
        pygame.draw.rect(gameDisplay, self.activeColor, self.rect)
        self.Text_Display()

    def HoverEffect(self):
        mouse = pygame.mouse.get_pos()
        if self.rect[0] < mouse[0] < self.rect[0] + self.rect[2] and self.rect[1] < mouse[1] < self.rect[1] + self.rect[
            3]:
            self.activeColor = self.hover_color
            self.Draw()
            pygame.display.update()
        else:
            self.activeColor = self.color
            self.Draw()
            pygame.display.update()

    def onclick(self):
        mouse = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if self.rect[0] < mouse[0] < self.rect[0] + self.rect[2] and self.rect[1] < mouse[1] < self.rect[1] + \
                    self.rect[3]:
                self.clickhandler()

    def Text_Display(self):
        large_text = pygame.font.Font('freesansbold.ttf', 20)
        text_surf, text_rect = text_objects(self.text, large_text, black)
        text_rect.center = (self.rect[0] + self.rect[2] / 2, self.rect[1] + self.rect[3] / 2)
        gameDisplay.blit(text_surf, text_rect)
        pygame.display.update()


def quit_warning():
    global bg
    gameDisplay.blit(bg, (0, 0))
    message_display("Are you sure you want to quit", white)
    ok_button = Button("Yes", red, dark_red, [290, 350, 100, 50], quit_game)
    ok_button.Draw()
    cancel_button = Button("Cancel", green, dark_green, [410, 350, 100, 50], lambda: start_menu('Start'))
    cancel_button.Draw()
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                print('quiting from warning screen')
                quit()
        ok_button.HoverEffect()
        cancel_button.HoverEffect()
        ok_button.onclick()
        cancel_button.onclick()
        clock.tick(120)


def quit_game():
    pygame.quit()
    quit()

def pause_game():
    global pause
    global game_music_volume
    pause = True
    message_display("Game Paused", white)
    resume_b = Button("Resume", green, dark_green, [50, 20, 120, 50], unpause)
    resume_b.Draw()
    quit_b = Button("Quit", red, dark_red, [650, 20, 120, 50], quit_game)
    quit_b.Draw()
    pygame.display.update()
    if game_music_volume:
        pygame.mixer.music.set_volume(0.03)
        pygame.mixer.music.play()
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
        resume_b.HoverEffect()
        quit_b.HoverEffect()
        resume_b.onclick()
        quit_b.onclick()
        clock.tick(120)



def text_objects(text, font, color):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def message_display(text, color):
    lines = text.split("\n")
    y_offset = 0
    for line in lines:
        large_text = pygame.font.Font('freesansbold.ttf', 20)
        text_surf, text_rect = text_objects(line, large_text, color)
        text_rect.center = (display_width / 2, display_height / 2 + y_offset)
        gameDisplay.blit(text_surf, text_rect)
        y_offset += 30
    pygame.display.update()
import random

def generate_random_x(start, stop, min_gap, num_numbers):
    numbers = []
    current_number = start

    while len(numbers) < num_numbers:
        # Generate a random number
        random_number = random.uniform(start, stop)

        # Check if the random number is at least min_gap away from the current number
        if abs(random_number - current_number) >= min_gap:
            numbers.append(random_number)
            current_number = random_number

    return numbers

class Obstacle:
    def __init__(self, obstacle_id, image):
        self.image = image
        self.obstacle_id = obstacle_id

    def Display_obstacle(self, mysurface, obstaclex, obstacley):
        mysurface.blit(self.image, (obstaclex, obstacley))
    def obstacle_initial_position_generator(self):
        # init_obs_x = random.randrange(0, display_width - obs_width)
        init_obs_y = -random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 20, 25]) * obs_height
        return init_obs_y

def game_loop():
    global game_music_volume
    global pause
    global bg
    crash_sound = pygame.mixer.Sound('media/music/carcrash.wav')
    pygame.mixer.music.load('media/music/MainMusic.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(game_music_volume)
    no_of_obstacles = 8
    obs_speed = 1
    x_change_left = 0
    x_change_right = 0
    y_change_up = 0
    y_change_down = 0
    DEFAULT_IMAGE_WIDTH = 74
    DEFAULT_IMAGE_HEIGHT = 68
    DEFAULT_IMAGE_SIZE = (DEFAULT_IMAGE_WIDTH, DEFAULT_IMAGE_HEIGHT)
    score = 0
    booster_x = 0
    booster_y = 0
    booster_points = random.randrange(7, 12)
    myCar = pygame.image.load('media/images/mycar.png')
    myCar = pygame.transform.scale(myCar, DEFAULT_IMAGE_SIZE)
    obs1 = pygame.image.load('media/images/car1.png')
    obs1 = pygame.transform.scale(obs1, [obs_width, obs_height])
    obs2 = pygame.image.load('media/images/car2.png')
    obs2 = pygame.transform.scale(obs2, [obs_width, obs_height])
    def DisplayScore(score):
        font = pygame.font.SysFont('None', size=25)
        text = font.render(f'Score: {str(score)}', True, white)
        gameDisplay.blit(text, (0, 0))

    def car(cord_x, cord_y):
        gameDisplay.blit(myCar, (cord_x, cord_y))

    def crash(message):
        message_display(message, white)

    x = display_width / 2 - DEFAULT_IMAGE_WIDTH / 2
    y = display_height - DEFAULT_IMAGE_HEIGHT
    obstaclex = [0 for _ in range(no_of_obstacles)]
    obstacley = [0 for _ in range(no_of_obstacles)]
    obstacle_object = []
    for i in range(no_of_obstacles):
        obstacle_object.append(Obstacle(i, random.choice([obs1, obs2])))
        obstaclex=generate_random_x(0, display_width-obs_width,obs_width,no_of_obstacles)
        obstacley[i] = obstacle_object[i].obstacle_initial_position_generator()
    for i in range(no_of_obstacles):
        obstacle_object[i].Display_obstacle(gameDisplay, obstaclex[i], obstacley[i])

    booster_x = random.randrange(0, display_width - 50)
    booster_y = random.randrange(0, display_height-100)


    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_warning()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change_left = -5
                if event.key == pygame.K_RIGHT:
                    x_change_right = 5
                if event.key == pygame.K_UP:
                    y_change_up = -5
                if event.key == pygame.K_DOWN:
                    y_change_down = 5
                # pause functionality with P key
                if event.key == pygame.K_p:
                    pause_game()
                if event.key == pygame.K_EQUALS:
                    change_volume(True)
                    pygame.mixer.music.set_volume(game_music_volume)
                if event.key == pygame.K_MINUS:
                    change_volume(False)
                    pygame.mixer.music.set_volume(game_music_volume)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    x_change_left = 0
                if event.key == pygame.K_RIGHT:
                    x_change_right = 0
                if event.key == pygame.K_UP:
                    y_change_up = 0
                if event.key == pygame.K_DOWN:
                    y_change_down = 0
        x += (x_change_left + x_change_right)
        y += (y_change_up + y_change_down)
        gameDisplay.fill(white)
        gameDisplay.blit(bg, (0, 0))
        for i in range(no_of_obstacles):
            obstacle_object[i].Display_obstacle(gameDisplay, obstaclex[i], obstacley[i])
        car(x, y)
        DisplayScore(score)
        gameDisplay.blit(booster_image, (booster_x, booster_y))
        font = pygame.font.SysFont('None', size=25)
        text = font.render(f"+{booster_points}", True, black)
        gameDisplay.blit(text, (booster_x +5, booster_y + 5))

        if x > (display_width - DEFAULT_IMAGE_WIDTH):
            x = display_width - DEFAULT_IMAGE_WIDTH
        if x < 0:
            x = 0
        if y > (display_height - DEFAULT_IMAGE_HEIGHT):
            y = display_height - DEFAULT_IMAGE_HEIGHT
        if y < 0:
            y = 0
        for i in range(no_of_obstacles):
            print(x,y)
            if obstacley[i] > display_height:
                obstacley[i] = -obs_height
                obstaclex[i] = random.choice(generate_random_x(0, display_width-obs_width,obs_width,no_of_obstacles))
                score += 1
                obs_speed += score / 2000
            if pixel_overlap(obstacle_object[i].image, myCar, [obstaclex[i], obstacley[i]], [x,y]):
                crash(f'Oh No ... Accident..Game Over \n Your Score is {score}')
                pygame.mixer.music.stop()
                crash_sound.set_volume(game_music_volume)
                crash_sound.play()
                time.sleep(4)
                start_menu('Play Again')
                score = 0
                pygame.mixer.music.set_volume(game_music_volume)
            if pixel_overlap(booster_image, myCar, [booster_x, booster_y], [x, y]):
                boost_sound = pygame.mixer.Sound('media/music/Coin.wav')
                boost_sound.play()
                score += booster_points
                booster_x = random.randrange(0 + 25, display_width - 50)
                booster_y = random.randrange(0, display_height - 100)
                booster_points = random.randrange(7, 12)
            if booster_y > display_height:
                booster_x = random.randrange(0 + 20, display_width - 20)
                booster_y = random.randrange(0, display_height - 100)
                booster_points = random.randrange(7, 12)
            obstacley[i] += obs_speed
            booster_y += 0.1
            pygame.display.update()
        clock.tick(120)

start_menu('Start')
game_loop()
pygame.quit()
quit()
