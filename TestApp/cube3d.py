import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

verticies = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
    )
edges = (
    (0,1),(0,3),(0,4),
    (2,1),(2,3),(2,7),
    (6,3),(6,4),(6,7),
    (5,1),(5,4),(5,7)
    )
faces = (
    (0,1,2,3),
    (3,2,7,6),
    (6,7,5,4),
    (4,5,1,0),
    (1,5,7,2),
    (4,0,3,6)
    )
colors = (
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (1,1,0),
    (1,1,1),
    (0,1,1),
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (1,1,0),
    (1,1,1),
    (0,1,1)
    )
dims = (2000,2000)
center = (dims[0]/2, dims[1]/2)

#Vector operations
def distance(p1, p2):
    return ((p1[0]-p2[0])**2+(p1[0]-p2[0])**2)**0.5

def displacement(p1, p2):
    return (p1[0]-p2[0], p1[1]-p2[1])

def unit_vec(p1):
    return (p1[0]/distance(p1,(0,0)), p1[1]/distance(p1,(0,0)))

def scale(p1, a):
    return (p1[0]*a, p1[1]*a)

#function mycube renders the cube onscreen
def mycube():

    #render cube faces
    glBegin(GL_QUADS)

    for face in faces:
        x = 0
        for vertex in face:
            x+=1
            glColor3fv(colors[x])
            glVertex3fv(verticies[vertex])
    glEnd()

    #render cube edges
    glBegin(GL_LINES)

    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])

    glEnd()


def main():
    #configure pygame
    pygame.init()
    display = dims
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    #confugure opengl
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslate(0.0,0.0, -5)
    glRotatef(0, 0, 0, 0)

    #pygame mainloop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:

                pygame.quit()
                quit()
        #get mouse location relative to center (=mvec)
        mp = pygame.mouse.get_pos()
        mvec = scale(displacement(mp, center),1/500)

        #rotate on x and y axis
        glRotatef(2*mvec[0], 1, 0, 0)
        glRotatef(2*mvec[1], 0, 1, 0)
        #render graphics
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        mycube()
        pygame.display.flip()
        #delay
        pygame.time.wait(10)

main()
