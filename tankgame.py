#!/usr/bin/env python

try:
    import sys, os, math, random
    import pygame
    from pygame.locals import *

except ImportError, err:
    print "%s Failed to Load Module: %s" % (__file__, err)
    sys.exit(1)

class Paddle(pygame.sprite.Sprite):
    """A paddle sprite. Subclasses the pygame sprite class.
    Handles its own position so it will not go off the screen."""

    def __init__(self, xy):
        # initialize the pygame sprite part
        pygame.sprite.Sprite.__init__(self)
        # set image and rect
        self.image = pygame.image.load(os.path.join('images','pong_paddle.gif'))
        self.rect = self.image.get_rect()

        # set position
        self.rect.centerx, self.rect.centery = xy

        # the movement speed of our paddle
        self.movementspeed = 5

        # the current velocity of the paddle -- can only move in Y direction
        self.velocity_x = 0
        self.velocity_y = 0

    def up(self):
        """Increases the vertical velocity"""
        self.velocity_y -= self.movementspeed

    def down(self):
        """Decreases the vertical velocity"""
        self.velocity_y += self.movementspeed

    def left(self):
        """Increases the horizontal velocity"""
        self.velocity_x -= self.movementspeed

    def right(self):
        """Decreases the horizontal velocity"""
        self.velocity_x += self.movementspeed

    def move(self, dx, dy):
        """Move the paddle. Don't go off the screen."""
        if self.rect.right + dx > 800:
            self.rect.right = 800
        elif self.rect.left + dx < 0:
            self.rect.left = 0
        else:
            self.rect.x += dx

        if self.rect.bottom + dy > 400:
            self.rect.bottom = 400
        elif self.rect.top + dy < 0:
            self.rect.top = 0
        else:
            self.rect.y += dy

    def update(self):
        """Called to update the sprite. Do this every frame. Handles
        moving the sprite by its velocity"""
        self.move(self.velocity_x, self.velocity_y)


class Ball(pygame.sprite.Sprite):
    """docstring for Ball"""
    def __init__(self,xy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('images','pong_ball.gif'))
 
        self.rect = self.image.get_rect()

        self.rect.centerx, self.rect.centery = xy
        self.maxspeed = 10
        self.servespeed = 5
        self.velx = 0
        self.vely = 0

    def reset(self):
        self.rect.centerx, self.rect.centery = 400, 200
        self.velx = 0
        self.vely = 0        

    def serve(self):
        angle = random.randint(-45, 45)

        if abs(angle) < 5 or abs(angle-180) < 5:
            angle = random.randint(10,20)

        if random.random() > .5:
                angle += 180

        x = math.cos(math.radians(angle))
        y = math.sin(math.radians(angle))

        self.velx = self.servespeed * x
        self.vely = self.servespeed * y
        

class Score(pygame.sprite.Sprite) :
    def __init__(self, xy):
        pygame.sprite.Sprite.__init__(self)
        self.xy = xy

        self.font = pygame.font.Font(None, 50)

        self.leftscore = 0

        self.rightscore = 0

        self.reRender()

    def update(self):
        pass 

    def left(self):
        self.leftscore += 1  

        self.reRender()

    def right(self):
        self.rightscore += 1

        self.reRender()

    def reset(self):
        self.leftscore = 0

        self.rightscore = 0

        self.reRender()

    def reRender(self):
        self.image = self.font.render("%d     %d"%(self.leftscore, self.rightscore), True, (0,0,0))
        self.rect = self.image.get_rect()

        self.rect.center = self.xy


   



