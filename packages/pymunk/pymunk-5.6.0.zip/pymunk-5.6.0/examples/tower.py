import math

import pygame
from pygame.locals import *

import pymunk
from pymunk.vec2d import Vec2d
import pymunk.pygame_util 

fps = 30
dt = 1./fps

landed_previous = False
direction = 1
remaining_jumps = 2
landing = {'p':Vec2d.zero(), 'n':0}
frame_number = 0

PLAYER_MASS = 5

HEAD_FRICTION = 0.7

PLAYER_VELOCITY = 200
PLAYER_GROUND_ACCEL_TIME = 0.05
PLAYER_GROUND_ACCEL = (PLAYER_VELOCITY/PLAYER_GROUND_ACCEL_TIME)

PLAYER_AIR_ACCEL_TIME = 0.25
PLAYER_AIR_ACCEL = (PLAYER_VELOCITY/PLAYER_AIR_ACCEL_TIME)

JUMP_HEIGHT = 16.*3
JUMP_CUTOFF_VELOCITY = 100
FALL_VELOCITY = 500

ENEMY_VELOCITY = 180
ENEMY_JUMP_FREQ = 0.01
ENEMY_JUMP_HEIGHT = 25

pygame.init()
screen = pygame.display.set_mode((320,180))#, flags=pygame.SCALED)
clock = pygame.time.Clock()

space = pymunk.Space()
draw_options = pymunk.pygame_util.DrawOptions(screen)

space.gravity = 0,-1000
space.sleep_time_threshold = 0.3

r = 2
static = [
    pymunk.Segment(space.static_body, (0, 0), (320, 0), r),
    pymunk.Segment(space.static_body, (320, 0), (320, 180), r),
    #pymunk.Segment(space.static_body, (320, 180), (0, 180), r),
    pymunk.Segment(space.static_body, (0, 180), (0, 0), r)
    ]
for s in static:
    s.friction = 1
space.add(static)

#player
player_body = pymunk.Body(PLAYER_MASS, pymunk.inf)
player_body.position = 100,100

head = pymunk.Circle(player_body, 10, (0,5))
head2 = pymunk.Circle(player_body, 10, (0,13))
feet = pymunk.Circle(player_body, 10, (0,-5))
feet.friction = 1
space.add(player_body, head, head2, feet)

def cpfclamp(f, min_, max_):
    """Clamp f between min and max"""
    return min(max(f, min_), max_)

def cpflerpconst(f1, f2, d):
    """Linearly interpolate from f1 to f2 by no more than d."""
    return f1 + cpfclamp(f2 - f1, -d, d)

def calc_grounding(body):
    grounding = {
        'normal' : Vec2d.zero(),
        'penetration' : Vec2d.zero(),
        'impulse' : Vec2d.zero(),
        'position' : Vec2d.zero(),
        'body' : None
    }
    # find out if player is standing on ground, and if standing on multiple 
    # objects pick the one with straightest collision normal as collision body.
    def f(arbiter):
        n = -arbiter.contact_point_set.normal
        if n.y > grounding['normal'].y:
            grounding['normal'] = n
            grounding['body'] = arbiter.shapes[1].body
            #grounding['penetration'] = -arbiter.contact_point_set.points[0].distance
            #grounding['impulse'] = arbiter.total_impulse
            #grounding['position'] = arbiter.contact_point_set.points[0].point_b
    body.each_arbiter(f)
    return grounding


grounding = calc_grounding(player_body)

#if self.force[0] and grounding['body']
#    grounding['body'].apply_force_at_world_point((-self.force[0], 0), grounding['position'])
#well_grounded = False

#if grounding['body'] != None and abs(grounding['normal'].x/grounding['normal'].y) < feet.friction:
#    well_grounded = True
#    remaining_jumps = 2
import random
for x in range(2):

    b = pymunk.Body()
    b.position = random.randint(1,100),60
    c = pymunk.Circle(b, 10)
    c.mass = PLAYER_MASS
    c.friction = 0.5
    space.add(b,c)

for x in range(50):
    b = pymunk.Body()
    b.position = random.randint(1,300),120
    c = pymunk.Poly(b, [
        (random.randint(1,30),random.randint(1,30)),
        (random.randint(1,30),random.randint(1,30)),
        (random.randint(1,30),random.randint(1,30)),
        (random.randint(1,30),random.randint(1,30))
    ], radius = 2)
    c.mass = PLAYER_MASS/3
    c.friction = 0.5
    c.color = pygame.color.THECOLORS['red']
    space.add(b,c)


