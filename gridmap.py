#!/usr/bin/env python

import math

X = 0
Y = 1

class GridMap( object ):

   WALL_L = 0
   WALL_R = 1

   def __init__( self, grid ):
      self.grid = grid

   def cast( self, x, pos_x, pos_y, facing_x, facing_y, plane_x, plane_y, screen_sz ):
      # calculate ray position and direction

      # x-coordinate in camera space
      cam_x = 2.0 * x / float( screen_sz[Y] ) - 1
      if 0 == cam_x:
         return 0, 0, 0
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

      wall_dist = 0

      # what direction to step in x or y-direction (either +1 or -1)
      step_x = 0
      step_y = 0

      # was there a wall hit?
      hit = False
      # was a NS or a EW wall hit?
      side = GridMap.WALL_L

      # calculate step and initial sideDist
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
            side = GridMap.WALL_L
         else:
            side_dist_y += delta_dist_y
            map_y += step_y
            side = GridMap.WALL_R

         # Check if ray has hit a wall
         if self.grid[map_x][map_y] > 0:
            hit = True;

      # Calculate distance projected on camera direction (Euclidean distance will give fisheye effect!)
      if side == 0:
         wall_dist = (map_x - pos_x + (1 - step_x) / 2) / ray_dir_x
      else:
         wall_dist = (map_y - pos_y + (1 - step_y) / 2) / ray_dir_y

      # Calculate height of line to draw on screen
      line_height = int(screen_sz[Y] / wall_dist)

      # calculate lowest and highest pixel to fill in current stripe
      draw_start = int(-line_height / 2 + screen_sz[Y] / 2)
      if draw_start < 0:
         draw_start = 0
      draw_end = int(line_height / 2 + screen_sz[Y] / 2)
      if draw_end >= screen_sz[Y]:
         draw_end = screen_sz[Y] - 1

      return draw_start, draw_end, side


   def tile( self, pos ):
      return self.grid[int(pos[X])][int(pos[Y])]

   def collides( self, pos ):
      if self.tile( pos ) == 0:
         return False
      else:
         return True