class Game(object):
    """Our game object! This is a fairly simple object that handles the
    initialization of pygame and sets up our game to run."""

    def __init__(self):
        """Called when the the Game object is initialized. Initializes
        pygame and sets up our pygame window and other pygame tools
        that we will need for more complicated tutorials."""

        # load and set up pygame
        pygame.init()

        # create our window
        self.window = pygame.display.set_mode((800, 400))

        # clock for ticking
        self.clock = pygame.time.Clock()

        # set the window title
        pygame.display.set_caption('Pong')

        # tell pygame to only pay attention to certain events
        # we want to know if the user hits the X on the window, and we
        # want keys so we can close the window with the esc key
        pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])

        # make background -- all white, with black line down the middle
        self.background = pygame.Surface((800,400))
        self.background.fill((255,255,255))
        # draw the line vertically down the center
        pygame.draw.line(self.background, (0,0,0), (400,0), (400,400), 2)
        self.window.blit(self.background, (0,0))
        # flip the display so the background is on there
        pygame.display.flip()

        # a sprite rendering group for our ball and paddles
        self.sprites = pygame.sprite.RenderUpdates()

        # create our paddles and add to sprite group
        self.leftpaddle = Paddle((50,200))
        self.sprites.add(self.leftpaddle)
        self.rightpaddle = Paddle((750,200))
        self.sprites.add(self.rightpaddle)

        self.ball = Ball((400,200))

        self.sprites.add(self.ball)

        self.scoreImage = Score((400, 50))

        self.sprites.add(self.scoreImage)

        self.pingsound = pygame.mixer.Sound(os.path.join('sound', 'ping.wav'))
        self.pongsound = pygame.mixer.Sound(os.path.join('sound', 'pong.wav'))


    def manageBall(self):
        self.ball.rect.x += self.ball.velx
        self.ball.rect.y += self.ball.vely

        if self.ball.rect.top < 0:
            self.ball.rect.top = 1

            self.ball.vely *= -1

            self.pingsound.play()

        elif self.ball.rect.bottom > 400:
            self.ball.rect.bottom = 399

            self.ball.vely *= -1

            self.pingsound.play()

        if self.ball.rect.left < 0:
            self.scoreImage.right()

            self.ball.reset()

            return

        elif self.ball.rect.right > 800:
            self.scoreImage.left()

            self.ball.reset()

            return

        collided = pygame.sprite.spritecollide(self.ball, [self.leftpaddle, self.rightpaddle], dokill=False)

        if len(collided) > 0:
            hitpaddle = collided[0]

            self.ball.velx *= -1

            self.ball.rect.x += self.ball.velx

            self.ball.vely += hitpaddle.velocity_y / 3.0             
            self.pongsound.play()


    def run(self):
        """Runs the game. Contains the game loop that computes and renders
        each frame."""

        print 'Starting Event Loop'

        running = True
        # run until something tells us to stop
        while running:


            # tick pygame clock
            # you can limit the fps by passing the desired frames per seccond to tick()
            self.clock.tick(60)

            # handle pygame events -- if user closes game, stop running
            running = self.handleEvents()

            self.manageBall()

            # update the title bar with our frames per second
            pygame.display.set_caption('Pong   %d fps' % self.clock.get_fps())

            # update our sprites
            for sprite in self.sprites:
                sprite.update()

            # render our sprites
            self.sprites.clear(self.window, self.background)    # clears the window where the sprites currently are, using the background
            dirty = self.sprites.draw(self.window)              # calculates the 'dirty' rectangles that need to be redrawn

            # blit the dirty areas of the screen
            pygame.display.update(dirty)                        # updates just the 'dirty' areas

        print 'Quitting. Thanks for playing'


    def handleEvents(self):
        """Poll for PyGame events and behave accordingly. Return false to stop
        the event loop and end the game."""

        # poll for pygame events
        for event in pygame.event.get():
            if event.type == QUIT:
                return False

            # handle user input
            elif event.type == KEYDOWN:
                # if the user presses escape, quit the event loop.
                if event.key == K_ESCAPE:
                    return False

                # paddle control
                elif event.key == K_w:
                    self.leftpaddle.up()
                elif event.key == K_s:
                    self.leftpaddle.down()

                elif event.key == K_d:
                    self.leftpaddle.right()
                elif event.key == K_a:
                    self.leftpaddle.left()

                elif event.key == K_RIGHT:
                    self.rightpaddle.right()
                elif event.key == K_LEFT:
                    self.rightpaddle.left()

                elif event.key == K_UP:
                    self.rightpaddle.up()
                elif event.key == K_DOWN:
                    self.rightpaddle.down()

                elif event.key == K_SPACE:
                    if self.ball.velx == 0 and self.ball.vely == 0:
                        self.ball.serve()

            elif event.type == KEYUP:
                # paddle control
                if event.key == K_w:
                    self.leftpaddle.down()
                elif event.key == K_s:
                    self.leftpaddle.up()

                elif event.key == K_d:
                    self.leftpaddle.left()
                elif event.key == K_a:
                    self.leftpaddle.right()

                elif event.key == K_UP:
                    self.rightpaddle.down()
                elif event.key == K_DOWN:
                    self.rightpaddle.up()

                elif event.key == K_RIGHT:
                    self.rightpaddle.left()
                elif event.key == K_LEFT:
                    self.rightpaddle.right()

        return True


# create a game and run it
if __name__ == '__main__':
    game = Game()
    game.run()
