import random
from random import randint
import pgzrun
from pgzero.actor import Actor
# from pgzero.game import screen
from pgzero.keyboard import keyboard
from pygame.examples.grid import TITLE
from pygame.examples.moveit import HEIGHT
from ultimate_save import save
from ultimate_save import save_lives, load_lives
from ultimate_save import load_score
from pygame import Rect
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'

HEIGHT = 540
WIDTH = 960
TITLE = 'WHY?'
FPS = 60
score = 0
game_state = 'menu'
#cheli
background = Actor('arena')
hero = Actor('1-peppo',(WIDTH/2,HEIGHT-121))
toppins = []
load_button = Actor('load',(WIDTH-60,150))
save_button = Actor('save',(WIDTH-60,100))
faces = []
fakers = []
hpi = []
start_button = Rect((WIDTH // 2 - 100, HEIGHT // 2 - 60), (200, 50))
exit_button = Rect((WIDTH // 2 - 100, HEIGHT // 2 + 10), (200, 50))

#sozdanie sira
def resp_cheese():
        toppin = Actor('cheeso')
        toppin.y = randint(-200, -100)
        toppin.x = randint(40, WIDTH - 40)
        toppin.speed = randint(4,7 )
        toppins.append(toppin)


#sozdanie clonov
def resp_clones():
        faker = Actor('fakefall')
        faker.y = randint(-590,-300)
        faker.x = randint(40,WIDTH-40)
        faker.speed = randint(4,5)
        fakers.append(faker)


def resp_pizza():
    face = Actor('noose')
    face.y = randint(-500,-300)
    face.x = randint(40, WIDTH - 40)
    face.speed = 6
    faces.append(face)

# hpeshki
def resp_hp():
    hp = Actor('hpeshka')
    hp.x = 30+(50 * len(hpi))
    hpi.append(hp)

def game_begins(hepeshki=False):
    for i in range(1):
        resp_pizza()
    for i in range(10):
        resp_clones()
    for i in range(80):
        resp_cheese()
    if hepeshki:
        for i in range(hepeshki):
            resp_hp()


game_begins(hepeshki=6)


die = Actor('game',(WIDTH/2,HEIGHT/2))
#risuem
def draw():
    if game_state == 'menu':
        screen.fill((30, 30, 30))
        screen.draw.text('Меню', center=(WIDTH // 2, HEIGHT // 2 - 120), fontsize=70, color='white')
        screen.draw.filled_rect(start_button, (70, 170, 255))
        screen.draw.text('start',center = start_button.center,fontsize=40,color='white')
        screen.draw.filled_rect(exit_button, (70, 170, 255))
        screen.draw.text('exit', center=exit_button.center, fontsize=40, color='white')
        load_button.draw()

    elif game_state == 'game':
        background.draw()
        hero.draw()
        for face in faces:
            face.draw()

        for topin in toppins:
            topin.draw()

        for faker in fakers:
            faker.draw()

        for hp in hpi:
            hp.draw()
        screen.draw.text(f'score: {str(score)}', (WIDTH - 150, 20), fontsize=40)
        save_button.draw()
    elif game_state == 'game_over':
        screen.fill('black')
        die.draw()
        load_button.draw()
        screen.draw.text('close the window or load from last save file', center=(WIDTH / 2 - 10, HEIGHT / 2 + 80),fontsize=50)


#move
def update():
     global score,game_state
     if game_state == 'game':
         if keyboard.left and hero.x > 40:
             hero.x -= 7
         if keyboard.right and hero.x <WIDTH-40:
             hero.x += 7
         for toppin in toppins:
            if toppin.y <= HEIGHT:
                toppin.y += toppin.speed
            if hero.colliderect(toppin):
                toppins.remove(toppin)
                resp_cheese()
                score +=1
            if toppin.y >= HEIGHT:
                toppins.remove(toppin)
                resp_cheese()
         for face in faces:
             if face.y <= HEIGHT:
                 face.y += face.speed
             if hero.colliderect(face)and len(hpi)!= 0:
                 hpi.pop()
                 faces.remove(face)
                 resp_pizza()
             if face.y >= HEIGHT:
                 faces.remove(face)
                 resp_pizza()
             if face.x > hero.x:
                face.x -= 1
             else:
                 face.x += 1
         for faker in fakers:
            if faker.y <= HEIGHT:
                faker.y +=faker.speed
            if hero.colliderect(faker) and len(hpi)!= 0:
                fakers.remove(faker)
                hpi.pop()
                resp_clones()

            if faker.y >= HEIGHT:
                fakers.remove(faker)
                resp_clones()
            if len(hpi) == 0 :
                save(score)
                game_state = 'game_over'

def on_mouse_down(pos,button):
    global score,game_state
    if button == mouse.LEFT and save_button.collidepoint(pos):
        save_lives(len(hpi))
        save(score)
    if button == mouse.LEFT and load_button.collidepoint(pos):
        a = load_lives()
        hpi.clear()
        fakers.clear()
        toppins.clear()
        faces.clear()
        score = load_score()
        game_begins(hepeshki=a)
        game_state = 'game'
    if game_state == 'menu':
        if mouse.LEFT and start_button.collidepoint(pos):
            game_state = 'game'
        if mouse.LEFT and exit_button.collidepoint(pos):
            exit()

def on_key_down(key):
    global game_state
    if key == keys.ESCAPE:
        game_state = 'menu'
        hpi.clear()
        fakers.clear()
        toppins.clear()
        faces.clear()
        game_begins()


pgzrun.go()