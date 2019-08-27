#!/usr/bin/env python

import math

X = 0
Y = 1

class GridWall( object ):

   SIDE_NS = 0
   SIDE_EW = 1

   def __init__( self ):
      self.wall_dist = 0
      self.side = GridWall.SIDE_NS
      self.draw_start = 0
      self.draw_end = 0

class GridRay( object ):

   def __init__( self, x, pos, facing, plane, screen_sz ):
      # x-coordinate in camera space
      cam_x = 2.0 * x / float( screen_sz[Y] ) - 1
      self.dir = (float( facing[X] ) + float( plane[X] ) * float( cam_x ),
         float( facing[Y] ) + float( plane[Y] ) * float( cam_x ))

      # which box of the map we're in
      self.map_x = int( pos[X] )
      self.map_y = int( pos[Y] )

      # length of ray from one x or y-side to next x or y-side
      self.delta_dist = (math.fabs(1 / self.dir[X]), math.fabs(1 / self.dir[Y]))

      # Figure out the step (direction of the ray) and side_dist (length of ray
      # from current position to next X or Y side.
      if self.dir[X] < 0:
         step_x = -1
         self.side_dist_x =
            (float( pos[X] ) - self.map_x) * self.delta_dist[X]
      else:
         step_x = 1
         self.side_dist_x =
            (float( self.map_x ) + 1.0 - pos[X]) * self.delta_dist[X]

      if self.dir[Y] < 0:
         step_y = -1
         self.side_dist_y =
            (float( pos[Y] ) - self.map_y) * self.delta_dist[Y]
      else:
         step_y = 1
         self.side_dist_y =
            (float( self.map_y ) + 1.0 - pos[Y]) * self.delta_dist[Y]

      self.step = (step_x, step_y)

   def cast( self, gmap, pos, screen_sz, zbuffer ):
      # calculate ray position and direction

      wall = GridWall()

      # was there a wall hit?
      hit = False

      # perform DDA
      while not hit:
         # jump to next map square, OR in x-direction, OR in y-direction
         if self.side_dist_x < self.side_dist_y:
            self.side_dist_x += self.delta_dist[X]
            self.map_x += self.step[X]
            wall.side = GridWall.SIDE_NS
         else:
            self.side_dist_y += self.delta_dist[Y]
            self.map_y += self.step[Y]
            wall.side = GridWall.SIDE_EW

         # Check if ray has hit a wall
         if gmap.grid[self.map_x][self.map_y] > 0:
            hit = True;

      # Calculate distance projected on camera direction (Euclidean distance will give fisheye effect!)
      if wall.side == GridWall.SIDE_NS:
         wall.dist = (self.map_x - pos[X] + (1 - self.step[X]) / 2) / self.dir[X]
      else:
         wall.dist = (self.map_y - pos[Y] + (1 - self.step[Y]) / 2) / self.dir[Y]
      #zbuffer[x] = wall.dist

      # Calculate height of line to draw on screen
      line_height = int(screen_sz[Y] / wall.dist)

      # calculate lowest and highest pixel to fill in current stripe
      wall.draw_start = int(-line_height / 2 + screen_sz[Y] / 2)
      if wall.draw_start < 0:
         wall.draw_start = 0
      wall.draw_end = int(line_height / 2 + screen_sz[Y] / 2)
      if wall.draw_end >= screen_sz[Y]:
         wall.draw_end = screen_sz[Y] - 1

      return wall

class GridMap( object ):

   def __init__( self, grid ):
      self.grid = grid

   def tile( self, pos ):
      return self.grid[int(pos[X])][int(pos[Y])]

   def collides( self, pos ):
      if self.tile( pos ) == 0:
         return False
      else:
         return True

