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
#The pices to be places. [x,y,rad,r,g,b]
pieces = [
	[537.051523513223,355.244173597710,34.5538710367623,111,1,10],
	[142.605224091665,216.913254859790,36.4234107772852,214,198,183],
	[242.172979113019,252.830271177577,36.7846671150205,212,194,180],
	[541.526026882741,152.001818337356,35.9156207592183,201,185,170],
	[347.794065497258,242.810807547300,34.7768420203598,138,2,17]
]
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
		glScalef( 0.5, 0.5, 0.2)


		#Top
		glBegin(GL_QUADS)
		glColor3f(self.red*0.7, self.green*0.7, self.blue*0.7)
		glVertex3f( 1.0, 1.0,-1.0)
		glVertex3f(-1.0, 1.0,-1.0)
		glVertex3f(-1.0, 1.0, 1.0)
		glVertex3f( 1.0, 1.0, 1.0) 
		
		
		glVertex3f( 1.0,-1.0, 1.0)
		glVertex3f(-1.0,-1.0, 1.0)
		glVertex3f(-1.0,-1.0,-1.0)
		glVertex3f( 1.0,-1.0,-1.0) 

		glColor3f(self.red, self.green, self.blue)
		glVertex3f( 1.0, 1.0, 1.0)
		glVertex3f(-1.0, 1.0, 1.0)
		glVertex3f(-1.0,-1.0, 1.0)
		glVertex3f( 1.0,-1.0, 1.0)

		glColor3f(self.red*0.7, self.green*0.7, self.blue*0.7)
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
		self.rad = rad/100
		self.x = (x)/120 + 0.2
		self.y = -(y)/120 -1.4
		self.z = -5
		self.selected = False
		print self.x, x, self.y, y



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
			glColor3f(float(self.red)/355, float(self.green)/355, float(self.blue)/355)
		else:
			glColor3f(float(self.red)/255, float(self.green)/255, float(self.blue)/255)

		glTranslatef(self.x, self.y, self.z)
		glScalef(1.0, 1.0, 2.0)
		quadratic = gluNewQuadric()
		gluDisk(quadratic,0,.34,32,32)
		gluCylinder(quadratic,.34,.34,0.1,200,200)
		glPopMatrix()

# create list of planes
#
board = [[(square(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)) for x in range(B)] for y in range(H)]

# Inits the board tiles, with posistion and color.
def makeBoard():
	y = 0
	odd = True
	for i in range(H):
		odd = not(odd)
		for j in range(B):
			board[i][j].x = j
			board[i][j].y = y
			if (j + int(odd)) % 2  == 0:
				board[i][j].blue = 1.0
			else:
				board[i][j].red = 1.0
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
	transformedX = (x)/120
	transformedY = -(y)/120
	print transformedX, transformedY
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
	glFrustum(-1.0, 1.0, -1.0, 1.0, 1.2, 50)
	model = glGetDoublev(GL_MODELVIEW_MATRIX)
	glMatrixMode(GL_MODELVIEW)
	glRotatef(-90.0, 0.0, 0.0, 0.0)
	glTranslatef(-3.5, 11.2, 1.0)
	# add three initial random planes
	# start event processing */
	#Create the board
	makeBoard()
	for i in range(len(pieces)):
		gamePieces.append(gamePiece(pieces[i][0],pieces[i][1],pieces[i][2],pieces[i][3],pieces[i][4],pieces[i][5]))
	print len(pieces)
	glutMainLoop()
