#!/usr/bin/env python

import time
import random
import math
from gridmap import GridMap, GridRay, GridWall
from microgfx import Gfx, Input
from maps import DefaultMap
from mob import Mob

#from guppy import hpy

ZOOM = 4
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

sprites = {
   'bottle': [0x6, 0xcb, 0xb5, 0x8b, 0x85, 0xbb, 0xcf, 0x6]
}

class MainLoop( object ):

   def __init__( self, gfx, inp, gmap ):
      self.gfx = gfx
      self.gmap = gmap
      self.running = True
      self.input = inp

   def pick_wall_color( self, wall ):
      color = (255, 255, 255)
      if 1 == wall.tile:
         color = (255, 0, 0)
      elif 2 == wall.tile:
         color = (0, 255, 0)
      elif 3 == wall.tile:
         color = (0, 0, 255)
      elif 4 == wall.tile:
         color = (255, 0, 255)
      elif 5 == wall.tile:
         color = (0, 255, 255)
      return color

   def run( self ):
      gfx = self.gfx
      ticks = 0
      mspeed = 0.5
      zbuffer = [0] * SCREEN_W

      mobs = []

      randpos = (random.randint( 10, 18 ), random.randint( 10, 18 ))
      mobs.append( Mob( randpos, sprites['bottle'] ) )

      while( self.running ):

         gfx.blank( (0, 0, 0) )

         prev_ticks = ticks
         ticks = time.clock()
         frame_ticks = (ticks - prev_ticks) / 1000.0
         #rspeed = frame_ticks * 3
         rspeed = 0.5
         last_wall_top = 0

         #print (gfx.plane[X], gfx.plane[Y], gfx.facing[X], gfx.facing[Y])

         # Poll interaction events.
         event = self.input.poll()
         if Input.EVENT_QUIT == event:
            self.running = False
         elif Input.EVENT_RRIGHT == event:
            gfx.rotate( -1 * rspeed )
         elif Input.EVENT_RLEFT == event:
            gfx.rotate( rspeed )
         elif Input.EVENT_FWD == event:
            new_x = gfx.pos[X]
            new_y = gfx.pos[Y]
            if not self.gmap.collides( \
            (int(gfx.pos[X] + gfx.facing[X] * mspeed), int(gfx.pos[Y])) ):
               new_x = gfx.pos[X] + (gfx.facing[X] * mspeed)
            if not self.gmap.collides( \
            (int(gfx.pos[X]), int(gfx.pos[Y] + gfx.facing[Y] * mspeed)) ):
               new_y = gfx.pos[Y] + (gfx.facing[Y] * mspeed)
            gfx.pos = (new_x, new_y)

         # Draw the walls.
         for x in range( 0, SCREEN_W - 1 ):
            ray = None
            try:
               ray = GridRay( x, gfx.pos, gfx.facing, gfx.plane, 
                  (SCREEN_W, SCREEN_H) )
            except( ZeroDivisionError ):
               continue

            walls = []
            wall = None
            while None == wall or \
            (ray.map_x < 23 and ray.map_y < 23 and \
            ray.map_x > 0 and ray.map_y > 0):
               wall = \
                  ray.cast( self.gmap, gfx.pos, (SCREEN_W, SCREEN_H), zbuffer )
               if None == wall:
                  continue
               walls.append( wall )

            walls = reversed( walls )
            for wall in walls:
               if GridWall.FACE_BACK != wall.face:
                  color = self.pick_wall_color( wall )
                  gfx.line( color, x, wall.draw[START], wall.draw[END], \
                     Gfx.PATTERN_FILLED if GridWall.SIDE_NS == wall.side else \
                     Gfx.PATTERN_HASH )

               if GridWall.FACE_BACK == wall.face:
                  last_wall_top = wall.draw[START];
               elif 0 < last_wall_top:
                  color = (255, 255, 255)
                  gfx.line( color, x, last_wall_top, wall.draw[START], \
                     Gfx.PATTERN_STRIPES_HORIZ )

            # Draw the mobs.
            for mob in mobs:
               pass
               #for px_x, px_y, px in mob.cast( x, gfx.pos, gfx.facing, gfx.plane, (SCREEN_W, SCREEN_H), zbuffer ):
               #   if px:
               #      gfx.line( (255, 0, 0), x, px_y, px_y, False )

         # Draw the UI.
         gfx.text( 'foo', (255, 255, 255), 0,  0, (0, 0, 0) )

         gfx.flip()

         gfx.wait( 10 )

gfx = Gfx( (SCREEN_W, SCREEN_H), ZOOM )
main = MainLoop( gfx, Input(), GridMap( DefaultMap ) )

main.run()

