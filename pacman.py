"""Pacman, classic arcade game.

Exercises

1. Change the board.
2. Change the number of ghosts.
3. Change where pacman starts.
4. Make the ghosts faster/slower.
5. Make the ghosts smarter.
"""
# Importación de módulos necesarios
from random import choice  # Para elegir direcciones al azar para los fantasmas
import turtle  # Se utiliza para dibujar y animar en pantalla

from freegames import floor, vector  # Funciones auxiliares

state = {'score': 0}  # Estado global que almacena el puntaje del jugador
path = turtle.Turtle(visible=False)  # Objeto que dibuja el tablero
writer = turtle.Turtle(visible=False)  # Objeto que escribe el puntaje
aim = vector(5, 0)  # Dirección (vectorial) inicial en la que se mueve pacman
pacman = vector(-40, -80)  # Posición inicial de pacman

# Posición y dirección (vectorial) inicial de los fantasmas
ghosts = [
    [vector(-180, 160), vector(10, 0)],
    [vector(-180, -160), vector(0, 10)],
    [vector(100, 160), vector(0, -10)],
    [vector(100, -160), vector(-10, 0)],
]

# Definición del tablero del juego:
# 0: pared, 1: comida, 2: comida consumida.
# fmt: off
tiles = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0,
    0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]
# fmt: on


def square(x, y):
    """Dibuja un cuadrado en la posición (x, y).
     Args:
        x (int): Coordenada x de inicio.
        y (int): Coordenada y de inicio.
    """
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill()

    # Dibuja un cuadrado de 20x20
    for count in range(4):
        path.forward(20)
        path.left(90)

    path.end_fill()


def offset(point):
    """Calcula el índice del tile basado en la posición dada.

    Args:
        point (vector): Posición actual.

    Returns:
        int: Índice correspondiente en la lista 'tiles'.
    """
    # Ajusta la posición para que coincida con la cuadrícula
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    index = int(x + y * 20)
    return index


def valid(point):
    """Verifica si la posición dada es válida (no choca con una pared).

    Args:
        point (vector): Posición a verificar.

    Returns:
        bool: True si la posición es válida, False de lo contrario.
    """
    index = offset(point)
    if tiles[index] == 0:  # Si el tile es 0 el movimiento es inválido
        return False

    index = offset(point + 19)

    if tiles[index] == 0:
        return False
    # Se permite movimiento si la posición está alineada con la cuadrícula
    return point.x % 20 == 0 or point.y % 20 == 0


def world():
    """Dibuja el mundo (tablero) del juego utilizando el turtle 'path'."""
    turtle.bgcolor('black')
    path.color('blue')

    # Itera sobre cada tile para dibujar el tablero
    for index in range(len(tiles)):
        tile = tiles[index]

        # Dibuja el cuadrado si el tile es distinto de 0
        if tile > 0:
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            square(x, y)

            # Si el tile es 1, dibuja el punto de comida en el centro
            if tile == 1:
                path.up()
                path.goto(x + 7, y + 12)
                path.down()
                path.color('gold')  # Cambia el color del punto de comida
                path.begin_fill()

                # Dibuja una estrella de 5 puntas
                for _ in range(5):  
                    path.forward(5)
                    path.right(144)

                path.end_fill()
                path.color('blue')  # Restaura el color original



def move():
    """Actualiza el estado del juego moviendo a pacman y los fantasmas."""
    writer.undo()  # Borra el puntaje anterior
    writer.write(state['score'], font=("Times New Roman", 28, "bold"))  # Escribe el nuevo puntaje

    turtle.clear()  # Limpia la pantalla para el siguiente frame

    # Mueve a pacman si la nueva posición es válida
    if valid(pacman + aim):
        pacman.move(aim)

    # Obtiene el índice del tile donde se encuentra pacman
    index = offset(pacman)

    # Si pacman se encuentra sobre un tile con comida, la consume
    if tiles[index] == 1:
        tiles[index] = 2  # Marca el tile como consumido
        state['score'] += 1
        x = (index % 20) * 20 - 200
        y = 180 - (index // 20) * 20
        square(x, y)

    # Dibuja a pacman como un punto amarillo
    turtle.up()
    turtle.goto(pacman.x + 10, pacman.y + 10)
    turtle.dot(20, 'yellow')

    # Actualiza la posición de cada fantasma
    for point, course in ghosts:
        # Si el movimiento es válido, continúa en la misma dirección
        if valid(point + course):
            point.move(course)
        else:
            # Si el movimiento es inválido, escoge una nueva dirección
            options = [
                vector(10, 0),
                vector(-10, 0),
                vector(0, 10),
                vector(0, -10),
            ]
            plan = choice(options)
            course.x = plan.x
            course.y = plan.y

        # Dibuja al fantasma como un punto rojo
        turtle.up()
        turtle.goto(point.x + 10, point.y + 10)
        turtle.dot(20, 'red')

    turtle.update()  # Actualiza la pantalla

    # Verifica colisiones: termina el juego si pacman choca con un fantasma
    for point, course in ghosts:
        if abs(pacman - point) < 20:
            return

    # Programa la siguiente actualización del juego cada 100 ms
    turtle.ontimer(move, 100)


def change(x, y):
    """Cambia la dirección de pacman si el nuevo movimiento es válido.

    Args:
        x (int): Desplazamiento en el eje x.
        y (int): Desplazamiento en el eje y.
    """
    if valid(pacman + vector(x, y)):
        aim.x = x
        aim.y = y


# Configuración de la ventana del juego
turtle.setup(420, 420, 370, 0)
turtle.hideturtle()  # Oculta el turtle principal
turtle.tracer(False)  # Desactiva la animación de los turtles

# Configuración del turtle 'writer' para mostrar el puntaje
writer.goto(160, 0)
writer.color('yellow')
writer.write(state['score'])
turtle.listen()  # Escucha los eventos del teclado

# Asignación de teclas para cambiar la dirección de pacman
turtle.onkey(lambda: change(5, 0), 'Right')
turtle.onkey(lambda: change(-5, 0), 'Left')
turtle.onkey(lambda: change(0, 5), 'Up')
turtle.onkey(lambda: change(0, -5), 'Down')

world()  # Dibuja el mundo (tablero)
move()  # Inicia el movimiento de pacman y los fantasmas

turtle.done()  # Finaliza la ejecución del turtle
