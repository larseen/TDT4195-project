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
pieces = [ [142.6052,216.9133, 34.5539, 1,0,0] ]
gamePieces = []
SELECTEDPIECE = None

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
		self.rad = rad
		self.x = .4
		self.y = -3.9
		self.z = -4
		self.selected = False

	def select(self):
		self.selected = True

	def deselect(self):
		self.selected = False

	def inMe(self,x,y):
		if((x-self.x)**2 + (y-self.y)**2 < self.rad**2):
			return True
		else:
			return False

	def movePiece(self, newX, newY):
		self.x = newX
		self.y = newY

	def draw(self):	
		glPushMatrix()
		if(self.selected):
			glColor3f(0, 1.0, 0)
		else:
			glColor3f(0.0, 0.0, 0.0)

		glTranslatef(self.x, self.y, self.z)
		glTranslatef(0.0, 5.0, -1.0)
		glScalef(1.0, 1.0, 2.0)
		quadratic = gluNewQuadric()
		gluDisk(quadratic,0,.35,32,32)
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
	draw()


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
	global SELECTEDPIECE
	if (ch == chr(27)) :
		sys.exit(0)
	if(SELECTEDPIECE is not None):
		if(ch == 'w'):
			SELECTEDPIECE.y += 0.05
		if(ch == 's'):
			SELECTEDPIECE.y -= 0.05
		if(ch == 'd'):
			SELECTEDPIECE.x += 0.05
		if(ch == 'a'):
			SELECTEDPIECE.x -= 0.05
	else:
		return
	draw()

def findPiece(x,y):
	for i in range(len(gamePieces)):
		if(gamePieces[i].inMe(x,y)):
			gamePieces[i].select()
			return gamePieces[i]

def mouse(button, state,  x,  y):
	global SELECTEDPIECE
	if(button == 0 and state == 1):
		piece = findPiece(x,y)
		if(piece is not None):
			SELECTEDPIECE = piece
	if(button == 2 and state == 1):
		SELECTEDPIECE.deselect()
		SELECTEDPIECE = None
	draw()


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
	glutMouseFunc(mouse)

	# setup OpenGL state
	glClearColor(1.0, 1.0, 1.0, 0.0)
	glMatrixMode(GL_PROJECTION)
	glFrustum(-1.0, 1.0, -1.0, 1.0, 1.0, 10)
	# add three initial random planes
	# start event processing */
	#Create the board
	makeBoard()
	for i in range(len(pieces)):
		gamePieces.append(gamePiece(pieces[i][0],pieces[i][1],pieces[i][2],pieces[i][3],pieces[i][4],pieces[i][5]))
	glutMainLoop()
