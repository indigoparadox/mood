#!/usr/bin/env python

import math

X = 0
Y = 1

START = 0
END = 1

class GridCam( object ):

   def __init__( self, gmap ):

      self.pos = (float( 6 ), float( 3 ))
      self.facing = (float( -1 ), float( 0 ))
      self.plane = (float( 0 ), float( 0.66 ))

      self.gmap = gmap

   def forward( self, mspeed ):
      new_x = self.pos[X]
      new_y = self.pos[Y]
      if not self.gmap.collides( \
      (int(self.pos[X] + self.facing[X] * (mspeed * 2)), int(self.pos[Y])) ):
         new_x = self.pos[X] + (self.facing[X] * mspeed)
      if not self.gmap.collides( \
      (int(self.pos[X]), int(self.pos[Y] + self.facing[Y] * mspeed)) ):
         new_y = self.pos[Y] + (self.facing[Y] * (mspeed * 2))
      self.pos = (new_x, new_y)

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

class GridWall( object ):

   SIDE_NS = 0
   SIDE_EW = 1

   FACE_FRONT = 0
   FACE_BACK = 1

   def __init__( self, gmap, tile_id, side ):
      self.wall_dist = 0
      self.side = side
      self.draw = (0, 0)
      self.face = GridWall.FACE_FRONT
      self.height = 0
      self.gmap = gmap
      self.tile_id = tile_id

   def get_tile( self ):
      return self.gmap.tiles[self.tile_id]

class GridRay( object ):

   def __init__( self, gmap, x, pos, facing, plane, screen_sz ):
      # x-coordinate in camera space
      cam_x = 2.0 * x / float( screen_sz[Y] ) - 1
      self.dir = (float( facing[X] ) + float( plane[X] ) * float( cam_x ),
         float( facing[Y] ) + float( plane[Y] ) * float( cam_x ))

      self.gmap = gmap
      self.last_tile = gmap.tiles[0]
      self._last_wall_height = 0

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

   def cast( self, pos, screen_sz ):

      # Move the ray one step forward.
      side = GridWall.SIDE_NS
      if self.side_dist_x < self.side_dist_y:
         self.side_dist_x += self.delta_dist[X]
         self.map_x += self.step[X]
      else:
         self.side_dist_y += self.delta_dist[Y]
         self.map_y += self.step[Y]
         side = GridWall.SIDE_EW

      tile = self.gmap.tile_at( self.map_x, self.map_y )

      # Check if ray has hit a wall.
      try:
         if tile['id'] == self.last_tile['id']:
            # Nope!
            return None
      except TypeError:
         return None

      wall = GridWall( self.gmap, tile['id'], side )

      if not self.last_tile['pass'] and 0 == tile['id']:
         # This must be a back wall, since we're going to 0.
         wall.face = GridWall.FACE_BACK
         wall.height = self._last_wall_height
      else:
         wall.height = tile['height']
         self._last_wall_height = wall.height

      self.last_tile = tile

      # Calculate distance projected on camera direction
      # (Euclidean distance will give fisheye effect!)
      if wall.side == GridWall.SIDE_NS:
         wall.dist = \
            (float( self.map_x ) - pos[X] + (1.0 - self.step[X]) / 2.0) / \
            self.dir[X]
      else:
         wall.dist = \
            (float( self.map_y ) - pos[Y] + (1.0 - self.step[Y]) / 2.0) / \
            self.dir[Y]

      # Determine the on-screen drawing scanline start and stop.
      x_line_height = int( float( screen_sz[Y] ) / wall.dist )
      x_line_half = x_line_height / 2.0;

      # Figure out the wall bottom.
      draw_end = x_line_height + (screen_sz[Y] / 2.0)

      # Figure out the wall top.
      draw_start = float( draw_end ) - 2.0 * x_line_half * wall.height

      # calculate lowest and highest pixel to fill in current stripe
      if draw_start < 0:
         draw_start = 0
      if draw_end >= screen_sz[Y]:
         draw_end = screen_sz[Y] - 1

      wall.draw = (int( draw_start ), int( draw_end ))

      return wall

class GridMap( object ):

   def __init__( self, grid, tiles ):
      self.grid = grid
      self.tiles = tiles

   def tile_at( self, x, y ):
      out = self.tiles[0]
      try:
         out = self.tiles[self.grid[x][y]]
      except IndexError:
         pass
      return out

   def collides( self, pos ):
      if self.tile_at( pos[X], pos[Y] )['pass']:
         return False
      else:
         return True

