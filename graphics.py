import sys

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from math import *
from random import random, choice, randint, getrandbits



### DATA GENERATED FROM MATLAB

boardColurs = [[210,79,66],[74,110,145]]

pieces = [
	[140.575579012684,330.585020962471,36.1654768404031,246,239,220],
	[548.834948975566,238.044696946200,35.7943337765257,238,229,212],
	[237.248082927155,140.100965293905,35.2164543487218,156,11,23],
	[428.783860704430,135.137817610981,35.2823678533650,217,212,193],
	[352.412787048160,244.258137126295,35.9556412541358,164,7,26]
]

### GLOBALS

gamePieces = []
SELECTEDPIECE = None
B = 8 #bredth
H = 5 #length
HEIGHT = 800
WIDTH = 1200

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
		glColor3f(float(self.red)/255*0.7, float(self.green)/255*0.7, float(self.blue)/255*0.7)
		glVertex3f( 1.0, 1.0,-1.0)
		glVertex3f(-1.0, 1.0,-1.0)
		glVertex3f(-1.0, 1.0, 1.0)
		glVertex3f( 1.0, 1.0, 1.0) 
		
		
		glVertex3f( 1.0,-1.0, 1.0)
		glVertex3f(-1.0,-1.0, 1.0)
		glVertex3f(-1.0,-1.0,-1.0)
		glVertex3f( 1.0,-1.0,-1.0) 

		glColor3f(float(self.red)/255, float(self.green)/255, float(self.blue)/255)
		glVertex3f( 1.0, 1.0, 1.0)
		glVertex3f(-1.0, 1.0, 1.0)
		glVertex3f(-1.0,-1.0, 1.0)
		glVertex3f( 1.0,-1.0, 1.0)

		glColor3f(float(self.red)/255*0.7, float(self.green)/255*0.7, float(self.blue)/255*0.7)
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
		gluDisk(quadratic,0,self.rad,32,32)
		gluCylinder(quadratic,self.rad,self.rad,0.1,200,200)
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
				board[i][j].red = boardColurs[0][0]
				board[i][j].green = boardColurs[0][1]
				board[i][j].blue = boardColurs[0][2]
			else:
				board[i][j].red = boardColurs[1][0]
				board[i][j].green = boardColurs[1][1]
				board[i][j].blue = boardColurs[1][2]
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
	# CREATE PIECES
	makeBoard()
	# CREATE PIECES
	for i in range(len(pieces)):
		gamePieces.append(gamePiece(pieces[i][0],pieces[i][1],pieces[i][2],pieces[i][3],pieces[i][4],pieces[i][5]))
	print len(pieces)
	glutMainLoop()
