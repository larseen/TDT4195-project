import sys
import ctypes
import numpy as np
import OpenGL.GL as gl
import OpenGL.GLUT as glut

vertex_code = """
	uniform flat scale;
	attribute vec4 color;
	attribute vec2 position;
	varying vec4 v_color;
	void main()
	{
		gl_position = vec4(scale*position, 0.0, 1.0);
		v_color = color;
	} """

fragment_code = """
	varying vec4 v_color;
	void main()
	{
		gl_FragColor = v_color;
	}"""


def display():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    gl.glDrawArrays(gl.GL_TRIANGLE_STRIP, 0, 4)
    glut.glutSwapBuffers()

def reshape(width,height):
    gl.glViewport(0, 0, width, height)

def keyboard( key, x, y ):
    if key == '\033':
        sys.exit( )

glut.glutInit()
glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGBA)
glut.glutCreateWindow('Hello world!')
glut.glutReshapeWindow(512,512)
glut.glutReshapeFunc(reshape)
glut.glutDisplayFunc(display)
glut.glutKeyboardFunc(keyboard)

data = np.zeros(4, [ ("position", np.float32, 2),
					 ("color",    np.float32, 4)] )

data['color'] = [(1,0,0,1), (0,1,0,1), (0,0,1,1), (1,1,0,1)]
data['position'] = [(-1,-1), (-1,+1), (+1,-1), (+1,+1)]

#
#BUILD AND ACTIVATE PROGRAM
#
#Request a program and shader slots from GPU
program  = gl.glCreateProgram()
vertex   = gl.glCreateShader(gl.GL_VERTEX_SHADER)
fragment = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)

# Set shaders source
gl.glShaderSource(vertex, vertex_code)
gl.glShaderSource(fragment, fragment_code)

# Compile shaders
gl.glCompileShader(vertex)
gl.glCompileShader(fragment)

#Attach shaders
gl.glAttachShader(program, vertex)
gl.glAttachShader(program, fragment)

#Build program
gl.glLinkProgram(program)

#Detach shaders
gl.glDetachShader(program, vertex)
gl.glDetachShader(program, fragment)

#set program to default program
gl.glUseProgram(program)

#
#BUILT BUFFER
#
# Request a buffer slot from GPU
buffer = gl.glGenBuffers(1)

# Make this buffer the default one
gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)

# Upload data
gl.glBufferData(gl.GL_ARRAY_BUFFER, data.nbytes, data, gl.GL_DYNAMIC_DRAW)

#
#BIND ATTRIBUTES
#
stride = data.strides[0]
offset = ctypes.c_void_p(0)
loc = gl.glGetAttribLocation(program, "position")
gl.glEnableVertexAttribArray(loc)
gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)
gl.glVertexAttribPointer(loc, 3, gl.GL_FLOAT, False, stride, offset)

offset = ctypes.c_void_p(data.dtype["position"].itemsize)
loc = gl.glGetAttribLocation(program, "color")
gl.glEnableVertexAttribArray(loc)
gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)
gl.glVertexAttribPointer(loc, 4, gl.GL_FLOAT, False, stride, offset)

#
#BIND UNIFORMS
#
loc = gl.glGetUniformLocation(program, "scale")
gl.glUniform1f(loc, 1.0)
#
#ENTER MAIN LOOP
#
glut.glutMainLoop()