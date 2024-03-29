try:
    import simplegui
    import random
    from vector import Vector
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui


WIDTH = 700
HEIGHT = 700
CANVAS_DIMS = (WIDTH, HEIGHT)
Game_end = False
Game_started = False
Game_restart = False


background = simplegui.load_image(
    'http://personal.rhul.ac.uk/zkac/332/planet_background_final.jpg')
IMG_backgournd_DIMS = (1890, 1417)
# this is position of picture not player sprite pos
IMG_backgournd_CENTRE = (IMG_backgournd_DIMS[0]/2, IMG_backgournd_DIMS[1]/2)

IMG_player = simplegui.load_image(
    'http://personal.rhul.ac.uk/zkac/332/DurrrSpaceShip_1.png')
IMG_Player_DIMS = (80, 80)
# this is position of picture not player sprite pos
IMG_Player_CENTRE = (IMG_Player_DIMS[0]/2, IMG_Player_DIMS[1]/2)

IMG_meteorite = simplegui.load_image(
    'http://personal.rhul.ac.uk/zkac/332/Meteorite.gif')
IMG_Met_DIMS = (1503, 1213)
# this is position of picture not player sprite pos
IMG_Met_CENTRE = (IMG_Met_DIMS[0]/2, IMG_Met_DIMS[1]/2)

sound = simplegui.load_sound(
    'http://personal.rhul.ac.uk/zkac/332/BoxCat-Games-Battle-Boss.mp3')

img_rot = 0
img_dest_dim = (90, 90)


def rand_step():
    STEP = random.choice([0.03, 0.04, 0.05])
    return STEP


def rand_meteorite():
    pos = Vector(random.randint(0, WIDTH), -40)
    vel = Vector(0, random.randint(3, 5))
    radius = random.randint(10, 50)
    return Meteorite(pos, vel, radius)


def reset_rand_meteorite():
    pos = Vector(random.randint(0, WIDTH), -40)
    vel = Vector(0, random.randint(3, 5))
    radius = random.randint(10, 50)
    return Meteorite(pos, vel, radius)


class Score:
    SCORE_TEXT_SIZE = 25
    SCORE_TEXT_COLOR = "white"

    def __init__(self, pos, score_val):
        self.pos = pos
        self.score_val = score_val

    def draw(self, canvas):
        canvas.draw_text('Score: ' + str(self.score_val),
                         self.pos,
                         self.SCORE_TEXT_SIZE,
                         self.SCORE_TEXT_COLOR)

    def on_hit(self):
        self.score_val = self.score_val + -1

    def score_up(self, add):
        self.score_val = self.score_val + add

    def get_score(self):
        return self.score_val


class Countdown:
    CLOCK_TEXT_SIZE = 25
    CLOCK_TEXT_COLOR = "white"

    def __init__(self, pos, duration):
        self.pos = pos
        self.time_left = duration
        self.timer = simplegui.create_timer(1000, self.tick)

    def draw(self, canvas):
        canvas.draw_text('Time left: ' + str(self.time_left),
                         self.pos,
                         self.CLOCK_TEXT_SIZE,
                         self.CLOCK_TEXT_COLOR)

    def start(self):
        self.timer.start()

    def tick(self):
        if self.time_left > 0 and Game_started:
            self.time_left -= 1
        else:
            self.timer.stop()

    def time_end(self):
        global Game_end
        if self.time_left == 0:
            Game_end = True

    def get_time_left(self):
        return self.time_left

    def reset(self):
        self.time_left = 50


class Meteorite:
    def __init__(self, pos, vel, radius):
        self.pos = pos
        self.vel = vel
        self.radius = radius
        self.img_rot = 0

    def draw(self, canvas):
        global met_dest_dim
        canvas.draw_image(IMG_meteorite,
                          IMG_Met_CENTRE,
                          IMG_Met_DIMS,
                          self.pos.get_p(),
                          img_dest_dim, img_rot)

    def update(self):
        self.pos.add(self.vel)


class SpaceShip:
    LIVES_TEXT_SIZE = 25
    LIVES_TEXT_COLOR = "white"

    def __init__(self, pos, radius):
        self.pos = pos
        self.vel = Vector()
        self.radius = radius
        self.img_rot = 0
        self.vel_y = 0
        self.lives = 3

    def draw(self, canvas):
        global img_rot
        canvas.draw_image(IMG_player, IMG_Player_CENTRE, IMG_Player_DIMS,
                          self.pos.get_p(), img_dest_dim,)
        canvas.draw_text('Lives: ' + str(self.lives),
                         ((25), (100)),
                         self.LIVES_TEXT_SIZE,
                         self.LIVES_TEXT_COLOR)

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

    def ship_hit(self):
        self.lives = self.lives - 1

    def game_over(self):
        global Game_end
        if self.lives <= 0:
            Game_end = True


class Keyboard:
    def __init__(self):
        self.right = False
        self.left = False
        self.up = False
        self.down = False
        self.space = False

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


def click(pos):
    global Game_started
    screen = [WIDTH, HEIGHT]
    is_in_width = (screen[0] - screen[0]) < pos[0] < (screen[0])  # 0 -> 700
    is_in_height = (screen[1] - screen[1]) < pos[1] < (screen[1])  # 0 -> 700
    if not Game_started and is_in_width and is_in_height:
        Game_started = True


def button():
    global Game_started, Game_end, Game_restart
    Game_started = False
    Game_end = False
    Game_restart = True
    spaceship.lives = 3
    countdown.time_left = 50
    score.score_val = 0
    spaceship.pos = Vector(CANVAS_DIMS[0]/2, CANVAS_DIMS[1]/2)
    sound.play()


