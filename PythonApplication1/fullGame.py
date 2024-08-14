import cv2
import numpy as np
import pygame
import turtle

# Open the webcam (usually the default webcam)
cap = cv2.VideoCapture(0)

# Check if the webcam is opened successfully
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Set new resolution
new_width = 640
new_height = 480
cap.set(3, new_width)
cap.set(4, new_height)

# ROI boundaries (x, y, width, height)
roi_values = [
(400, 0, 200, 150),
(0, 330, 150, 100),
(0, 0, 200, 150),
(400, 330, 150, 100)
]
# Flags to track movement detection for each corner
movement_detected = [False] * len(roi_values)

# Constants
GRAVITY = -0.5
JUMP_SPEED = 15
DIVE_SPEED_X = 15
DIVE_SPEED_Y = 15

# Initialize player scores
blu_box_score = 0
red_box_score = 0

pygame.init()

# Set up the screen
turtle.register_shape("D:/soucer/rasproject/asset/hit.gif")
screen = turtle.Screen()
screen.title("Divekick Copy")
screen.bgpic("D:/soucer/rasproject/asset/fondo2.gif")
screen.setup(width=800, height=750)

turtle.register_shape("D:/soucer/rasproject/asset/Standing.gif")
turtle.register_shape("D:/soucer/rasproject/asset/jump.gif")
turtle.register_shape("D:/soucer/rasproject/asset/hit.gif")
turtle.register_shape("D:/soucer/rasproject/asset/jump2.gif")
turtle.register_shape("D:/soucer/rasproject/asset/Hit2.gif")

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

#blu_box.shape("/home/rasp/rasproject/asset/hit.gif")

blu_box.inAir = False
#blu_box.shape("/home/rasp/rasproject/asset/hit.gif")


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

red_box.inAir = False
#red_box.shape("/home/rasp/rasproject/asset/Standing.gif")


def jump(character):
    if character.ycor() <= -250:  # Check if the character is on the ground
        character.velocityY = JUMP_SPEED
        character.inAir = True

def dive(character):
    if character.inAir:
        character.velocityY = -DIVE_SPEED_Y
        character.velocityX = -DIVE_SPEED_X * character.inverted  # If player swapped, swap movement


#change image wen press : (w or Up)        
def change_to_jumpR(character):
    character.shape("D:/soucer/rasproject/asset/jump2.gif") 
    jump(character) 

def change_to_jumpB(character):
    character.shape("D:/soucer/rasproject/asset/jump.gif")
    jump(character)

#change image wen press : (s or Down)
def change_to_diveR(character):
    character.shape("D:/soucer/rasproject/asset/Hit2.gif")
    dive(character)  

def change_to_diveB(character):
    character.shape("D:/soucer/rasproject/asset/hit.gif")
    dive(character)

# Keyboard bindings
screen.listen()
screen.onkeypress(lambda: change_to_jumpB(blu_box), "w")
screen.onkeypress(lambda: change_to_diveB(blu_box), "s")  # 's' key for diving

screen.onkeypress(lambda: change_to_jumpR(red_box), "Up")
screen.onkeypress(lambda: change_to_diveR(red_box), "Down")


