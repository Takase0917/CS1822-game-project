try:
    import simplegui
    import math
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui


# The Vector class


class Vector:

    # Initialiser
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    # Returns a string representation of the vector
    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

    # Tests the equality of this vector and another
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    # Tests the inequality of this vector and another
    def __ne__(self, other):
        return not self.__eq__(other)

    # Returns a tuple with the point corresponding to the vector
    def get_p(self):
        return (self.x, self.y)

    def set_p(self, x, y):
        self.x = x
        self.y = y

    # Returns a copy of the vector
    def copy(self):
        return Vector(self.x, self.y)

    # Adds another vector to this vector
    def add(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __add__(self, other):
        return self.copy().add(other)

    # Negates the vector (makes it point in the opposite direction)
    def negate(self):
        return self.multiply(-1)

    def __neg__(self):
        return self.copy().negate()

    # Subtracts another vector from this vector
    def subtract(self, other):
        return self.add(-other)

    def __sub__(self, other):
        return self.copy().subtract(other)

    # Multiplies the vector by a scalar
    def multiply(self, k):
        self.x *= k
        self.y *= k
        return self

    def __mul__(self, k):
        return self.copy().multiply(k)

    def __rmul__(self, k):
        return self.copy().multiply(k)

    # Divides the vector by a scalar
    def divide(self, k):
        return self.multiply(1/k)

    def __truediv__(self, k):
        return self.copy().divide(k)

    # Normalizes the vector
    def normalize(self):
        return self.divide(self.length())

    # Returns a normalized version of the vector
    def get_normalized(self):
        return self.copy().normalize()

    # Returns the dot product of this vector with another one
    def dot(self, other):
        return self.x * other.x + self.y * other.y

    # Returns the length of the vector
    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

    # Returns the squared length of the vector
    def length_squared(self):
        return self.x**2 + self.y**2

    # Reflect this vector on a normal
    def reflect(self, normal):
        n = normal.copy()
        n.multiply(2*self.dot(normal))
        self.subtract(n)
        return self

    # Returns the angle between this vector and another one
    def angle(self, other):
        return math.acos(self.dot(other) / (self.length() * other.length()))

    # Rotates the vector 90 degrees anticlockwise
    def rotate_anti(self):
        self.x, self.y = -self.y, self.x
        return self

    # Rotates the vector according to an angle theta given in radians
    def rotate_rad(self, theta):
        rx = self.x * math.cos(theta) - self.y * math.sin(theta)
        ry = self.x * math.sin(theta) + self.y * math.cos(theta)
        self.x, self.y = rx, ry
        return self

    # Rotates the vector according to an angle theta given in degrees
    def rotate(self, theta):
        theta_rad = theta / 180 * math.pi
        return self.rotate_rad(theta_rad)

    # project the vector onto a given vector
    def get_proj(self, vec):
        unit = vec.get_normalized()
        return unit.multiply(self.dot(unit))

    # returns x value of vector
    def getX(self):
        return int(self.x)

    # returns y value of vector
    def getY(self):
        return int(self.y)


WIDTH = 500
HEIGHT = 500
CANVAS_DIMS = (WIDTH, HEIGHT)

image = simplegui.load_image(
    'https://i.ytimg.com/vi/JPJ1doUobGY/maxresdefault.jpg')
image_w = 1280
image_h = 720

IMG_player = simplegui.load_image(
    'https://clipartpngfree.com/download/sprite-elvish-spacecraft-opengameartorg')
IMG_CENTRE = (500, 500)
IMG_DIMS = (1000, 1000)

STEP = 0.9
img_rot = 0

# Global variables
img_dest_dim = (90, 90)


class Wheel:
    def __init__(self, pos, radius=10):
        self.pos = pos
        self.vel = Vector()
        self.radius = max(radius, 10)
        self.colour = '#2C6A6A'
        self.img_rot = 0
        self.vel_y = 0

    def draw(self, canvas):
        global img_rot
        # it doesn't matter whether there is or not
        canvas.draw_circle(self.pos.get_p(), self.radius, 1, self.colour)
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

    def on_ground(self):
        if self.pos.y >= CANVAS_DIMS[1]-40:
            return True
        else:
            return False


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
    def __init__(self, wheel, keyboard):
        self.wheel = wheel
        self.keyboard = keyboard

    def update(self):
        global img_rot

        if self.keyboard.right:
            # Still got rotation code if we need it in future
            #img_rot -= STEP
            self.wheel.vel.add(Vector(1, 0))

        if self.keyboard.left:
            #img_rot += STEP
            self.wheel.vel.add(Vector(-1, 0))

        if self.keyboard.up:
            #img_rot -= STEP
            self.wheel.vel.add(Vector(0, -1))

        if self.keyboard.down:
            #img_rot += STEP
            self.wheel.vel.add(Vector(0, 1))


kbd = Keyboard()
wheel = Wheel(Vector(CANVAS_DIMS[0]/2, CANVAS_DIMS[1]/2), 40)
inter = Interaction(wheel, kbd)


def draw(canvas):
    canvas.draw_image(image, (image_w/2, image_h/2),
                      (500, 500), (WIDTH/2, HEIGHT/2), (500, 500))
    inter.update()
    wheel.update()
    wheel.draw(canvas)


frame = simplegui.create_frame('Interactions', CANVAS_DIMS[0], CANVAS_DIMS[1])
frame.set_canvas_background('#2C6A6A')
frame.set_draw_handler(draw)
frame.set_keydown_handler(kbd.keyDown)
frame.set_keyup_handler(kbd.keyUp)
frame.start()
