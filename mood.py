#!/usr/bin/env python

import time
import random
import math
from gridmap import GridMap, GridRay, GridWall
from microgfx import Gfx
from maps import DefaultMap, DefaultMapTiles
from mob import Mob
import pygame

#from guppy import hpy

ZOOM = 2
SCREEN_H = 64
SCREEN_W = 128
#SCREEN_H = 480
#SCREEN_W = 640
#SCREEN_H = 240
#SCREEN_W = 320

X = 0
Y = 1

START = 0
END = 1

def pick_wall_color( wall ):
   color = (255, 255, 255)
   return color

def pick_wall_pattern( wall ):
   return Gfx.PATTERN_STRIPES_DIAG_1 if GridWall.SIDE_NS == wall.side else \
   Gfx.PATTERN_HASH

def pick_top_pattern( wall ):
   return Gfx.PATTERN_STRIPES_HORIZ

def mood( pyg, screen_sz=(SCREEN_W, SCREEN_H), zoom=ZOOM ):
   gfx = Gfx( pyg, screen_sz, zoom )
   gmap = GridMap( DefaultMap, DefaultMapTiles )
   tiles = DefaultMapTiles
   ticks = 0
   mspeed = 0.5
   running = True

   while( running ):

      gfx.blank( (0, 0, 0) )

      prev_ticks = ticks
      ticks = time.clock()
      frame_ticks = (ticks - prev_ticks) / 1000.0
      rspeed = 0.5

      # Poll interaction events.
      for event in pygame.event.get():
         if pygame.QUIT == event.type:
            running = False
         elif pygame.KEYDOWN == event.type:
            if pygame.K_ESCAPE == event.key:
               running = False

      keys = pygame.key.get_pressed()
      if keys[pygame.K_RIGHT]:
         gfx.rotate( -1 * rspeed )
      if keys[pygame.K_LEFT]:
         gfx.rotate( rspeed )
      if keys[pygame.K_UP]:
         new_x = gfx.pos[X]
         new_y = gfx.pos[Y]
         if not gmap.collides( \
         (int(gfx.pos[X] + gfx.facing[X] * (mspeed * 2)), int(gfx.pos[Y])) ):
            new_x = gfx.pos[X] + (gfx.facing[X] * mspeed)
         if not gmap.collides( \
         (int(gfx.pos[X]), int(gfx.pos[Y] + gfx.facing[Y] * mspeed)) ):
            new_y = gfx.pos[Y] + (gfx.facing[Y] * (mspeed * 2))
         gfx.pos = (new_x, new_y)

      # Draw the walls.
      for x in range( 0, screen_sz[X] - 1 ):
         ray = None
         try:
            ray = GridRay( gmap, x, gfx.pos, gfx.facing, gfx.plane, 
               screen_sz )
         except( ZeroDivisionError ):
            continue

         walls = []
         wall = None
         while None == wall or \
         (ray.map_x < 23 and ray.map_y < 23 and \
         ray.map_x > 0 and ray.map_y > 0):
            wall = ray.cast( gfx.pos, screen_sz )
            if None == wall:
               continue
            walls.append( wall )

         walls = reversed( walls )
         last_wall_top = 0
         for wall in walls:
            if GridWall.FACE_BACK != wall.face:
               color = pick_wall_color( wall )
               gfx.line( color, x, wall.draw[START], wall.draw[END], \
                  pick_wall_pattern( wall ) )

            if GridWall.FACE_BACK == wall.face:
               last_wall_top = wall.draw[START];
            elif 0 < last_wall_top:
               color = (255, 255, 255)
               gfx.line( color, x, last_wall_top, wall.draw[START], \
                  pick_top_pattern( wall ) )
               last_wall_top = 0

      # Draw the UI.
      gfx.text( '{},{}'.format( int( gfx.pos[X] ), int( gfx.pos[Y] ) ), \
         (255, 255, 255), 0,  0, (0, 0, 0) )

      gfx.flip()

      gfx.wait( 10 )

if '__main__' == __name__:
   import pygame
   mood( pyg=pygame )

