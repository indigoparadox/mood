#!/usr/bin/env python

import time
import random
import math
from gridmap import GridMap, GridRay, GridWall
from microgfx import Gfx, Input
from maps import DefaultMap
from mob import Mob

#from guppy import hpy

SCREEN_H = 64
SCREEN_W = 128
#SCREEN_H = 480
#SCREEN_W = 640

X = 0
Y = 1

sprites = {
   'bottle': [0x6, 0xcb, 0xb5, 0x8b, 0x85, 0xbb, 0xcf, 0x6]
}

class MainLoop( object ):

   def __init__( self, gfx, inp, gmap ):
      self.gfx = gfx
      self.gmap = gmap
      self.running = True
      self.input = inp

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
            try:
               ray = GridRay( x, gfx.pos, gfx.facing, gfx.plane, (SCREEN_W, SCREEN_H) )
               wall = ray.cast( self.gmap, gfx.pos, (SCREEN_W, SCREEN_H), zbuffer )
               color = (255, 255, 255)
               gfx.line( color, x, wall.draw_start, wall.draw_end, \
                  True if GridWall.SIDE_NS == wall.side else False )
            except( ZeroDivisionError ):
               pass

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

gfx = Gfx( (SCREEN_W, SCREEN_H), 4 )
main = MainLoop( gfx, Input(), GridMap( DefaultMap ) )

main.run()

