import pygame
from pygame.draw import *
import math
from random import randint, random
pygame.init()

FPS = 2
screen = pygame.display.set_mode((1200, 900))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

scores = 0

def get_e_vector(dx, dy):
    '''
    Returns unit vector codirectional to
    vector with given coordinates

    Parameters
    ----------
    dx : float
        X-coordinate of  vector
    dy : float
        Y-coordinate of vector

    Returns
    -------
    list
        Coordinates of unit vector
        coodirectional to vector = {dx, dy}

    '''
    if dx != 0:    
        a = math.atan2(dy, dx)
    else:
        return [0, dy / abs(dy)]
    
    return [math.cos(a), math.sin(a)]

def scalar_product_2D(a, b):
    '''
    Scalar product of given vectors

    Parameters
    ----------
    a : list
        Coordinates of first vector.
    b : list
        Coordinates of second vector.

    Returns
    -------
    float
        Scalar product of given vectors.

    '''
    return a[0] * b[0] + a[1] * b[1]

def vector_sum(a, b):
    '''
    Sum of given vectors

    Parameters
    ----------
    a : list
        Coordinates of first vector.
    b : list
        Coordinates of second vector.

    Returns
    -------
    list
        Coordinates of sum of given vectors.

    '''
    return [a[0] + b[0], a[1] + b[1]]

def vector_sub(a, b):
    '''
    Subtraction vector b from vector a

    Parameters
    ----------
    a : list
        Coordinates of first vrctor.
    b : list
        Coordinates of second vector.

    Returns
    -------
    list
        Coordinates of subtraction vector b
        from vector a

    '''
    return [a[0] - b[0], a[1] - b[1]]

def get_length(a):
    '''
    Returns absolute value of vector a

    Parameters
    ----------
    a : list
        Coordinates of given vector.

    Returns
    -------
    float
        Absolute value of given vector.

    '''
    return math.sqrt(a[0]**2 + a[1]**2)

def get_angle(v):
    '''
    Returns angle between vector v and X axis

    Parameters
    ----------
    v : list
        Coordinates of given vector.

    Returns
    -------
    float
        Angle between vector v and X axis 
        in radians.

    '''
    if v[1] == 0:
        if v[0] < 0:
            return math.pi 
        else: 
            return 0
    if v[0] == 0:
        return math.pi / 2 * v[1] / abs(v[1])
    return math.atan2(v[1], v[0])

balls = []

def balls_collisions():
    '''
    This function checks if any 2 circles collide and, if so,
    calculates their velocities after collision

    Returns
    -------
    None.

    '''
    for i in range(len(balls)):
        for j in range(i+1, len(balls)):            
            v_i = balls[i]['v']
            v_j = balls[j]['v']
            n = get_e_vector(balls[i]['x'] - balls[j]['x'], balls[i]['y'] - balls[j]['y'])

            v_i_n = [n[0] * scalar_product_2D(v_i, n), n[1] * scalar_product_2D(v_i, n)]
            v_i_t = vector_sub(v_i, v_i_n)

            v_j_n = [n[0] * scalar_product_2D(v_j, n), n[1] * scalar_product_2D(v_j, n)]
            v_j_t = vector_sub(v_j, v_j_n)

            if (balls[i]['x'] - balls[j]['x'])**2 + (balls[i]['y'] - balls[j]['y'])**2 <= (balls[i]['r'] + balls[j]['r'] + (get_length(v_i_n) + get_length(v_j_n))*FPS)**2:               
                balls[i]['v'] = vector_sum(v_i_t, v_j_n)
                balls[j]['v'] = vector_sum(v_j_t, v_i_n)

def walls_collisions(random_):
    '''
    This function checks if any circle collides the wall and, if so,
    calculates ball's speed after collision

    Parameters
    ----------
    random_ : bool
        is velocity after collision random

    Returns
    -------
    None.

    '''
    
    for t in balls:
        if t['x'] <= -t['v'][0]*FPS + t['r']  or t['x'] >= 1200 - t['v'][0]*FPS - t['r']:
            if random_ == False:
                t['v'] = [-t['v'][0], t['v'][1]]
            else:
                t['v'] = [-t['v'][0] / abs(t['v'][0]) * 5 * random(), 10 * random() - 5]
                
        if t['y'] <= -t['v'][1]*FPS + t['r']  or t['y'] >= 900 - t['v'][1]*FPS - t['r']:
            if random_ == False:
                t['v'] = [t['v'][0], -t['v'][1]]
            else:
                t['v'] = [10 * random() - 5, -t['v'][1] / abs(t['v'][1]) * 5 * random()]
                
def new_ball():
    '''
    Draws new ball with random position,
    color and radius which are saved as global
    variables;
    adds new ball balls array

    Returns
    -------
    None.

    '''
    global x, y, r, v, color
    
    no_coll = False
    
    while not no_coll:
        r = randint(30,50)
        x = randint(r,1200 - r)
        y = randint(r,900 - r)
        v = [10 * random() - 5, 10 * random() - 5]
        color = COLORS[randint(0, 5)]   
        
        if len(balls) == 0:
            break
        
        for b in balls:
            if (b['x'] - x) ** 2 + (b['y'] - y) ** 2 <= (b['r'] + r) ** 2:
                no_coll = False
                break
            else: 
                no_coll = True
        
    balls.append({'x' : x, 'y' : y, 'r' : r, 'v' : v, 'color' : color})

def draw_balls():
    for b in balls:
        circle(screen, b['color'], (b['x'], b['y']), b['r'])

def click(event):
    '''
    Checks if click is in circle and, if so, returns this circle

    Parameters
    ----------
    event : pygame.event
        Event of click

    Returns
    -------
    bool
        Is click inside last circle created by
        new_ball().

    '''
    for b in balls:
        if (b['x'] - event.pos[0]) ** 2 + (b['y'] - event.pos[1]) ** 2 <= b['r'] ** 2:
            return b
    
    return False
    
for i in range(7):
    new_ball()

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for b in balls:
        b['x'] += b['v'][0] * FPS
        b['y'] += b['v'][1] * FPS
    balls_collisions()
    walls_collisions(True)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            res = click(event)
            if res != False:
                scores += 1
                balls.remove(res)
                new_ball()
    draw_balls()
    pygame.display.update()
    screen.fill(BLACK)

print(scores)

pygame.quit()