class Interaction:
    def __init__(self, meteorite, spaceship, keyboard, countdown, score):
        self.meteorite = meteorite
        self.spaceship = spaceship
        self.keyboard = keyboard
        self.countdown = countdown
        self.score = score
        self.in_collision = set()
        self.collision_occured = False
        self.is_mete_nolonger_visible = set()
        self.count = 0

    def hit(self, spaceship, meteorite):  # provisional instance val
        distance = spaceship.pos.copy().subtract(meteorite.pos)
        # if ship radius + met radius bigger than or equal to distance between ship pos and met pos
        return distance.length() <= spaceship.radius + meteorite.radius

    def draw_handler(self, canvas):
        if not Game_end and not Game_started:
            canvas.draw_text('SPACEY', (260, 100), 50, 'Blue', 'monospace')
            canvas.draw_text('How to play: ', (260, 200),
                             25, 'Blue', 'monospace')
            canvas.draw_text(
                'Use the arrow keys to control your spaceship ', (80, 250), 20, 'Gray', 'monospace')
            canvas.draw_text('and dodge the asteroids',
                             (200, 275), 20, 'Gray', 'monospace')
            canvas.draw_text('lives are lost when a collision occurs',
                             (120, 325), 20, 'Gray', 'monospace')
            canvas.draw_text(
                'Points are gained for the amount of time survived', (50, 375), 20, 'Gray', 'monospace')
            canvas.draw_text('Survive till the end to win!',
                             (20, 475), 40, 'Blue', 'monospace')
            canvas.draw_text('Good luck', (225, 550), 40, 'Red', 'monospace')
            canvas.draw_text('Click screen to begin...',
                             (150, 625), 30, 'White', 'monospace')
        elif not Game_end and Game_started:
            self.update()
            canvas.draw_image(background, IMG_backgournd_CENTRE, IMG_backgournd_DIMS,
                              (WIDTH/2, HEIGHT/2), IMG_backgournd_DIMS)  # this is for background
            for met in self.meteorite:
                if not met in self.is_mete_nolonger_visible:  # if not mete which hasn't occurred
                    met.draw(canvas)  # read the list of meteorite
            self.spaceship.draw(canvas)
            self.countdown.draw(canvas)
            self.score.draw(canvas)
        else:
            sound.pause()
            if self.countdown.get_time_left() > 0:
                canvas.draw_text('GAME OVER', (215, 300),
                                 50, 'Red', 'monospace')
            else:
                canvas.draw_text('YOU WIN', (235, 300),
                                 50, 'green', 'monospace')
            canvas.draw_text('You got ' + str(self.score.get_score()) +
                             ' points', (215, 350), 25, 'White', 'monospace')

    def collide(self, spaceship, meteorite):
        if self.hit(spaceship, meteorite):
            mete_exist = meteorite in self.in_collision
            self.score.on_hit()
            if not mete_exist:
                self.in_collision.add(meteorite)
                self.is_mete_nolonger_visible.add(meteorite)
                self.collision_occured = True
                self.count += 1
                score_value = self.score.score_val - 100

    # check wether the meteorite within the canvas
    def is_meteorite_on_canvas(self, meteorite):
        # off top
        # center of the meteorite + the meteorite's radius -> the meteorite's edge
        if meteorite.pos.y + meteorite.radius < 0:
            return False
        # off bottom
        if meteorite.pos.y - meteorite.radius > HEIGHT:
            return True

    def show_rand_mete(self):
        if not Game_restart:
            self.meteorite.add(rand_meteorite())
        if self.countdown.get_time_left() < 35 and not Game_end:
            self.score.score_up(2)
            self.meteorite.add(rand_meteorite())
        if self.countdown.get_time_left() < 25 and not Game_end:
            self.score.score_up(4)
            self.meteorite.add(rand_meteorite())
        if self.countdown.get_time_left() < 15 and not Game_end:
            self.score.score_up(8)
            self.meteorite.add(rand_meteorite())
        else:
            self.meteorite.discard(rand_meteorite())
            self.meteorite.add(reset_rand_meteorite())

    def update(self):
        global Game_started
        for met in self.meteorite:
            met.update()
        self.spaceship.update()
        self.countdown.start()
        self.countdown.time_end()
        self.spaceship.game_over()
        self.score.score_up(1)
        global img_rot
        img_rot -= rand_step()

        for met in self.meteorite:
            if met != self.spaceship:
                self.collide(self.spaceship, met)

        for met in self.in_collision:
            if self.collision_occured:
                self.in_collision.discard(self.is_mete_nolonger_visible)

        if self.count == 1:
            self.spaceship.ship_hit()
            self.count = 0

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


meteorite = set()
spaceship = SpaceShip(Vector(CANVAS_DIMS[0]/2, CANVAS_DIMS[1]/2), 40)
kbd = Keyboard()
countdown = Countdown((25, 50), 50)
score = Score((550, 50), 0)

inter = Interaction(meteorite, spaceship, kbd, countdown, score)

frame = simplegui.create_frame('Asteroids', CANVAS_DIMS[0], CANVAS_DIMS[1])
frame.set_draw_handler(inter.draw_handler)
frame.set_keydown_handler(kbd.keyDown)
frame.set_keyup_handler(kbd.keyUp)
frame.set_mouseclick_handler(click)
frame.add_button("Restart", button)

timer = simplegui.create_timer(1000, inter.show_rand_mete)
timer.start()
frame.start()
sound.play()
