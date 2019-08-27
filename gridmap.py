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

   def cast( self, gmap, x, pos_x, pos_y, facing_x, facing_y, plane_x, plane_y, screen_sz, zbuffer ):
      # calculate ray position and direction

      # x-coordinate in camera space
      cam_x = 2.0 * x / float( screen_sz[Y] ) - 1
      if 0 == cam_x:
         return GridWall()
      ray_dir_x = float( facing_x ) + float( plane_x ) * float( cam_x )
      ray_dir_y = float( facing_y ) + float( plane_y ) * float( cam_x )

      # which box of the map we're in
      map_x = int(pos_x);
      map_y = int(pos_y);

      # length of ray from current position to next x or y-side
      side_dist_x = 0
      side_dist_y = 0

      # length of ray from one x or y-side to next x or y-side
      delta_dist_x = math.fabs(1 / ray_dir_x)
      delta_dist_y = math.fabs(1 / ray_dir_y)

      wall = GridWall()

      # what direction to step in x or y-direction (either +1 or -1)
      step_x = 0
      step_y = 0

      # was there a wall hit?
      hit = False

      # Move the ray forward by one step.
      if ray_dir_x < 0:
         step_x = -1
         side_dist_x = (float( pos_x ) - map_x) * delta_dist_x
      else:
         step_x = 1
         side_dist_x = (float( map_x ) + 1.0 - pos_x) * delta_dist_x

      if ray_dir_y < 0:
         step_y = -1
         side_dist_y = (float( pos_y ) - map_y) * delta_dist_y
      else:
         step_y = 1
         side_dist_y = (float( map_y ) + 1.0 - pos_y) * delta_dist_y

      # perform DDA
      while not hit:
         # jump to next map square, OR in x-direction, OR in y-direction
         if side_dist_x < side_dist_y:
            side_dist_x += delta_dist_x
            map_x += step_x
            wall.side = GridWall.SIDE_NS
         else:
            side_dist_y += delta_dist_y
            map_y += step_y
            wall.side = GridWall.SIDE_EW

         # Check if ray has hit a wall
         if gmap.grid[map_x][map_y] > 0:
            hit = True;

      # Calculate distance projected on camera direction (Euclidean distance will give fisheye effect!)
      if wall.side == GridWall.SIDE_NS:
         wall.dist = (map_x - pos_x + (1 - step_x) / 2) / ray_dir_x
      else:
         wall.dist = (map_y - pos_y + (1 - step_y) / 2) / ray_dir_y
      zbuffer[x] = wall.dist

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

