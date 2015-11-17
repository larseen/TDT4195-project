import sys

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from math import *
from random import random, choice, randint, getrandbits

M_PI   = pi
M_PI_2 = pi / 2.0

moving = False
B = 8 #bredth
H = 5 #length
HEIGHT = 800
WIDTH = 1200
pieces = [ [537.0515,355.2442, 34.5539, 1,1,1],[142.6052,216.9133, 34.5539,1,0,0] ]
gamePieces = []

# define plane object
class square(object):
	def __init__(self, red, green, blue, x, y, z):
		self.red   = red
		self.green = green
		self.blue  = blue
		self.x = x
		self.y = y
		self.z = -6
		self.w = 100
		self.h = 100
	def draw(self):

		glPushMatrix()
		print self.x, self.y
		glTranslatef(self.x, self.y, self.z)
		glScalef( 0.5, 0.5, 0.1)


		#Top
		glBegin(GL_QUADS)
		glColor3f(self.red, self.green, self.blue)
		glVertex3f( 1.0, 1.0,-1.0)
		glVertex3f(-1.0, 1.0,-1.0)
		glVertex3f(-1.0, 1.0, 1.0)
		glVertex3f( 1.0, 1.0, 1.0) 

		glVertex3f( 1.0,-1.0, 1.0)
		glVertex3f(-1.0,-1.0, 1.0)
		glVertex3f(-1.0,-1.0,-1.0)
		glVertex3f( 1.0,-1.0,-1.0) 

		glVertex3f( 1.0, 1.0, 1.0)
		glVertex3f(-1.0, 1.0, 1.0)
		glVertex3f(-1.0,-1.0, 1.0)
		glVertex3f( 1.0,-1.0, 1.0)

		glVertex3f( 1.0,-1.0,-1.0)
		glVertex3f(-1.0,-1.0,-1.0)
		glVertex3f(-1.0, 1.0,-1.0)
		glVertex3f( 1.0, 1.0,-1.0)

		glVertex3f(-1.0, 1.0, 1.0) 
		glVertex3f(-1.0, 1.0,-1.0)
		glVertex3f(-1.0,-1.0,-1.0) 
		glVertex3f(-1.0,-1.0, 1.0) 

		glVertex3f( 1.0, 1.0,-1.0) 
		glVertex3f( 1.0, 1.0, 1.0)
		glVertex3f( 1.0,-1.0, 1.0)
		glVertex3f( 1.0,-1.0,-1.0)
		glEnd()
		glPopMatrix()


# define a game piece
class gamePiece(object):
	def __init__(self, x,y,rad,r,g,b):
		self.red   = r
		self.green = g
		self.blue  = b
		self.x = .4
		self.y = -3.9
		self.z = -4
		self.selected = False

	def selectPiece(self):
		self.selected = True

	def movePiece(self, newX, newY):
		self.x = newX
		self.y = newY

	def draw(self):
		glPushMatrix()
		glTranslatef(self.x, self.y, self.z)
		glTranslatef(0.0, 5.0, -1.0)
		glScalef(1.0, 1.0, 2.0)
		glColor3f(0, 1.0, 0)
		quadratic = gluNewQuadric()
		gluDisk(quadratic,0,.5,32,32)
		glPopMatrix()

# create list of planes
#
board = [[(square(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)) for x in range(B)] for y in range(H)]

# Inits the board tiles, with posistion and color.
def makeBoard():
	y = 0
	odd = False
	for i in range(H):
		odd = not(odd)
		x = -int(B/2)

		for j in range(B):
			print x,y
			board[i][j].x = x
			board[i][j].y = y
			if (x + int(odd)) % 2  == 0:
				board[i][j].blue = 1.0
			else:
				board[i][j].red = 1.0
			x += 1

		y -= 1


#
# define the GLUT display function
#
def draw():
	glViewport(0, 0, WIDTH, HEIGHT)
	glClear(GL_DEPTH_BUFFER_BIT)
	glShadeModel(GL_SMOOTH)
	# paint planes
	glClear( GL_COLOR_BUFFER_BIT )
	glEnable(GL_DEPTH_TEST)
	glShadeModel(GL_FLAT)

	for i in range(H):
		for j in range(B):
			board[i][j].draw()
	for i in range(len(gamePieces)):
		gamePieces[i].draw()
		
	glutSwapBuffers()
	return

#define choice of planes to animate
def resize(w,h):
	HEIGHT = h
	WIDTH = w


#define choice of planes to animate
def tick():
	for i in range(MAX_PLANES) :
		if (planes[i].speed != 0.0) :
			tick_per_plane(i)
	return

# define animator so that motion can be started
def animate():
	tick()
	glutPostRedisplay()
	return


def visible(state):
	if (state == GLUT_VISIBLE) :
		if (moving) :
			glutIdleFunc(animate)
	else :
		if (moving) :
			glutIdleFunc(None)
	return


# ARGSUSED1

def keyboard( ch,  x,  y):
	if(ch == ' ') :
		if (not moving) :
			tick()
			glutPostRedisplay()
	elif (ch == chr(27)) :
		sys.exit(0)
	return 0

VOID, ADD_PLANE, MOTION_ON, MOTION_OFF, QUIT = range(5)

def domotion_on():
	moving = GL_TRUE
	glutChangeToMenuEntry(3, "Motion off", MOTION_OFF)
	glutIdleFunc(animate)
	return

def domotion_off():
	moving = GL_FALSE
	glutChangeToMenuEntry(3, "Motion", MOTION_ON)
	glutIdleFunc(None)
	return

def doquit():
	sys.exit(0)
	return


menudict ={QUIT : doquit}
def dmenu(item):
	menudict[item]()
	return 0

if __name__ == "__main__":
	glutInit(['glutplane'])
	glutInitWindowPosition(112, 84)
	glutInitWindowSize(WIDTH, HEIGHT)

	# use multisampling if available
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH | GLUT_MULTISAMPLE)
	wintitle = "TDT4195 - Project"
	glutCreateWindow(wintitle)
	glutDisplayFunc(draw)
	glutKeyboardFunc(keyboard)
	glutVisibilityFunc(visible)
	glutReshapeFunc(resize)

	#
	# RIGHT-CLICK to display the menu
	#
	glutCreateMenu(dmenu)
	glutAddMenuEntry("Quit", QUIT)
	glutAttachMenu(GLUT_RIGHT_BUTTON)

	# setup OpenGL state
	glClearDepth(1.0)
	glClearColor(1.0, 1.0, 1.0, 0.0)
	glMatrixMode(GL_PROJECTION)
	glFrustum(-1.0, 1.0, -1.0, 1.0, 1.0, 30)
	glMatrixMode(GL_MODELVIEW)
	# add three initial random planes
	# start event processing */
	#Create the board
	makeBoard()
	for i in range(len(pieces)):
		gamePieces.append(gamePiece(pieces[i][0],pieces[i][1],pieces[i][2],pieces[i][3],pieces[i][4],pieces[i][5]))
	glutMainLoop()
