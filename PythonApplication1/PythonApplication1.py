from re import I
import numpy as np
import turtle

# Constants
GRAVITY = -0.5
JUMP_SPEED = 10
DIVE_SPEED_X = 7
DIVE_SPEED_Y = 15


# Set up the screen
screen = turtle.Screen()
screen.title("Simple Python Game")
screen.bgpic("D:/soucer/rasproject/asset/fondo2.gif")

screen.setup(width=800, height=700)



turtle.register_shape("D:/soucer/rasproject/asset/Standing.gif")
turtle.register_shape("D:/soucer/rasproject/asset/jump.gif")
turtle.register_shape("D:/soucer/rasproject/asset/hit.gif")
turtle.register_shape("D:/soucer/rasproject/asset/jump2.gif")
turtle.register_shape("D:/soucer/rasproject/asset/Hit2.gif")
#turtle.register_shape("D:/soucer/rasproject/asset/fondo2.gif")

# Character movement functions
def move_left(character):
    x = character.xcor()
    if x > -390:  # Adjust the boundary according to your window size
        character.setx(x - 20)

def move_right(character):
    x = character.xcor()
    if x < 390:  # Adjust the boundary according to your window size
        character.setx(x + 20)

def jump(character):
    if character.ycor() <= -250:  # Check if the character is on the ground
        character.velocityY = JUMP_SPEED

def drive(character):
    character.velocityY = -DIVE_SPEED_Y
    character.velocityX = -DIVE_SPEED_X * character.inverted # If player swapped, swap movement

def update(character):
    character.sety(character.ycor() + character.velocityY)
    character.setx(character.xcor() + character.velocityX)
    # Check for ground
    if character.ycor() <= -250:
        character.grounded = 1
        character.sety(-250)
        character.dy = 0
        character.velocityX = 0
        character.velocityY = 0
    else:
    # Apply gravity to character
        character.velocityY += GRAVITY

#change image wen press : (w or Up)        
def change_to_jumpR(character):
    character.shape("D:/soucer/rasproject/asset/jump2.gif") 
    jump(character) 

def change_to_jumpB(character):
    character.shape("D:/soucer/rasproject/asset/jump.gif")
    jump(character)

#change image wen press : (s or Down)
def change_to_driveR(character):
    character.shape("D:/soucer/rasproject/asset/Hit2.gif")
    drive(character)  

def change_to_driveB(character):
    character.shape("D:/soucer/rasproject/asset/hit.gif")
    drive(character)

# Keyboard bindings
screen.listen()
screen.onkeypress(lambda: change_to_jumpB(blu_box), "w")
screen.onkeypress(lambda: change_to_driveB(blu_box), "s")  # 's' key for diving

screen.onkeypress(lambda: change_to_jumpR(red_box), "Up")
screen.onkeypress(lambda: change_to_driveR(red_box), "Down")

# Set up the blue character
blu_box = turtle.Turtle()
blu_box.shape("D:/soucer/rasproject/asset/Standing.gif")
blu_box.color("blue")
blu_box.shapesize(stretch_wid=3, stretch_len=3)
blu_box.penup()
blu_box.speed(0)
blu_box.goto(-250, 0)
blu_box.velocityX = 0
blu_box.velocityY = 0
blu_box.inverted = -1
#blu_box.shape("D:/soucer/rasproject/asset/Standing.gif")

# Set up the red box
red_box = turtle.Turtle()
red_box.shape("D:/soucer/rasproject/asset/Standing.gif")
red_box.color("red")
red_box.shapesize(stretch_wid=3, stretch_len=3)
red_box.penup()
red_box.speed(0)
red_box.goto(250, 0)
red_box.velocityX = 0
red_box.velocityY = 0
red_box.inverted = 1
#red_box.shape("D:/soucer/rasproject/asset/Standing.gif")


# Main game loop
while True:
  update(blu_box)
  update(red_box) 
  screen.update() 
  #turtle.done()