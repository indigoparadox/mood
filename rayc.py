#!/usr/bin/env python

import pygame
import math

worldMap = [
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
]

SCREEN_WIDTH = 512
SCREEN_HEIGHT = 384

from gridmap import GridMap

def main():
   # x and y start position
   posX = float( 22 )
   posY = float( 12 )

   # initial direction vector
   dirX = float( -1 )
   dirY = float( 0 )

   # the 2d raycaster version of camera plane
   planeX = 0.0
   planeY = 0.66

   # time of current frame
   time = 0
   # time of previous frame
   oldTime = 0

   pygame.init()
   screen = pygame.display.set_mode( (SCREEN_WIDTH, SCREEN_HEIGHT) )

   running = True
   while running:

      pygame.draw.rect( screen, (0, 0, 0), [0, 0, SCREEN_WIDTH, SCREEN_HEIGHT] )

      #print (planeX, planeY, dirX, dirY)

      for x in range( 0, SCREEN_WIDTH - 1 ):
         # calculate ray position and direction

         # x-coordinate in camera space
         cameraX = 2.0 * x / float( SCREEN_WIDTH ) - 1
         if 0 == cameraX:
            continue
         rayDirX = float( dirX ) + float( planeX ) * float( cameraX )
         rayDirY = float( dirY ) + float( planeY ) * float( cameraX )

         # which box of the map we're in
         mapX = int(posX);
         mapY = int(posY);

         # length of ray from current position to next x or y-side
         sideDistX = 0
         sideDistY = 0

         # length of ray from one x or y-side to next x or y-side
         deltaDistX = math.fabs(1 / rayDirX)
         deltaDistY = math.fabs(1 / rayDirY)

         perpWallDist = 0

         # what direction to step in x or y-direction (either +1 or -1)
         stepX = 0
         stepY = 0

         # was there a wall hit?
         hit = 0
         # was a NS or a EW wall hit?
         side = 0

         # calculate step and initial sideDist
         if rayDirX < 0:
            stepX = -1
            sideDistX = (float( posX ) - mapX) * deltaDistX
         else:
            stepX = 1
            sideDistX = (float( mapX ) + 1.0 - posX) * deltaDistX

         if rayDirY < 0:
            stepY = -1
            sideDistY = (float( posY ) - mapY) * deltaDistY
         else:
            stepY = 1
            sideDistY = (float( mapY ) + 1.0 - posY) * deltaDistY

         # perform DDA
         while hit == 0:
            # jump to next map square, OR in x-direction, OR in y-direction
            if sideDistX < sideDistY:
               sideDistX += deltaDistX
               mapX += stepX
               side = 0
            else:
               sideDistY += deltaDistY
               mapY += stepY
               side = 1

            # Check if ray has hit a wall
            if worldMap[mapX][mapY] > 0:
               hit = 1;

         # Calculate distance projected on camera direction (Euclidean distance will give fisheye effect!)
         if side == 0:
            perpWallDist = (mapX - posX + (1 - stepX) / 2) / rayDirX
         else:
            perpWallDist = (mapY - posY + (1 - stepY) / 2) / rayDirY

         # Calculate height of line to draw on screen
         lineHeight = int(SCREEN_HEIGHT / perpWallDist)

         # calculate lowest and highest pixel to fill in current stripe
         drawStart = int(-lineHeight / 2 + SCREEN_HEIGHT / 2)
         if drawStart < 0:
            drawStart = 0
         drawEnd = int(lineHeight / 2 + SCREEN_HEIGHT / 2)
         if drawEnd >= SCREEN_HEIGHT:
            drawEnd = SCREEN_HEIGHT - 1

         # give x and y sides different brightness
         intensity = 255
         if side == 1:
            intensity /= 2

         # choose wall color
         color = (0, 0, 0)
         if worldMap[mapX][mapY] == 1:
            color = (intensity, 0, 0)
         elif worldMap[mapX][mapY] == 2:
            color = (0, intensity, 0)
         elif worldMap[mapX][mapY] == 3:
            color = (0, 0, intensity)
         elif worldMap[mapX][mapY] == 4:
            color = (intensity, intensity, intensity)
         else:
            color = (0, intensity, intensity)

         # draw the pixels of the stripe as a vertical line
         pygame.draw.line( screen, color, (x, drawStart), (x, drawEnd) )

      # timing for input and FPS counter
      oldTime = time
      time = pygame.time.get_ticks()

      # frameTime is the time this frame has taken, in seconds
      frameTime = (float( time ) - float( oldTime )) / 1000.0

      
      # FPS counter
      pygame.display.flip()

      # speed modifiers
      # the constant value is in squares/second
      #moveSpeed = float( frameTime ) * 5.0
      moveSpeed = 1
      # the constant value is in radians/second
      #rotSpeed = float( frameTime ) * 3.0
      rotSpeed = 1

      for event in pygame.event.get():
         if pygame.QUIT == event.type:
            running = False
         elif pygame.KEYDOWN == event.type:
            if pygame.K_ESCAPE == event.key:
               running = False

            if pygame.K_UP == event.key:
               if worldMap[int(posX + dirX * moveSpeed)][int(posY)] == 0:
                  posX += dirX * moveSpeed
               if worldMap[int(posX)][int(posY + dirY * moveSpeed)] == 0:
                  posY += dirY * moveSpeed

            # move backwards if no wall behind you
            if pygame.K_DOWN == event.key:
               if worldMap[int(posX - dirX * moveSpeed)][int(posY)] == 0:
                  posX -= dirX * moveSpeed
               if worldMap[int(posX)][int(posY - dirY * moveSpeed)] == 0:
                  posY -= dirY * moveSpeed

            # rotate to the right
            if pygame.K_RIGHT == event.key:
               # both camera direction and camera plane must be rotated
               oldDirX = dirX
               dirX = dirX * math.cos(-rotSpeed) - dirY * math.sin(-rotSpeed)
               dirY = oldDirX * math.sin(-rotSpeed) + dirY * math.cos(-rotSpeed)
               
               oldPlaneX = planeX;
               planeX = planeX * math.cos(-rotSpeed) - planeY * math.sin(-rotSpeed)
               planeY = oldPlaneX * math.sin(-rotSpeed) + planeY * math.cos(-rotSpeed)

            # rotate to the left
            if pygame.K_LEFT == event.key:
               # both camera direction and camera plane must be rotated
               oldDirX = dirX
               dirX = dirX * math.cos(rotSpeed) - dirY * math.sin(rotSpeed)
               dirY = oldDirX * math.sin(rotSpeed) + dirY * math.cos(rotSpeed)

               oldPlaneX = planeX
               planeX = planeX * math.cos(rotSpeed) - planeY * math.sin(rotSpeed)
               planeY = oldPlaneX * math.sin(rotSpeed) + planeY * math.cos(rotSpeed)

if '__main__' == __name__:
   main()

