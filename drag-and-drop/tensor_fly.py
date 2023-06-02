import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

tensor_data = [
    [[[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]],
     [[0.0, 0.0, 1.0], [1.0, 1.0, 0.0]]],
    
    [[[0.0, 1.0, 1.0], [1.0, 0.0, 1.0]],
     [[1.0, 0.5, 0.5], [0.5, 1.0, 0.5]]]
]

pygame.init()
width, height = 800, 600
pygame.display.set_mode((width, height), DOUBLEBUF|OPENGL)
pygame.display.set_caption("3D Tensor Visualization")

glViewport(0, 0, width, height)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(45, (width/height), 0.1, 50.0)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()
gluLookAt(5, 5, 10, 0, 0, 0, 0, 1, 0)
glEnable(GL_DEPTH_TEST)

angle = 0.0

# Load the font for rendering labels
font = pygame.font.Font(None, 64)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glPushMatrix()
    glRotatef(angle, 0, 1, 0)

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

                # Save the current projection and modelview matrices
                proj_matrix = glGetDoublev(GL_PROJECTION_MATRIX)
                modelview_matrix = glGetDoublev(GL_MODELVIEW_MATRIX)
                viewport = glGetIntegerv(GL_VIEWPORT)

                # Adjust the position to be within the viewing volume
                adjusted_i = i-0.5
                adjusted_j = j-0.5
                adjusted_k = k-0.5

                # Get the screen coordinates of the current vertex
                x, y, _ = gluProject(adjusted_i, adjusted_j, adjusted_k, modelview_matrix, proj_matrix, viewport)
                y = height - y  # Flip the y-coordinate because Pygame's origin is at the top-left corner

                # Create a Pygame surface with the label text
                label = font.render(f'({i}, {j}, {k})', True, (255, 255, 255))

                # Convert the surface to an OpenGL texture
                label_texture = pygame.image.tostring(label, 'RGBA', True)
                label_width = label.get_width()
                label_height = label.get_height()

                # Create a new texture ID and bind the label texture to it
                label_texture_id = glGenTextures(1)
                glBindTexture(GL_TEXTURE_2D, label_texture_id)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
                glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, label_width, label_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, label_texture)

                # Draw the label as a 2D texture at the screen coordinates of the vertex
                glEnable(GL_TEXTURE_2D)
                glLoadIdentity()
                glOrtho(0, width, 0, height, -1, 1)
                glBindTexture(GL_TEXTURE_2D, label_texture_id)
                glColor3f(1, 1, 1)
                glBegin(GL_QUADS)
                glTexCoord(0, 0); glVertex2f(x, y)
                glTexCoord(1, 0); glVertex2f(x + label_width, y)
                glTexCoord(1, 1); glVertex2f(x + label_width, y + label_height)
                glTexCoord(0, 1); glVertex2f(x, y + label_height)
                glEnd()
                glDisable(GL_TEXTURE_2D)

                # Delete the texture now that we're done with it
                glDeleteTextures([label_texture_id])

    glPopMatrix()

    pygame.display.flip()

    angle += 0.03

pygame.quit()
