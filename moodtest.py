#!/usr/bin/env python

import unittest
from gridmap import GridMap
import maps

from rayc import cast

X = 0
Y = 1

class TestGridMap( unittest.TestCase ):

   def setUp( self ):
      self.gmap = GridMap( maps.DefaultMap )

   def test_cast( self ):

      pos = (float( 6 ), float( 3 ))
      facing = (float( -1 ), float( 0 ))
      plane = (float( 0 ), float( 0.66 ))
      screen_sz = (640, 480)

      ds1l = []
      de1l = []
      ds2l = []
      de2l = []

      for x in range( 0, 479 ):
         ds1, de1, side1, color1 = \
            self.gmap.cast( x, facing, plane, pos, screen_sz )
         ds2, de2, color2 = cast( x, pos[X], pos[Y], facing[X], facing[Y], \
            plane[X], plane[Y] )
         ds1l.append( ds1 )
         ds2l.append( ds2 )
         de1l.append( de1 )
         de2l.append( de2 )

      self.assertSequenceEqual( ds1l, ds2l )
      self.assertSequenceEqual( de1l, de2l )

if '__main__' == __name__:
   unittest.main()

