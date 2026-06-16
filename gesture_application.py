# application for task 3
# gesture input program for first task
import pyglet
from pyglet import window, shapes, sprite
from pyglet.window import mouse
import recognizer
from recognizer import Point, Unistroke
import random
import time
import os

WINDOW_HEIGHT= 800
WINDOW_WIDTH = 300

BANNER_HEIGHT = 200
MONSTER_HEIGHT = 300
INPUT_HEIGHT = 300

win = window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)
input = pyglet.graphics.Batch()
ui = pyglet.graphics.Batch()
positions = []
bubbles = []
padding = 20
timer = 60
colour = (112, 66, 20)
game_inst = pyglet.text.Label("Welcome to Monster Attack. \n \nDraw the correct gestures to defeat the monsters.\n \n3 attacks defeat an enemy. You have to beat 6 monsters to win. \nBut beware! There is a time limit. \n\nPress 'P' to start playing.",
                          font_name='Times New Roman',
                          font_size=28,
                          x=win.width//2, y=win.height//2,
                          width = WINDOW_WIDTH- padding*2,
                          multiline=True,
                          color=colour,
                          anchor_x='center', anchor_y='center')
result = pyglet.text.Label("You lost!\n To play again press 'S',\n to quit game press 'Q'",
                          font_name='Times New Roman',
                          font_size=36,
                          x=win.width//2, y=win.height//2,
                          width = WINDOW_WIDTH- padding*2,
                          multiline=True,
                          color=colour,
                          anchor_x='center', anchor_y='center')
instruction = pyglet.text.Label('Defeat the enemies!', 
                                font_name='Times New Roman',
                                font_size=22,
                                x=WINDOW_WIDTH/2, y=WINDOW_HEIGHT-padding, color=colour,
                                anchor_x='center', anchor_y='center')
timer_label = pyglet.text.Label(f"{timer}", 
                                font_name='Times New Roman',
                                font_size=50,
                                x=WINDOW_WIDTH/2, y=WINDOW_HEIGHT-BANNER_HEIGHT/2, color=colour,
                                anchor_x='center', anchor_y='center')
background = shapes.Rectangle(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, color=(255, 255, 255), batch=ui)
filter = shapes.Rectangle(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, color=colour)
filter.opacity = 128
monster_1_img = pyglet.resource.image('assets/monster_1.png')
monster_1_img.anchor_x = monster_1_img.width/2
monster_2_img = pyglet.resource.image('assets/monster_2.png')
monster_2_img.anchor_x = monster_2_img.width/2
monster_3_img = pyglet.resource.image('assets/monster_3.png')
monster_3_img.anchor_x = monster_3_img.width/2
monster_4_img = pyglet.resource.image('assets/monster_4.png')
monster_4_img.anchor_x = monster_4_img.width/2
monster_5_img = pyglet.resource.image('assets/monster_5.png')
monster_5_img.anchor_x = monster_5_img.width/2
monster_6_img = pyglet.resource.image('assets/monster_6.png')
monster_6_img.anchor_x = monster_6_img.width/2
monster = sprite.Sprite(monster_1_img, WINDOW_WIDTH/2, BANNER_HEIGHT + MONSTER_HEIGHT/2, batch=ui)
line = shapes.Line(0, INPUT_HEIGHT, WINDOW_WIDTH, INPUT_HEIGHT, thickness=5, color=colour, batch=ui)

# game logic parameters
last_i = 5
attack = []
attack_img = []
current_attack_amount = 0
current_monster = 1
monster_amount = 6
attack_per_mon = 3
time_check = 0
game_running = True
screen_1 = True

rec = recognizer.DollarRecognizer()

class Bubble:
    def __init__(self, x, y, colour, chosen_batch):
        self.bubble = shapes.Circle(x, y, 2, color=colour, batch=chosen_batch)

# randomizes chosen attack
def chooseAttack():
    global attack, last_i
    i = last_i
    while i == last_i:
        i = random.randint(0, 4)
    attack = rec.Unistrokes[i]
    last_i = i

# generates the image to display attack that needs to be performed
def createAttackImg():
    global attack, attack_img
    for point in attack.points_original:
        y = INPUT_HEIGHT - point.y
        attack_img.append(Bubble(point.x, y, colour, ui))

def clearBubbles(bubbles):
    for bubble in bubbles:
        bubble.bubble.delete()
    positions.clear()
    bubbles.clear()

def clearInputField():
    clearBubbles(attack_img)
    clearBubbles(bubbles)
    chooseAttack()
    createAttackImg()

def initGame():
    global time_check, game_won, game_running, current_attack_amount, current_monster, timer, screen_1
    clearInputField()
    monster.image = monster_1_img
    monster.scale = 0.2
    timer = 60
    timer_label.text = f"{timer}"
    time_check = time.time()
    game_won = False
    game_running = True
    current_attack_amount = 0
    current_monster = 1
    screen_1 = True

def updateGame():
    global game_won, current_attack_amount, attack_per_mon, current_monster, monster_amount, game_running, game_won
    current_attack_amount += 1
    if current_attack_amount == attack_per_mon:
        current_attack_amount = 0
        if current_monster == monster_amount:
            game_running = False
            game_won = True
            result.text = "You won the game\n To play again press 'S',\n to quit game press 'Q'"
        else:
            current_monster += 1
            if current_monster == 2:
                monster.image = monster_2_img
                monster.scale = 0.3
                clearInputField()
            elif current_monster == 3:
                monster.image = monster_3_img
                monster.scale = 0.4
                clearInputField()
            elif current_monster == 4:
                monster.image = monster_4_img
                monster.scale = 0.1
                clearInputField()
            elif current_monster == 5:
                monster.image = monster_5_img
                clearInputField()
                monster.scale = 0.4
            elif current_monster == 6:
                monster.image = monster_6_img
                monster.scale = 0.1
                clearInputField()
    else:
        clearInputField()


initGame()

@win.event
def on_mouse_press(x, y, button, modifiers):
    clearBubbles(bubbles)

@win.event
def on_mouse_release(x, y, button, modifiers):
    global result
    res = rec.recognize(positions, False)
    if res.name == attack.name:
        updateGame()

@win.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if buttons & mouse.LEFT:
        positions.append(Point(x, WINDOW_HEIGHT-y))
        bubbles.append(Bubble(x, y, (255, 0, 0), input))


@win.event 
def on_key_press(symbol, modifiers):
    global screen_1
    if (symbol == window.key.Q):
        os._exit(0)
    if (symbol == window.key.S):
        initGame()
    if (symbol == window.key.P):
        if screen_1:
            screen_1 = False

@win.event
def on_draw():
    global timer, game_running, time_check
    win.clear()
    background.draw()
    if screen_1:
        game_inst.draw()
    else:
        if time.time()-time_check >= 1:
            timer -= 1
            timer_label.text = f"{timer}"
            time_check = time.time()
            if timer <= 0:
                game_running = False
                if game_won:
                    pass
                else:
                    result.text = "You lost!\n To play again press 'S',\n to quit game press 'Q'"
        if game_running:
            ui.draw()
            instruction.draw()
            timer_label.draw()
            input.draw()
        else: 
            result.draw()
    filter.draw()
    

pyglet.app.run()
