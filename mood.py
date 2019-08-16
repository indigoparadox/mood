#!/usr/bin/env python

import time
from gridmap import GridMap
from microgfx import Gfx, Input
from maps import DefaultMap

#SCREEN_H = 64
#SCREEN_W = 128
SCREEN_H = 480
SCREEN_W = 640

X = 0
Y = 1

class MainLoop( object ):

   def __init__( self, gfx, inp, gmap ):
      self.gfx = gfx
      self.gmap = gmap
      self.running = True
      self.input = inp

   def run( self ):
      midline = SCREEN_H / 2
      gfx = self.gfx
      ticks = 0
      mspeed = 0.5

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
            l_s, l_e, side, color = self.gmap.cast( \
               x, gfx.facing, gfx.plane, gfx.pos, (SCREEN_W, SCREEN_H) )

            gfx.line( color, l_s, l_e, \
               True if GridMap.WALL_L == side else False )

         gfx.flip()

         gfx.wait( 10 )

gfx = Gfx( (SCREEN_W, SCREEN_H) )
main = MainLoop( gfx, Input(), GridMap( DefaultMap ) )

main.run()

