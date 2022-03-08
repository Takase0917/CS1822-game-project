# CS1822-game-project (this is discription for game project)
Games:

Scoring based on timing, level increases the longer you survive in the game, background changes colour to indicate this. Try to add background music.


2.1 
Sprite: 
Lives: start with 3, lose life when hit with projectile
Score: based on time survived, score doubles each level passed

2.2
Welcome screen: has instructions
Lives go to 0, everything resets

2.3
Player controls sprite, arrow keys
Animation changes with direction

2.4
Vector class used: projectiles use velocity

2.5
Physics with collisions with projectiles, bounce off the edge of the canvas

2.6
Sprite in player class
‘Enemy’ class, projectiles saved in a list. Increased amount of projectiles per level, Increased speed per level
Interaction class
Game class



Additional
Destroy projectiles?
Powerups: reduce speed for an amount of time, invincibility
Scoreboard
Projectiles interactions (bounce)
Multiple levels based on time survived




Welcome screen:
Canvas size: 700px x 700px
Background: space themed
Start game:
Instructions: avoid asteroids, gain power ups, score based on time lasted
Leaderboard?
Music, Sound effects?

Game:
Timer: 3 minutes total, game is won if player lasts till timer ends
Score Counter: score increases every second, as level increases the counter increases. Extra score from powerup
Powerups: sprite change colour to indicate powerup
-  Slow down projectiles for 10 secs
	-  Invincibility for 10 secs
Levels: 3 levels, increases each minute survived. Background change to indicate level 
change/ enemy sprites change to indicate level change
Level 1: 2 projectiles, 1 power up
Level 2: 4 projectiles, 2 power ups
Level 3: 6 projectiles, 3 power ups
Lives: 3 lives, player loses a life if hit by projectile
Lose Screen: option to add score to leaderboard, play again/exit
Win Screen: option to add score to leaderboard, play again/exit

Sprites:
Player sprite: rocket, changes thruster direction to opposite way of moving
Projectile sprites: asteroids, change tail direction to opposite way of moving, change colour when level increases
PowerupSlow sprites: 
PowerupInvincible sprites:


Classes:
Player: rocket
Projectile: asteroids
PowerupSlow: slime
PowerupInvincible: force field/ shield
Keyboard:
Interaction:
Game:
Vector
Levels: defines the levels, no of powerups, no of enemy sprites
