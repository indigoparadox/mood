#!/usr/bin/env python

import time
import math

ENGINE_SSD1306 = 1
ENGINE_PYGAME = 2

#SCREEN_H = 64
#SCREEN_W = 128
SCREEN_H = 480
SCREEN_W = 640

X = 0
Y = 1

EVENT_NONE = 0
EVENT_QUIT = 1
EVENT_RLEFT = 2
EVENT_RRIGHT = 3
EVENT_FWD = 4

WALL_L = 0
WALL_R = 1

PATTERN_FILLED = 0
PATTERN_DOTS = 1
PATTERN_STRIPES = 2

engine = None
try:
   import ssd1306
   engine = ENGINE_SSD1306
except:
   import pygame
   engine = ENGINE_PYGAME

class GridMap( object ):
   def __init__( self, grid ):
      self.grid = grid

   def cast( self, x, facing, plane, pos ):
      cam_x = 2.0 * x / float( SCREEN_W ) - 1
      if 0 == cam_x:
         return (0, 0, (0, 0, 0))
      ray_dir = (float( facing[X] ) + float( plane[X] ) * float( cam_x ),
         float( facing[Y] ) + float( plane[Y] ) * float( cam_x ))
      delta_dist = (math.fabs( 1.0 / ray_dir[X]), math.fabs( 1.0 / ray_dir[Y] ))

      map_pos = (int( pos[X] ), int( pos[Y] ))
      print map_pos

      step_x = 1
      side_dist_x = (float( map_pos[X] ) + 1.0 - pos[X]) * delta_dist[X]
      if 0 > ray_dir[X]:
         step_x = -1
         side_dist_x = (float( pos[X] ) - map_pos[X]) * delta_dist[X]

      step_y = 1
      side_dist_y = (float( map_pos[Y] ) + 1.0 - pos[Y]) * delta_dist[Y]
      if 0 > ray_dir[Y]:
         step_x = -1
         side_dist_x = (float( pos[Y] ) - map_pos[Y]) * delta_dist[Y]

      assert( step_x == -1 or step_x == 1 )
      assert( step_y == -1 or step_y == 1 )

      hit = False
      side = WALL_L
      while not hit:
         if side_dist_x < side_dist_y:
            side_dist_x += delta_dist[X]
            map_pos = (int( map_pos[X] + step_x ), map_pos[Y])
            side = WALL_L
         else:
            side_dist_y += delta_dist[Y]
            map_pos = (map_pos[X], int( map_pos[Y] + step_y ))
            side = WALL_R

         #if 0 > map_pos[X] or 0 > map_pos[Y] or \
         #len( self.grid ) <= map_pos[Y] or len( self.grid[0] ) <= map_pos[X]:
         #   # Ray went off the map.
         #   return (10, side)

         if 0 < self.grid[map_pos[X]][map_pos[Y]]:
            # Ray hit a wall.
            hit = True

      intensity = 255
      if self.grid[map_pos[X]][map_pos[Y]] == 1:
         color = (intensity, 0, 0)
      elif self.grid[map_pos[X]][map_pos[Y]] == 2:
         color = (0, intensity, 0)
      elif self.grid[map_pos[X]][map_pos[Y]] == 3:
         color = (0, 0, intensity)
      elif self.grid[map_pos[X]][map_pos[Y]] == 4:
         color = (intensity, intensity, intensity)
      else:
         color = (0, intensity, intensity)

      if WALL_L == side:
         wall_dist = \
            (float( map_pos[X] ) - pos[X] + (1 - step_x) / 2) / ray_dir[X]
      else:
         wall_dist = \
            (float( map_pos[Y] ) - pos[Y] + (1 - step_y) / 2) / ray_dir[Y]

      return (int(SCREEN_H / wall_dist), side, color)

   def tile( self, pos ):
      return self.grid[int(pos[X])][int(pos[Y])]

   def collides( self, pos ):
      if self.tile( pos ) == 0:
         return False
      else:
         return True

