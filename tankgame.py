try:
    import sys, os, math, random
    import pygame
    from pygame.locals import *

except ImportError, err:
    print "%s Failed to Load Module: %s" % (__file__,  err)
    sys.exit(1)



class Paddle(pygame.sprite.Sprite):
    """docstring for Paddle"""
    def __init__(self, xy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('images','pong_paddle.gif'))
        self.rect = self.image.get_rect()

        self.rect.centerx, self.rect.centery = xy

        self.movementspeed = 5

        self.velocity = 0

    def up(self):
        self.velocity-= self.movementspeed

    def down(self):
        self.velocity+= self.movementspeed

    def move(self, dy):
        if self.rect.bottom + dy >400:
            self.rect.bottom = 400
        elif self.rect.top + dy < 0:
            self.rect.top = 0
        else:
            self.rect.y += dy

    def update(self):
            self.move(self.velocity)    




class Game(object):
    """docstring for Game"""
    
    def __init__(self):
        
        pygame.init () 

        self.window = pygame.display.set_mode ((800, 400))

        self.clock = pygame.time.Clock ()

        pygame.display.set_caption("PONG")

        pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP]) 
        
        self.backround = pygame.Surface((800, 400))
        self.backround.fill ((255,255,255))
        pygame.draw.line(self.backround, (0,0,0), (400,0), (400,400), 2)
        self.window.blit(self.backround, (0,0))
        pygame.display.flip()

        self.sprites = pygame.sprite.RenderUpdates()

        self.leftpaddle = Paddle ((50,200))
        self.sprites.add (self.leftpaddle)
        self.rightpaddle = Paddle ((750,200))
        self.sprites.add (self.rightpaddle)

    def run(self):
        
        print 'Starting Event Loop'

        running = True
        while running:
            self.clock.tick(60)

            running = self.handleEvents()

            pygame.display.set_caption('PONG  %d fps')

            for sprite in self.sprites:
                sprite.update()

            self.sprites.clear(self.window, self.backround)
            dirty = self.sprites.draw(self.window)

            pygame.display.update(dirty)

        print 'Thanks for Playing!!!!!'



    def handleEvents(self):
        
        for event in pygame.event.get():
            if event.type == QUIT:
                return False


            elif event.type == KEYDOWN:

                if event.key == K_ESCAPE:
                    return False

                if event.key == K_w:
                    self.leftpaddle.up()

                if event.key == K_s:
                    self.leftpaddle.down()


                if event.key == K_UP:
                    self.rightpaddle.up()

                if event.key == K_DOWN:
                    self.rightpaddle.down()

            elif event.type == KEYUP:

               
                if event.key == K_w:
                    self.leftpaddle.down()

                if event.key == K_s:
                    self.leftpaddle.up()


                if event.key == K_UP:
                    self.rightpaddle.down()

                if event.key == K_DOWN:
                    self.rightpaddle.up()

        return True


if __name__ == '__main__':
    game = Game()
    game.run()


