#!/usr/bin/env python

import math
from gridmap import GridMap, GridRay, GridWall, GridCam
from microgfx import Gfx
from maps import DefaultMap, DefaultMapTiles
from mob import Mob

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

WHITE = (255, 255, 255)

HALF_COLORS = {
   (  0, 0, 0): (0, 0, 0),
   (255, 0, 0): (128, 0, 0),
   (0, 255, 0): (0, 128, 0),
   (0, 0, 255): (0, 0, 128),
   (255, 0, 255): (128, 0, 128),
   (0, 255, 255): (0, 128, 128),
   (255,255,255): (128,128,128)
}

def pick_wall_pattern( wall, use_patterns ):
   if use_patterns:
      return Gfx.PATTERN_STRIPES_DIAG_1 if GridWall.SIDE_NS == wall.side else \
      Gfx.PATTERN_HASH
   return Gfx.PATTERN_FILLED

def pick_top_pattern( wall, use_patterns ):
   if use_patterns:
      return Gfx.PATTERN_STRIPES_HORIZ
   return Gfx.PATTERN_FILLED

def pick_wall_color( wall ):
   if GridWall.SIDE_EW == wall.side:
      return HALF_COLORS[wall.get_tile()['color']]
   return wall.get_tile()['color']

def mood( pyg, screen_sz, zoom, use_color, use_patterns ):
   gfx = Gfx( pyg, screen_sz, zoom )
   gmap = GridMap( DefaultMap, DefaultMapTiles )
   cam = GridCam( gmap )
   tiles = DefaultMapTiles
   mspeed = 0.5
   running = True

   while( running ):

      gfx.blank( (0, 0, 0) )
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
         cam.rotate( -1 * rspeed )
      if keys[pygame.K_LEFT]:
         cam.rotate( rspeed )
      if keys[pygame.K_UP]:
         cam.forward( mspeed )

      # Draw the walls.
      for x in range( 0, screen_sz[X] - 1 ):
         ray = None
         try:
            ray = GridRay( gmap, x, cam.pos, cam.facing, cam.plane, 
               screen_sz )
         except( ZeroDivisionError ):
            continue

         walls = []
         wall = None
         while None == wall or \
         (ray.map_x < 23 and ray.map_y < 23 and \
         ray.map_x > 0 and ray.map_y > 0):
            wall = ray.cast( cam.pos, screen_sz )
            if None == wall:
               continue
            walls.append( wall )

         walls = reversed( walls )
         last_wall_top = 0
         for wall in walls:
            if GridWall.FACE_BACK != wall.face:
               if use_color:
                  color = pick_wall_color( wall )
               else:
                  color = WHITE
               gfx.line( color, x, wall.draw[START], wall.draw[END], \
                  pick_wall_pattern( wall, use_patterns ) )

            if GridWall.FACE_BACK == wall.face:
               last_wall_top = wall.draw[START];
            elif 0 < last_wall_top:
               if use_color:
                  color = WHITE
               gfx.line( color, x, last_wall_top, wall.draw[START], \
                  pick_top_pattern( wall, use_patterns ) )
               last_wall_top = 0

      # Draw the UI.
      gfx.text( '{},{}'.format( int( cam.pos[X] ), int( cam.pos[Y] ) ), \
         WHITE, 0,  0, (0, 0, 0) )

      gfx.flip()

      gfx.wait( 10 )

if '__main__' == __name__:

   screen_sz=(SCREEN_W, SCREEN_H)
   zoom=ZOOM
   use_color=False

   try:
      import pygame

      import argparse

      parser = argparse.ArgumentParser()

      parser.add_argument( '-z', '--zoom', type=int )
      parser.add_argument( '-r', '--res', nargs="+", type=int )
      parser.add_argument( '-c', '--color', action='store_true' )
      parser.add_argument( '-p', '--patterns', action='store_true' )

      args = parser.parse_args()

      if None != args.zoom:
         zoom = args.zoom
      use_color = args.color
      use_patterns = args.patterns
      if None != args.res:
         screen_sz = tuple( args.res )
      
   except ImportError:
      import upygame as pygame
   mood( pygame, screen_sz, zoom, use_color, use_patterns )

