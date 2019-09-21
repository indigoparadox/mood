#!/usr/bin/env python

X = 0
Y = 1

class Mob( object ):

    def __init__( self, pos, sprite ):
        self.pos = pos
        self.sprite = sprite

    def cast( self, x, cam, facing, plane, screen_sz, zbuffer ):
        mob_x = float( self.pos[X] ) - cam[X]
        mob_y = float( self.pos[Y] ) - cam[Y]

        inv_det = 1.0 / (plane[X] * facing[Y] - facing[X] * \
            plane[Y])

        transform_x = inv_det * (facing[Y] * mob_x - facing[X] * \
            mob_y)
        transform_y = inv_det * (-plane[Y] * mob_x + plane[X] * \
            mob_y)

        mob_screen_x = int( (screen_sz[Y] / 2) * (1 + transform_x / transform_y) )
        mob_height = abs( int(screen_sz[X] / transform_y) )
        mob_ds_y = -mob_height / 2 + screen_sz[X] / 2
        if 0 > mob_ds_y:
            mob_ds_y = 0
        mob_de_y = mob_height / 2 + screen_sz[X] / 2
        if mob_de_y >= screen_sz[X]:
            mob_de_y = screen_sz[X] - 1

        mob_width = abs( int( screen_sz[X] / transform_y ) )
        mob_ds_x = -mob_width / 2 + mob_screen_x
        if 0 > mob_ds_x:
            mob_ds_x = 0
        mob_de_x = mob_width / 2 + mob_screen_x
        if mob_de_x >= screen_sz[Y]:
            mob_de_x = screen_sz[Y] - 1

        for stripe in range( mob_ds_x, mob_de_x - 1 ):
            mob_tex_x = int( 256 * (stripe - (-mob_width / 2 + \
                mob_screen_x)) * 8 / mob_width) / 256

            if 0 >= transform_y or \
            0 >= stripe or \
            screen_sz[X] <= stripe or \
            transform_y >= zbuffer[stripe]:
                continue

            #gfx.line( (255, 0, 0), mob_draw_x, mob_ds_y, mob_de_y, False )
            for mob_draw_y in range( mob_ds_y, mob_de_y - 1 ):

                d = mob_draw_y * 256 - screen_sz[Y] * 128 + mob_height * 128
                mob_tex_y = ((d * 8) / mob_height) / 256
                sprite_tex_col = self.sprite[mob_tex_x]
                sprite_tex_col <<= mob_tex_y

                #print mob_tex_x, mob_tex_y

                #if 1 == (1 & sprite_tex_col):
                yield stripe, mob_draw_y, True
                #else:
                #    yield stripe, mob_draw_y, False

