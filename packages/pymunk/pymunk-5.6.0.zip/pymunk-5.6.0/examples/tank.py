import random

import pygame
from pygame.locals import *
#from pygame.color import *

import pymunk
from pymunk.vec2d import Vec2d
import pymunk.pygame_util

def update(space, dt, surface):
    global tank_body
    global tank_control_body

    mpos = pygame.mouse.get_pos()
    mouse_pos = pymunk.pygame_util.from_pygame( Vec2d(mpos), surface )

    mouse_delta = mouse_pos - tank_body.position
    turn = tank_body.rotation_vector.cpvunrotate(mouse_delta).angle
    tank_control_body.angle =  tank_body.angle - turn
    
    # drive the tank towards the mouse
    if ((mouse_pos - tank_body.position).get_length_sqrd() < 30**2):
        tank_control_body.velocity = 0,0
    else:
        direction = 1.0 if mouse_delta.dot(tank_body.position) > 0.0 else -1.0
        tank_control_body.velocity = tank_body.rotation_vector.cpvrotate(Vec2d(30.0*direction, 0.0))
    
    space.step(dt)
    
def add_box(space, size, mass):
    radius = Vec2d(size, size).length

    body = pymunk.Body()
    space.add(body)
    body.position = Vec2d(random.random()*(640 - 2*radius) + radius, random.random()*(480 - 2*radius) + radius)
    
    shape = pymunk.Poly.create_box(body, (size, size), 0.0)
    shape.mass = mass
    shape.elasticity = 0
    shape.friction = 0.7
    space.add(shape)
    
    return body


def init():
    ChipmunkDemoMessageString = "Use the mouse to drive the tank, it will follow the cursor.";
    
    space = pymunk.Space()
    space.iterations = 10
    space.sleep_time_threshold = 0.5
    
    static_body = space.static_body
        
    # Create segments around the edge of the screen.
    shape = pymunk.Segment(static_body, (0,0), (0,480), 0.0)
    space.add(shape)
    shape.elasticity = 1.0
    shape.friction = 1
    #cpShapeSetFilter(shape, NOT_GRABBABLE_FILTER);

    shape = pymunk.Segment(static_body, (640,0), (640,480), 0.0)
    space.add(shape)
    shape.elasticity = 1.0
    shape.friction = 1
    #cpShapeSetFilter(shape, NOT_GRABBABLE_FILTER);

    shape = pymunk.Segment(static_body, (0,0), (640,0), 0.0)
    space.add(shape)
    shape.elasticity = 1.0
    shape.friction = 1
    #cpShapeSetFilter(shape, NOT_GRABBABLE_FILTER);

    shape = pymunk.Segment(static_body, (0,480), (640,480), 0.0)
    space.add(shape)
    shape.elasticity = 1
    shape.friction = 1
    #cpShapeSetFilter(shape, NOT_GRABBABLE_FILTER);
    
    for x in range(50):
        body = add_box(space, 20, 1)
        
        pivot = pymunk.PivotJoint(static_body, body, (0,0), (0,0))
        space.add(pivot)
        pivot.max_bias = 0 # disable joint correction
        pivot.max_Force = 1000 # emulate linear friction
        
        gear = pymunk.GearJoint(static_body, body, 0.0, 1.0)
        space.add(gear)
        gear.max_bias = 0 # disable joint correction
        gear.max_force = 5000  # emulate angular friction
    
    # We joint the tank to the control body and control the tank indirectly by modifying the control body.
    global tank_control_body
    tank_control_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    tank_control_body.position = 320, 240
    space.add(tank_control_body)
    global tank_body
    tank_body = add_box(space, 30, 10)
    tank_body.position = 320, 240
    
    pivot = pymunk.PivotJoint(tank_control_body, tank_body, (0,0), (0,0))
    space.add(pivot)
    pivot.max_bias = 0 # disable joint correction
    pivot.max_force = 10000 # emulate linear friction
    
    gear = pymunk.GearJoint(tank_control_body, tank_body, 0.0, 1.0)
    space.add(gear)	
    gear.error_bias = 0 # attempt to fully correct the joint each step
    gear.max_bias = 1.2  # but limit it's angular correction rate
    gear.max_force = 50000 # emulate angular friction
        
    return space

space = init()

screen = pygame.display.set_mode((800,600)) 
clock = pygame.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(screen)

while True:
	for event in pygame.event.get():
		if event.type == QUIT or \
			event.type == KEYDOWN and (event.key in [K_ESCAPE, K_q]): 
			exit()
	
	screen.fill(pygame.color.THECOLORS["black"])
	space.debug_draw(draw_options)
	fps = 60.0
	update(space, 1/fps, screen)
	pygame.display.flip()
	
	clock.tick(fps)