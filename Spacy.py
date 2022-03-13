try:
    import simplegui
    import random
    import math
    from vector import Vector
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui


WIDTH = 700
HEIGHT = 700
CANVAS_DIMS = (WIDTH, HEIGHT)
NUM_METEORITES = 10

image = simplegui.load_image(
    'https://i.ytimg.com/vi/JPJ1doUobGY/maxresdefault.jpg')
image_w = 1280
image_h = 720

IMG_player = simplegui.load_image(
    'https://clipartpngfree.com/download/sprite-elvish-spacecraft-opengameartorg')
IMG_DIMS = (1000, 1000)
# this is position of picture not player sprite pos
IMG_CENTRE = (IMG_DIMS[0]/2, IMG_DIMS[1]/2)


# https://pngset.com/images/download-free-asteroid-redirect-asteroid-rock-limestone-moon-outer-space-transparent-png-2831660.png
IMG_meteorite = simplegui.load_image(
    'https://clipartpngfree.com/thumbnail/learning/secondary_school_what_to_learn.png')
IMG_Met_DIMS = (1024, 832)
# this is position of picture not player sprite pos
IMG_Met_CENTRE = (IMG_Met_DIMS[0]/2, IMG_Met_DIMS[1]/2)


STEP = 0.9
img_rot = 0

# Global variables
img_dest_dim = (90, 90)


def rand_meteorite():
    pos = Vector(random.randint(0, WIDTH), -40)
    vel = Vector(0, random.randint(3, 5))
    radius = random.randint(10, 50)

    return Meteorite(pos, vel, radius)


class Meteorite:
    def __init__(self, pos, vel, radius):
        self.pos = pos
        self.vel = vel
        self.radius = radius

    def draw(self, canvas):
        global met_dest_dim
        canvas.draw_image(IMG_meteorite,
                          IMG_Met_CENTRE,
                          IMG_Met_DIMS,
                          self.pos.get_p(),
                          img_dest_dim)

    def update(self):
        self.pos.add(self.vel)


class SpaceShip:
    def __init__(self, pos, radius):
        self.pos = pos
        self.vel = Vector()
        self.radius = radius
        self.img_rot = 0
        self.vel_y = 0

    def draw(self, canvas):
        global img_rot
        canvas.draw_image(IMG_player, IMG_CENTRE, IMG_DIMS,
                          self.pos.get_p(), img_dest_dim, img_rot)

    def update(self):
        self.pos.add(self.vel)
        self.vel.multiply(0.85)
        X = self.pos.getX()
        Y = self.pos.getY()
        if (X + self.radius) < 0:
            self.pos.set_p((WIDTH + self.radius), (Y))
        if (X - self.radius) > WIDTH:
            self.pos.set_p((0 - self.radius), (Y))

    # def on_ground(self):
        # if self.pos.y >= CANVAS_DIMS[1]-40:
            # return True
       # else:
            # return False


class Keyboard:
    def __init__(self):
        self.right = False
        self.left = False
        self.up = False
        self.down = False

    def keyDown(self, key):
        if key == simplegui.KEY_MAP['right']:
            self.right = True

        if key == simplegui.KEY_MAP['left']:
            self.left = True

        if key == simplegui.KEY_MAP['up']:
            self.up = True

        if key == simplegui.KEY_MAP['down']:
            self.down = True

    def keyUp(self, key):
        if key == simplegui.KEY_MAP['right']:
            self.right = False

        if key == simplegui.KEY_MAP['left']:
            self.left = False

        if key == simplegui.KEY_MAP['up']:
            self.up = False

        if key == simplegui.KEY_MAP['down']:
            self.down = False


class Interaction:
    def __init__(self, meteorite, spaceship, keyboard):
        self.meteorite = meteorite
        self.spaceship = spaceship
        self.keyboard = keyboard
        self.in_collision = set()

    def hit(self, spaceship, meteorite):  # provisional instance val
        distance = spaceship.pos.copy().subtract(meteorite.pos)
        # if ship radius + met radius bigger than or equal to distance between ship pos and met pos
        return distance.length() <= spaceship.radius + meteorite.radius

    def draw_handler(self, canvas):
        canvas.draw_image(image, (image_w/2, image_h/2), (WIDTH, HEIGHT),
                          (WIDTH/2, HEIGHT/2), (WIDTH, HEIGHT))  # this is for background
        self.update()
        for met in self.meteorite:
            met.draw(canvas)  # read the set of meteorite
        self.spaceship.draw(canvas)

    def collide(self, spaceship, meteorite):
        if self.hit(spaceship, meteorite):
            print("hit")
            shipmete = (spaceship, meteorite) in self.in_collision
            print(shipmete)

            if not shipmete:
                self.in_collision.add((spaceship, meteorite))
            else:

                # check wether the meteorite within the canvas

    def is_meteorite_on_canvas(self, meteorite):
        # off top
        # center of the meteorite + the meteorite's radius -> the meteorite's edge
        if meteorite.pos.y + meteorite.radius < 0:
            return False
        # off bottom
        if meteorite.pos.y - meteorite.radius > HEIGHT:
            return True

    def update(self):
        for met in self.meteorite:
            met.update()
        self.spaceship.update()

        for met in self.meteorite:
            if met != self.spaceship:
                self.collide(self.spaceship, met)

        if self.keyboard.right:
            # Still got rotation code if we need it in future
            #img_rot -= STEP
            self.spaceship.vel.add(Vector(1, 0))

        if self.keyboard.left:
            #img_rot += STEP
            self.spaceship.vel.add(Vector(-1, 0))

        if self.keyboard.up:
            #img_rot -= STEP
            self.spaceship.vel.add(Vector(0, -1))

        if self.keyboard.down:
            #img_rot += STEP
            self.spaceship.vel.add(Vector(0, 1))


kbd = Keyboard()
spaceship = SpaceShip(Vector(CANVAS_DIMS[0]/2, CANVAS_DIMS[1]/2), 40)
meteorite = [rand_meteorite() for i in range(NUM_METEORITES)]
inter = Interaction(meteorite, spaceship, kbd)

frame = simplegui.create_frame('Interactions', CANVAS_DIMS[0], CANVAS_DIMS[1])
frame.set_draw_handler(inter.draw_handler)
frame.set_keydown_handler(kbd.keyDown)
frame.set_keyup_handler(kbd.keyUp)


frame.start()
