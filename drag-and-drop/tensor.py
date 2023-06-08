import pygame
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Define the tensor data
tensor_data = [
    [[[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]],
     [[0.0, 0.0, 1.0], [1.0, 1.0, 0.0]]],

    [[[0.0, 1.0, 1.0], [1.0, 0.0, 1.0]],
     [[1.0, 0.5, 0.5], [0.5, 1.0, 0.5]]]
]

# Set up the display
pygame.init()
width, height = 800, 600
pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
pygame.display.set_caption("3D Tensor Visualization")

# Set up the OpenGL viewport
glViewport(0, 0, width, height)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(45, width / height, 0.1, 50.0)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()
gluLookAt(5, 5, 10, 0, 0, 0, 0, 1, 0)
glEnable(GL_DEPTH_TEST)  # Enable depth testing

# Main rendering loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Draw the tensor
    for i in range(len(tensor_data)):
        for j in range(len(tensor_data[0])):
            for k in range(len(tensor_data[0][0])):
                color = tensor_data[i][j][k]
                glBegin(GL_QUADS)
                glColor3f(color[0], color[1], color[2])
                glVertex3f(i-0.5, j-0.5, k-0.5)
                glVertex3f(i+0.5, j-0.5, k-0.5)
                glVertex3f(i+0.5, j+0.5, k-0.5)
                glVertex3f(i-0.5, j+0.5, k-0.5)
                glEnd()

    pygame.display.flip()

# Quit the game
pygame.quit()
