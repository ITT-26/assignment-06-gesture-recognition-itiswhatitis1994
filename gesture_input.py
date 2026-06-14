# gesture input program for first task
import pyglet
from pyglet import window, shapes
from pyglet.window import mouse
import recognizer
from recognizer import Point

WINDOW_HEIGHT= 300
WINDOW_WIDTH = 300

win = window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)
batch = pyglet.graphics.Batch()
positions = []
bubbles = []
label = pyglet.text.Label('You drew a ...',
                          font_name='Times New Roman',
                          font_size=36,
                          x=win.width//2, y=win.height//2,
                          anchor_x='center', anchor_y='center')
result = False

rec = recognizer.DollarRecognizer()

class Bubble:
    def __init__(self, x, y):
        self.bubble = shapes.Circle(x, y, 2, color=(207,159,255), batch=batch)


@win.event
def on_mouse_press(x, y, button, modifiers):
    global result
    for bubble in bubbles:
        bubble.bubble.delete()
    positions.clear()
    bubbles.clear()
    result = False
    pass

@win.event
def on_mouse_release(x, y, button, modifiers):
    global result
    res = rec.recognize(positions, False)
    result = True
    label.text = res.name
    pass

@win.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if buttons & mouse.LEFT:
        positions.append(Point(x, WINDOW_HEIGHT-y))
        bubbles.append(Bubble(x, y))

@win.event
def on_draw():
    win.clear()
    batch.draw()
    if result:
        label.draw()
    

pyglet.app.run()
