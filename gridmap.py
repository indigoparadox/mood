#!/usr/bin/env python

import math

X = 0
Y = 1

START = 0
END = 1

class GridWall( object ):

   SIDE_NS = 0
   SIDE_EW = 1

   def __init__( self, side ):
      self.wall_dist = 0
      self.side = side
      self.draw = (0, 0)

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
         self.side_dist_x = \
            (float( pos[X] ) - self.map_x) * self.delta_dist[X]
      else:
         step_x = 1
         self.side_dist_x = \
            (float( self.map_x ) + 1.0 - pos[X]) * self.delta_dist[X]

      if self.dir[Y] < 0:
         step_y = -1
         self.side_dist_y = \
            (float( pos[Y] ) - self.map_y) * self.delta_dist[Y]
      else:
         step_y = 1
         self.side_dist_y = \
            (float( self.map_y ) + 1.0 - pos[Y]) * self.delta_dist[Y]

      self.step = (step_x, step_y)

   def cast( self, gmap, pos, screen_sz, zbuffer ):

      # Move the ray one step forward.
      side = GridWall.SIDE_NS
      if self.side_dist_x < self.side_dist_y:
         self.side_dist_x += self.delta_dist[X]
         self.map_x += self.step[X]
      else:
         self.side_dist_y += self.delta_dist[Y]
         self.map_y += self.step[Y]
         side = GridWall.SIDE_EW

      # Check if ray has hit a wall.
      if gmap.grid[self.map_x][self.map_y] <= 0:
         # Nope!
         return None

      wall = GridWall( side )

      # Calculate distance projected on camera direction
      # (Euclidean distance will give fisheye effect!)
      if wall.side == GridWall.SIDE_NS:
         wall.dist = \
            (self.map_x - pos[X] + (1 - self.step[X]) / 2) / self.dir[X]
      else:
         wall.dist = \
            (self.map_y - pos[Y] + (1 - self.step[Y]) / 2) / self.dir[Y]
      #zbuffer[x] = wall.dist

      # Determine the on-screen drawing scanline start and stop.
      x_line_height = int(screen_sz[Y] / wall.dist)
      x_line_half = x_line_height / 2;

      # Figure out the wall bottom.
      draw_end = int( x_line_half + (screen_sz[Y] / 2) )

      # Figure out the wall top.
      draw_start = int( draw_end - 2 * x_line_half * \
         1 / gmap.grid[self.map_x][self.map_y] )

      # calculate lowest and highest pixel to fill in current stripe
      if draw_start < 0:
         draw_start = 0
      if draw_end >= screen_sz[Y]:
         draw_end = screen_sz[Y] - 1

      wall.draw = (draw_start, draw_end)

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