def spawn_enemy():
    b = pymunk.Body(2, pymunk.inf)
    b.position = random.randint(5,315), 170
    s1 = pymunk.Circle(b, 10)
    #s1.mass = 2
    s1.friction = 0.7
    s2 = pymunk.Circle(b, 10, offset = (0,20))
    #s2.mass = 2
    s2.friction = 0.7
    s3 = pymunk.Circle(b, 11, offset = (0,-10))
    s3.friction = 0.7
    s3.color = pygame.color.THECOLORS['purple']
    b.feet = s3
    s1.color = s2.color = pygame.color.THECOLORS['green']

    space.add(b, s1, s2, s3)
    
    return b
    
enemies = [
    spawn_enemy(),
    spawn_enemy(),
    spawn_enemy(),
    spawn_enemy(),
    spawn_enemy(),
]

while True:
    grounding = calc_grounding(player_body)

    well_grounded = False
    if grounding['body'] != None and abs(grounding['normal'].x/grounding['normal'].y) < feet.friction:
        well_grounded = True
        remaining_jumps = 2

    ground_velocity = Vec2d.zero()
    if well_grounded:
        ground_velocity = grounding['body'].velocity

    for event in pygame.event.get():
        if event.type == QUIT or \
            event.type == KEYDOWN and (event.key in [K_ESCAPE, K_q]):  
            exit()
        elif event.type == KEYDOWN and event.key == K_UP:
            if well_grounded or remaining_jumps > 0:                    
                jump_v = math.sqrt(2.0 * JUMP_HEIGHT * abs(space.gravity.y))
                impulse = (0,player_body.mass * (ground_velocity.y+jump_v))
                player_body.apply_impulse_at_local_point(impulse)
                remaining_jumps -=1
        elif event.type == KEYUP and event.key == K_UP:                
            player_body.velocity.y = min(player_body.velocity.y, JUMP_CUTOFF_VELOCITY)

    # Let player walk
    target_vx = 0
    keys = pygame.key.get_pressed()
    if (keys[K_LEFT]):
        direction = -1
        target_vx -= PLAYER_VELOCITY
    if (keys[K_RIGHT]):
        direction = 1
        target_vx += PLAYER_VELOCITY

    feet.surface_velocity = -target_vx, 0


    if grounding['body'] != None:
        feet.friction = -PLAYER_GROUND_ACCEL/space.gravity.y
        head.friciton = HEAD_FRICTION
    else:
        feet.friction,head.friction = 0,0

    #air control
    if grounding['body'] == None:
        player_body.velocity = Vec2d(
            cpflerpconst(player_body.velocity.x, target_vx + ground_velocity.x, PLAYER_AIR_ACCEL*dt), 
            player_body.velocity.y
            )
        
    player_body.velocity = Vec2d(
        player_body.velocity.x, 
        max(player_body.velocity.y, -FALL_VELOCITY) # clamp upwards as well?
    )

    # Did we land?
    if abs(grounding['impulse'].y) / player_body.mass > 200 and not landed_previous:
        #sound.play()
        landing = {'p':grounding['position'],'n':5}
        landed_previous = True
    else:
        landed_previous = False
    if landing['n'] > 0:
        p = pymunk.pygame_util.to_pygame(landing['p'], screen)
        pygame.draw.circle(screen, pygame.color.THECOLORS['yellow'], p, 5)
        landing['n'] -= 1

    # ai for enemies
    for enemy in enemies:
        v = (enemy.position - player_body.position).normalized() * ENEMY_VELOCITY
        enemy.feet.surface_velocity = v
        if random.random() > 1-ENEMY_JUMP_FREQ:
            jump_v = math.sqrt(2.0 * ENEMY_JUMP_HEIGHT * abs(space.gravity.y))
            impulse = -v.x, enemy.mass * jump_v
            enemy.apply_impulse_at_local_point(impulse)
                

    screen.fill(pygame.color.THECOLORS["black"])
    space.debug_draw(draw_options)
    space.step(dt)
    pygame.display.flip()

    pygame.display.set_caption(f"fps: {clock.get_fps():.1f}")
    clock.tick(fps)
    
