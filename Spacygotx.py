try:
    import simplegui
    import random
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


def rand_meteorite():
    met_pos_x_1 = (0, random.randint(0, HEIGHT))

    pos = Vector(random.randint(0, WIDTH), -40)
    vel = Vector(0, random.randint(3, 5))
    radius = random.randint(10, 50)

    return Meteorite(pos, vel, radius)


WIDTH = 700
HEIGHT = 700
CANVAS_DIMS = (WIDTH, HEIGHT)

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
class Score:
    SCORE_TEXT_SIZE = 50
    SCORE_TEXT_COLOR = "white"
    
    def __init__(self, pos, score_val):
        self.pos = pos        
        self.score_val = score_val

    def draw(self, canvas):
        canvas.draw_text(str(self.score_val),
                         self.pos.get_p(),
                         self.SCORE_TEXT_SIZE,
                         self.SCORE_TEXT_COLOR)
        
    def update(self, score_value):
        self.score_val == score_value
        
class Countdown:
    CLOCK_TEXT_SIZE = 50
    CLOCK_TEXT_COLOR = "white"

    def __init__(self, pos, duration):
        self.pos = pos
        self.time_left = duration
        self.timer = simplegui.create_timer(1000, self.tick)
        
    def draw(self, canvas):
        canvas.draw_text(str(self.time_left),
                         self.pos.get_p(),
                         self.CLOCK_TEXT_SIZE,
                         self.CLOCK_TEXT_COLOR)
  
    def start(self):
        self.timer.start()
        
    def tick(self):
        if self.time_left > 0:
            self.time_left -= 1
        else:
            self.timer.stop()        

        
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

    def get_X(self):
        return Vector.getX(self.pos)
    
    def update(self):
        self.pos.add(self.vel)


class Wheel:
    def __init__(self, pos, radius=10):
        self.pos = pos
        self.vel = Vector()
        self.radius = max(radius, 10)
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
        if (Y + self.radius) < 0:
            self.pos.set_p((X), (HEIGHT + self.radius))
        if (Y - self.radius) > HEIGHT:
            self.pos.set_p((X), (0 - self.radius))

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
    def __init__(self, wheel, keyboard, countdown, score):
        self.meteorite_list = []
        self.wheel = wheel
        self.keyboard = keyboard
        self.countdown = countdown
        self.score = score
        self.countdown.start()
        
    def draw_handler(self, canvas):
        canvas.draw_image(image, (image_w/2, image_h/2), (WIDTH, HEIGHT),
                          (WIDTH/2, HEIGHT/2), (WIDTH, HEIGHT))  # this is for background
        self.update()
        for meteorite in self.meteorite_list:
            meteorite.draw(canvas)  # read the list of meteorite
        self.wheel.draw(canvas)
        self.countdown.draw(canvas)   
        self.score.draw(canvas)

    def add_random_meteorite(self):
        # added rand_meteorite to new list of the meteorite
        self.meteorite_list.append(rand_meteorite())

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
        score_value = 0
        global img_rot
        for meteorite in self.meteorite_list:
            meteorite.update()
            print(meteorite.get_X())
            if meteorite.pos == self.wheel.pos:
                score_value == self.score.score_val - 100
        self.wheel.update()
        self.score.update(score_value)

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

score = Score(Vector(500, 100), 1000)
countdown = Countdown(Vector(100, 100), 100)
kbd = Keyboard()
wheel = Wheel(Vector(CANVAS_DIMS[0]/2, CANVAS_DIMS[1]/2), 40)
inter = Interaction(wheel, kbd, countdown, score)

frame = simplegui.create_frame('Interactions', CANVAS_DIMS[0], CANVAS_DIMS[1])
frame.set_draw_handler(inter.draw_handler)
frame.set_keydown_handler(kbd.keyDown)
frame.set_keyup_handler(kbd.keyUp)

timer = simplegui.create_timer(500, inter.add_random_meteorite)

timer.start()
frame.start()