def update(character, movement_detected_flag, corner_index, other_character):
    global blu_box_score, red_box_score
    
    character.sety(character.ycor() + character.velocityY)
    character.setx(character.xcor() + character.velocityX)

    # Check for ground
    if character.ycor() <= -250:
        character.grounded = 1
        character.sety(-250)
        character.dy = 0
        character.velocityX = 0
        character.velocityY = 0
        character.inAir = False
        character.shape("D:/soucer/rasproject/asset/Standing.gif")
    else:
        # Apply gravity to character
        character.velocityY += GRAVITY

    # Check for movement detection flag
    if movement_detected_flag:
        perform_action(character, corner_index)
        

    # Check for screen boundaries in x-coordinates
    if character.xcor() > 390:
        character.setx(390)
        character.velocityX = 0
    elif character.xcor() < -390:
        character.setx(-390)
        character.velocityX = 0

    # Collision detection between characters
    if (
        character.xcor() - character.shapesize()[1] * 10 < other_character.xcor() + other_character.shapesize()[1] * 10 and
        character.xcor() + character.shapesize()[1] * 10 > other_character.xcor() - other_character.shapesize()[1] * 10 and
        character.ycor() - character.shapesize()[0] * 10 < other_character.ycor() + other_character.shapesize()[0] * 10 and
        character.ycor() + character.shapesize()[0] * 10 > other_character.ycor() - other_character.shapesize()[0] * 10
    ):
        if character.ycor() + character.shapesize()[0] * 10 > other_character.ycor() + other_character.shapesize()[0] * 10:
            
            # Collision from the top, give a point to the hitting player
            if character == blu_box:
                red_box_score += 1
            elif character == red_box:
                blu_box_score += 1
            print("Blue Box Score:", blu_box_score)
            print("Red Box Score:", red_box_score)

        # Check the direction of collision
        if character.ycor() + character.shapesize()[0] * 10 > other_character.ycor() + other_character.shapesize()[0] * 10:
            # Collision from the top, reset the characters
            character.setx(-250)
            character.sety(-250)
            other_character.setx(250)
            other_character.sety(-250)
            character.velocityY = 0
            other_character.velocityY = 0
            print("Top Collision - Resetting Players")
        else:
            # Collision from the side, handle collision logic here
            print("Side Collision")
            
    if character.xcor() > other_character.xcor():
        character.inverted = 1
        other_character.inverted = -1
    else:
        character.inverted = -1
        other_character.inverted = 1


def perform_action(character, corner_index):
    if corner_index == 0:
        #print(f"Corner {corner_index + 1}: Jumping Red Box")
        change_to_jumpR(red_box)
    elif corner_index == 1:
        #print(f"Corner {corner_index + 1}: Diving Blue Box")
        change_to_diveB(blu_box)
    elif corner_index == 2:
        #print(f"Corner {corner_index + 1}: Jumping Blue Box")
        change_to_jumpB(blu_box)
    elif corner_index == 3:
        #print(f"Corner {corner_index + 1}: Diving Red Box")
        change_to_diveR(red_box)

# Main game loop
while True:
    # Read a frame from the webcam
    ret, frame = cap.read()
    # Check if the frame was read successfully
    if not ret:
        print("Error: Could not read frame.")
        break

    frame = cv2.resize(frame, (new_width, new_height))

    # Loop over each ROI and process them separately
    for i, (roi_x, roi_y, roi_width, roi_height) in enumerate(roi_values):
        
        # Define ROI
        roi = frame[roi_y:roi_y + roi_height, roi_x:roi_x + roi_width]

        # Convert ROI to grayscale
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        # Calculate absolute difference between consecutive frames
        if f'prev_gray_roi_{i}' in locals():
            
            frame_diff = cv2.absdiff(eval(f'prev_gray_roi_{i}'), gray_roi)

            # Apply a threshold to detect motion areas
            _, threshold = cv2.threshold(frame_diff, 140, 255, cv2.THRESH_BINARY)

            # Check for movement
            if np.sum(threshold) > 0 and not movement_detected[i]:
                print(f"Corner {i + 1}: Movement detected")
                movement_detected[i] = True
                
                perform_action(blu_box if i ==0 else red_box, i)

                
            elif np.sum(threshold) == 0:
                movement_detected[i] = False
                
                # Find contours in the thresholded image
            contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Draw rectangles around detected motion areas
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (roi_x + x, roi_y + y), (roi_x + x + w, roi_y + y + h), (0, 255, 0), 2)

                
        exec(f'prev_gray_roi_{i} = gray_roi.copy()')                
    screen.update()
    update(blu_box, movement_detected[0], 0, red_box)
    update(red_box, movement_detected[1], 1, blu_box)


    # Display the camera feed
    cv2.imshow('Webcam', frame)

    # Wait for 'q' key to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
