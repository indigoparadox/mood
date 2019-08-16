#!/usr/bin/env python

import math

X = 0
Y = 1

class GridMap( object ):

   WALL_L = 0
   WALL_R = 1

   def __init__( self, grid ):
      self.grid = grid

   def cast( self, x, facing, plane, pos, screen_sz ):
      cam_x = 2.0 * x / float( screen_sz[X] ) - 1
      if 0 == cam_x:
         return 0, 0, 0, (0, 0, 0)
      ray_dir = (float( facing[X] ) + float( plane[X] ) * float( cam_x ),
         float( facing[Y] ) + float( plane[Y] ) * float( cam_x ))
      delta_dist = (math.fabs( 1.0 / ray_dir[X]), math.fabs( 1.0 / ray_dir[Y] ))

      map_pos = (int( pos[X] ), int( pos[Y] ))
      #print map_pos

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

      hit = False
      side = GridMap.WALL_L
      while not hit:
         if side_dist_x < side_dist_y:
            side_dist_x += delta_dist[X]
            map_pos = (int( map_pos[X] + step_x ), map_pos[Y])
            side = GridMap.WALL_L
         else:
            side_dist_y += delta_dist[Y]
            map_pos = (map_pos[X], int( map_pos[Y] + step_y ))
            side = GridMap.WALL_R

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

      if GridMap.WALL_L == side:
         wall_dist = \
            (float( map_pos[X] ) - pos[X] + (1 - step_x) / 2) / ray_dir[X]
      else:
         wall_dist = \
            (float( map_pos[Y] ) - pos[Y] + (1 - step_y) / 2) / ray_dir[Y]

      # calculate lowest and highest pixel to fill in current stripe
      line_height = int(screen_sz[Y] / wall_dist) 
      draw_start = int(-line_height / 2 + screen_sz[Y] / 2)
      if draw_start < 0:
         draw_start = 0
      draw_end = int(line_height / 2 + screen_sz[Y] / 2)
      if draw_end >= screen_sz[Y]:
         draw_end = screen_sz[Y] - 1

      return draw_start, draw_end, side, color

   def tile( self, pos ):
      return self.grid[int(pos[X])][int(pos[Y])]

   def collides( self, pos ):
      if self.tile( pos ) == 0:
         return False
      else:
         return True