class Input( object ):

   def __init__( self, engine ):
      self.engine = engine

   def poll( self ):
      if ENGINE_PYGAME == self.engine:
         for event in pygame.event.get():
            if pygame.QUIT == event.type:
               return EVENT_QUIT
            elif pygame.KEYDOWN == event.type:
               if pygame.K_ESCAPE == event.key:
                  return EVENT_QUIT
               elif pygame.K_RIGHT == event.key:
                  return EVENT_RRIGHT
               elif pygame.K_LEFT == event.key:
                  return EVENT_RLEFT
               elif pygame.K_UP == event.key:
                  return EVENT_FWD

class Gfx( object ):

   def __init__( self, engine ):

      self.engine = engine

      self.pos = (float( 6 ), float( 3 ))
      self.facing = (float( -1 ), float( 0 ))
      self.plane = (float( 0 ), float( 0.66 ))

      if ENGINE_PYGAME == self.engine:
         pygame.init()
         self.screen = pygame.display.set_mode( (SCREEN_W, SCREEN_H) )
         self.clock = pygame.time.Clock()

   def wait( self, fps ):
      if ENGINE_PYGAME == self.engine:
         self.clock.tick( fps )

   def blank( self, color ):
      if ENGINE_PYGAME == self.engine:
         pygame.draw.rect( self.screen, color, [0, 0, SCREEN_W, SCREEN_H] )

   def line( self, color, pos1, pos2, pattern ):

      if ENGINE_PYGAME == self.engine:
         if PATTERN_STRIPES == pattern:
            for y_dot in range( pos1[Y], pos2[Y] ):
               if 0 < y_dot % 2:
                  continue
               pygame.draw.line( self.screen, color, \
                  (pos1[X], y_dot), (pos2[X], y_dot) )

         elif PATTERN_DOTS == pattern:
            for y_dot in range( pos1[Y], pos2[Y] ):
               if 0 < y_dot % 2 and 0 < pos1[X] % 2 \
               or 0 == y_dot % 2 and 0 == pos1[X] % 2:
                  continue
               pygame.draw.line( self.screen, color, \
                  (pos1[X], y_dot), (pos2[X], y_dot) )

         else:
            pygame.draw.line( self.screen, color, pos1, pos2 )

   def rotate( self, speed ):

      # Speed -1 for right, +1 for left.

      # Rotate the camera.
      new_facing = \
         (self.facing[X] * math.cos( speed ) - \
            self.facing[Y] * math.sin( speed ), \
         self.facing[X] * math.sin( speed ) + \
            self.facing[Y] * math.cos( speed ))

      # Rotate the map.
      new_plane = \
         (self.plane[X] * math.cos( speed ) - \
            self.plane[Y] * math.sin( speed ),
         self.plane[X] * math.sin( speed ) + \
            self.plane[Y] * math.cos( speed ))

      self.facing = new_facing
      self.plane = new_plane

   def flip( self ):
      if ENGINE_PYGAME == self.engine:
         pygame.display.flip()

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
         if EVENT_QUIT == event:
            self.running = False
         elif EVENT_RRIGHT == event:
            gfx.rotate( -1 * rspeed )
         elif EVENT_RLEFT == event:
            gfx.rotate( rspeed )
         elif EVENT_FWD == event:
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
            cast = self.gmap.cast( x, gfx.facing, gfx.plane, gfx.pos )
            height = cast[0]
            side = cast[1]
            color = cast[2]
            y_s = -height / 2 + midline
            if 0 > y_s:
               y_s = 0
            y_e = height / 2 + midline
            if SCREEN_H <= y_e:
               y_e = SCREEN_H - 1

            l_s = (x, y_s)
            l_e = (x, y_e)

            gfx.line( color, l_s, l_e, \
               True if WALL_L == side else False )

         gfx.flip()

         gfx.wait( 10 )

main = MainLoop( Gfx( engine ), Input( engine ), GridMap( [
  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,2,2,2,2,2,0,0,0,0,3,0,3,0,3,0,0,0,1],
  [1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,3,0,0,0,3,0,0,0,1],
  [1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,2,2,0,2,2,0,0,0,0,3,0,3,0,3,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,0,4,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,0,0,0,0,5,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,0,4,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,0,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
] ) )

main.run()

