
QUIT = 1
KEYDOWN = 2

K_ESCAPE = 1
K_RIGHT = 2
K_LEFT = 3
K_UP = 4

def init():
   pass

class display( object ):
   @staticmethod
   def set_mode( mode ):
      return display( mode )

   def __init__( self, size ):
      self.size = size

   def get_width( self ):
      return self.size[0]

   def get_height( self ):
      return self.size[1]

   @staticmethod
   def flip():
      print( "Flip!" )

class time( object ):
   @staticmethod
   def Clock():
      return time()

   def tick( self, x ):
      pass

class draw( object ):
   @staticmethod
   def rect( surface, color, rect ):
      pass

class event( object ):
   @staticmethod
   def get():
      yield event()

   def __init__( self ):
      self.type = 0

class key( object ):

   @staticmethod
   def get_pressed():
      return range( 0, 100 )
   
