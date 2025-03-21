"""Tic Tac Toe

Exercises

1. Give the X and O a different color and width.
2. What happens when someone taps a taken spot?
3. How would you detect when someone has won?
4. How could you create a computer player?
"""

# We import the turtle library to draw on the screen
import turtle

# We import the line function from freegames
# This function allows us to draw lines
from freegames import line


def grid():
    """Draw tic-tac-toe grid."""
    line(-67, 200, -67, -200)  # Vertical 1
    line(67, 200, 67, -200)  # Vertical 2
    line(-200, -67, 200, -67)  # Horizontal 1
    line(-200, 67, 200, 67)  # Horizontal 2


def drawx(x, y):
    """Draw X player."""
    turtle.width(4)  # Increases line width
    turtle.color("red")  # Changes the color to red
    line(x, y, x + 83, y + 83)  # Diagonal \
    line(x, y + 83, x + 83, y)  # Diagonal /
    turtle.color("black")  # Return to black
    turtle.width(1)  # Decreases line width


def drawo(x, y):
    """Draw O player."""
    turtle.width(4)  # Increases line width
    turtle.color("blue")  # Changes the color to blue
    turtle.up()  # Disable drawings
    turtle.goto(x + 42, y)  # Moves the turtle
    turtle.down()  # Start drawing
    turtle.circle(42)  # Make a circle with radius 62
    turtle.color("black")  # Return to black
    turtle.width(1)  # Decreases line width


def gridIndex(value):
    """Round value to a certain index on the grid"""
    return int((value + 200) // 133)


def floor(value):
    """Round value down to grid with square size 133."""
    return ((value + 200) // 133) * 133 - 200 + 25
    # 25 is the padding for the new size
    # Possible return values:
    # -175, -42, 91


def gameRule():
    """Check if any player has won"""
    # First check for complete columns or rows
    for i in range(0, 3):
        # Columns
        if cellStates[i][0] == cellStates[i][1] == cellStates[i][2] != 0:
            # Returns the winner value
            return cellStates[i][0]
        # Rows
        if cellStates[0][i] == cellStates[1][i] == cellStates[2][i] != 0:
            # Returns the winner value
            return cellStates[0][i]
    # Now it checks for diagonals
    # Diagonal \
    if cellStates[0][0] == cellStates[1][1] == cellStates[2][2] != 0:
        # Returns the winner value
        return cellStates[0][0]
    # Diagonal /
    if cellStates[0][2] == cellStates[1][1] == cellStates[2][0] != 0:
        # Returns the winner value
        return cellStates[0][2]
    # If there's no winner still, it checks if theres still free spaces
    if all(cell != 0 for row in cellStates for cell in row):
        # If not, then it's a draw
        return 3
    # If we can still play, then it returns 0
    return 0


def win(value):
    """Displays the win message and locks the screen"""
    turtle.up()  # Stops drawing
    turtle.goto(-200, -200)  # Moves to the lower left corner
    if value == 1:  # If X wins
        turtle.write("X wins!", font=("Arial", 20, "bold"))
    elif value == 2:  # If O wins
        turtle.write("O wins!", font=("Arial", 20, "bold"))
    elif value == 3:  # If it's a draw
        turtle.write("It's a Draw!", font=("Arial", 20, "bold"))
    turtle.onscreenclick(None)  # Stops any interaction


state = {'player': 0}  # Sets the first turn as x
players = [drawx, drawo]  # Set of functions


def tap(x, y):
    """Draw X or O in tapped square."""
    indX = gridIndex(x)  # Get X index
    indY = gridIndex(y)  # Get Y index
    x = floor(x)  # Round X value
    y = floor(y)  # Round Y value
    if cellStates[indX][indY] == 0:
        player = state['player']  # Get the current player
        draw = players[player]  # Select the shape
        draw(x, y)  # Draws the shape in the right spot
        turtle.update()  # Update the changes
        state['player'] = not player  # Switch players
        cellStates[indX][indY] = player + 1  # X is 1 and O is 2
        # When the turn is over, checks if anyone has win
        if gameRule() != 0:
            # If so, it gives a winner
            win(gameRule())


# Create a Matrix for the state of each cell
cellStates = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
# Initial setup for the screen (padding of 20px)
turtle.setup(420, 420, 370, 0)
# Hide the pencil from turtle
turtle.hideturtle()
# Disable pencil's animation
turtle.tracer(False)
# Draw the grid
grid()
# Update this change
turtle.update()
# Associate the tap function with clicks
turtle.onscreenclick(tap)
# Keep the window running
turtle.done()
