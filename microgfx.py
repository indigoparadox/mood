#!/usr/bin/env python

ENGINE_SSD1306 = 1
ENGINE_PYGAME = 2

X = 0
Y = 1

engine = None

import math
try:
   import ssd1306
   engine = ENGINE_SSD1306
except:
   import pygame
   engine = ENGINE_PYGAME

class Input( object ):

   EVENT_NONE = 0
   EVENT_QUIT = 1
   EVENT_RLEFT = 2
   EVENT_RRIGHT = 3
   EVENT_FWD = 4

   def __init__( self ):
      pass

   def poll( self ):
      if ENGINE_PYGAME == engine:
         for event in pygame.event.get():
            if pygame.QUIT == event.type:
               return Input.EVENT_QUIT
            elif pygame.KEYDOWN == event.type:
               if pygame.K_ESCAPE == event.key:
                  return Input.EVENT_QUIT
               elif pygame.K_RIGHT == event.key:
                  return Input.EVENT_RRIGHT
               elif pygame.K_LEFT == event.key:
                  return Input.EVENT_RLEFT
               elif pygame.K_UP == event.key:
                  return Input.EVENT_FWD

class Gfx( object ):

   PATTERN_FILLED = 0
   PATTERN_DOTS = 1
   PATTERN_STRIPES = 2

   def __init__( self, screen_sz ):

      self.pos = (float( 6 ), float( 3 ))
      self.facing = (float( -1 ), float( 0 ))
      self.plane = (float( 0 ), float( 0.66 ))

      if ENGINE_PYGAME == engine:
         pygame.init()
         self.screen = pygame.display.set_mode( screen_sz )
         self.clock = pygame.time.Clock()

   def wait( self, fps ):
      if ENGINE_PYGAME == engine:
         self.clock.tick( fps )

   def blank( self, color ):
      if ENGINE_PYGAME == engine:
         pygame.draw.rect( self.screen, color, [0, 0,
            self.screen.get_width(), self.screen.get_height()] )

   def line( self, color, pos1, pos2, pattern ):

      if ENGINE_PYGAME == engine:
         if Gfx.PATTERN_STRIPES == pattern:
            for y_dot in range( pos1[Y], pos2[Y] ):
               if 0 < y_dot % 2:
                  continue
               pygame.draw.line( self.screen, color, \
                  (pos1[X], y_dot), (pos2[X], y_dot) )

         elif Gfx.PATTERN_DOTS == pattern:
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
      if ENGINE_PYGAME == engine:
         pygame.display.flip()

