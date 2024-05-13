import pygame
import os

pygame.font.init()
pygame.mixer.init()

bullet_hit_sound = pygame.mixer.Sound(os.path.join('assets', 'Grenade+1.mp3'))
bullet_fire_sound = pygame.mixer.Sound(os.path.join('assets', 'Gun+Silencer.mp3'))

vel = 5
bullet_vel = 7
max_bullets = 3

yellow_hit = pygame.USEREVENT + 1
red_hit = pygame.USEREVENT + 2

health_font = pygame.font.SysFont("comicsans", 40)
winner_font = pygame.font.SysFont("comicsans", 100)

width, height = 900, 500

# setting window's height and width
screen = pygame.display.set_mode((width, height))

# setting border in the middle of the window
border = pygame.Rect(width/2 - 5, 0, 10, height)

# setting game's name
pygame.display.set_caption("Spaceship Fight")

# setting spaceship's width and height
spaceship_width, spaceship_height = 60, 50

# loading image from the "asset" folder
yellow_spaceship_image = pygame.image.load("assets\spaceship_yellow.png")

# rotating the image so that the spaceship faces its opponent
yellow_spaceship = pygame.transform.rotate(pygame.transform.scale(
    yellow_spaceship_image, (spaceship_width, spaceship_height)), 90)

red_spaceship_image = pygame.image.load("assets\spaceship_red.png")
red_spaceship = pygame.transform.rotate(pygame.transform.scale(
    red_spaceship_image, (spaceship_width, spaceship_height)), 270)

# scaling the background image for the game so that it covers the entire window
space = pygame.transform.scale(pygame.image.load(os.path.join("assets", "space.png")), (width, height))

def draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health):
    # displaying background image
    screen.blit(space, (0, 0))

    # displaying player's HP
    red_health_text = health_font.render(f"Health: {red_health}", 1, (255, 255, 255))
    yellow_health_text = health_font.render(f"Health: {yellow_health}", 1, (255, 255, 255))
    screen.blit(red_health_text, (width - red_health_text.get_width() - 10, 10))
    screen.blit(yellow_health_text, (10, 10))

    # displaying spaceship images
    screen.blit(yellow_spaceship, (yellow.x, yellow.y))
    screen.blit(red_spaceship, (red.x, red.y))

    # displaying border
    pygame.draw.rect(screen, (255, 0, 0), border)

    # displaying bullets
    for bullet in yellow_bullets:
        pygame.draw.rect(screen, (255, 255, 0), bullet)

    for bullet in red_bullets:
        pygame.draw.rect(screen, (255, 0, 0), bullet)

    # updating the window
    pygame.display.update()

def yellow_movement(keys_pressed, yellow):
    # making sure that the yellow spaceship doesn't go off the window once it reaches the left border
    if keys_pressed[pygame.K_a] and yellow.x > 0:
        yellow.x -= vel

    # making sure that the yellow spaceship doesn't cross the middle border
    if keys_pressed[pygame.K_d] and yellow.x + yellow.height < border.x:
        yellow.x += vel

    # making sure that the yellow spaceship doesn't go off the window once it reaches the top
    if keys_pressed[pygame.K_w] and yellow.y > 0:
        yellow.y -= vel

    # making sure that the yellow spaceship doesn't go off the window once it reaches the bottom
    if keys_pressed[pygame.K_s] and yellow.y + yellow.width < 500:
        yellow.y += vel

def red_movement(keys_pressed, red):
    # making sure that the red spaceship doesn't cross the middle border
    if keys_pressed[pygame.K_LEFT] and red.x > border.x + border.width:
        red.x -= vel

    # making sure that the red spaceship doesn't go off the window once it reaches the right border
    if keys_pressed[pygame.K_RIGHT] and red.x + red.height < 900:
        red.x += vel

    # making sure that the red spaceship doesn't go off the window once it reaches the top
    if keys_pressed[pygame.K_UP] and red.y > 0:
        red.y -= vel

    # making sure that the red spaceship doesn't go off the window once it reaches the bottom
    if keys_pressed[pygame.K_DOWN] and red.y + red.width < 500:
        red.y += vel

def handle_bullets(yellow_bullets, red_bullets, yellow, red):

    for bullet in yellow_bullets:
        bullet.x += bullet_vel
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(red_hit))
            yellow_bullets.remove(bullet)
        elif bullet.x > 900:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= bullet_vel
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(yellow_hit))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):

    draw_text = winner_font.render(text, 1, (255, 255, 255))
    screen.blit(draw_text, (width / 2 - draw_text.get_width() / 2, height / 2 - draw_text.get_height() / 2))

    pygame.display.update()
    pygame.time.delay(5000)

def main():

    yellow = pygame.Rect(225, 250, spaceship_width, spaceship_height)
    red = pygame.Rect(675, 250, spaceship_width, spaceship_height)

    yellow_bullets = []
    red_bullets = []

    yellow_health = 5
    red_health = 5

    clock = pygame.time.Clock()
    running = True

    while running:

        clock.tick(60)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LCTRL and len(yellow_bullets) < max_bullets:

                    bullet = pygame.Rect(yellow.x + yellow.height, yellow.y + (yellow.width / 2 - 5), 10, 5)
                    yellow_bullets.append(bullet)
                    bullet_fire_sound.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < max_bullets:

                    bullet = pygame.Rect(red.x, red.y + (red.width / 2 - 5), 10, 5)
                    red_bullets.append(bullet)
                    bullet_fire_sound.play()

            if event.type == red_hit:
                red_health -= 1
                bullet_hit_sound.play()

            if event.type == yellow_hit:
                yellow_health -= 1
                bullet_hit_sound.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "YELLOW WINS!"

        if yellow_health <= 0:
            winner_text = "RED WINS!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        yellow_movement(pygame.key.get_pressed(), yellow)
        red_movement(pygame.key.get_pressed(), red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health)

    main()

if __name__ == "__main__":
    main()