from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import sqrt

G_OBJ_PLANE = 1
G_OBJ_SPHERE = 2
G_OBJ_CUBE = 3
G_OBJ_CYLINDER = 4
G_OBJ_TETRAHEDRON = 5

def make_plane():
	glNewList(G_OBJ_PLANE, GL_COMPILE)
	glLineWidth(0.5)
	glBegin(GL_LINES)
	glColor4f(1, 1, 0.7, 0.0)
	for i in xrange(29):
		glVertex3f(-7.0 + 0.5 * i, 0, -7)
		glVertex3f(-7.0 + 0.5 * i, 0, 7)
		glVertex3f(-7.0, 0, -7 + 0.5 * i)
		glVertex3f(7.0, 0, -7 + 0.5 * i)
	for j in xrange(29):
		glVertex3f(-7.0 + 0.5 * j, -7, 0)
		glVertex3f(-7.0 + 0.5 * j, 7, 0)
		glVertex3f(-7.0, -7 + 0.5 * j, 0)
		glVertex3f(7.0, -7 + 0.5 * j, 0)
	for k in xrange(29):
		glVertex3f(0, -7.0 + 0.5 * k, -7)
		glVertex3f(0, -7.0 + 0.5 * k, 7)
		glVertex3f(0, -7.0, -7 + 0.5 * k)
		glVertex3f(0, 7.0, -7 + 0.5 * k)

	# Axes
	glEnd()
	
	glLineWidth(5)

	glBegin(GL_LINES)
	glColor3f(0.5, 0.9, 1.0)
	glVertex3f(0.0, 0.0, 0.0)
	glVertex3f(7, 0.0, 0.0)
	glEnd()

	glBegin(GL_LINES)
	glColor3f(0.5, 0.9, 1.0)
	glVertex3f(0.0, 0.0, 0.0)
	glVertex3f(0.0, 7, 0.0)
	glEnd()

	glBegin(GL_LINES)
	glColor3f(0.5, 0.9, 1.0)
	glVertex3f(0.0, 0.0, 0.0)
	glVertex3f(0.0, 0.0, 7)
	glEnd()

	glLineWidth(5)
	
	# Draw the Y.
	glBegin(GL_LINES)
	glColor3f(0.0, 0.0, 0.0)
	glVertex3f(0.0, 7.5, 0.0)
	glVertex3f(0.0, 8.0, 0.0)
	glVertex3f(0.0, 8.0, 0.0)
	glVertex3f(-0.5, 8.5, 0.0)
	glVertex3f(0.0, 8.0, 0.0)
	glVertex3f(0.5, 8.5, 0.0)

	# Draw the Z.
	glVertex3f(-0.5, 0.0, 7.5)
	glVertex3f(0.5, 0.0, 7.5)
	glVertex3f(0.5, 0.0, 7.5)
	glVertex3f(-0.5, 0.0, 8.5)
	glVertex3f(-0.5, 0.0, 8.5)
	glVertex3f(0.5, 0.0, 8.5)

	# Draw the X.
	glVertex3f(7.5, 0.0, 0.5)
	glVertex3f(8.5, 0.0, -0.5)
	glVertex3f(7.5, 0.0, -0.5)
	glVertex3f(8.5, 0.0, 0.5)

	glEnd()
	glLineWidth(1)
	glEndList()

def make_sphere():
	glNewList(G_OBJ_SPHERE, GL_COMPILE)
	quad = gluNewQuadric()
	gluSphere(quad, 0.5, 30, 30)
	gluDeleteQuadric(quad)
	glEndList()
	
def make_cube():
	glNewList(G_OBJ_CUBE, GL_COMPILE)
	vertices = [((-0.5, -0.5, -0.5), (-0.5, -0.5, 0.5), (-0.5, 0.5, 0.5), (-0.5, 0.5, -0.5)),
				((-0.5, -0.5, -0.5), (-0.5, 0.5, -0.5), (0.5, 0.5, -0.5), (0.5, -0.5, -0.5)),
				((0.5, -0.5, -0.5), (0.5, 0.5, -0.5), (0.5, 0.5, 0.5), (0.5, -0.5, 0.5)),
				((-0.5, -0.5, 0.5), (0.5, -0.5, 0.5), (0.5, 0.5, 0.5), (-0.5, 0.5, 0.5)),
				((-0.5, -0.5, 0.5), (-0.5, -0.5, -0.5), (0.5, -0.5, -0.5), (0.5, -0.5, 0.5)),
				((-0.5, 0.5, -0.5), (-0.5, 0.5, 0.5), (0.5, 0.5, 0.5), (0.5, 0.5, -0.5))]
	normals = [(-1.0, 0.0, 0.0), (0.0, 0.0, -1.0), (1.0, 0.0, 0.0), (0.0, 0.0, 1.0), (0.0, -1.0, 0.0), (0.0, 1.0, 0.0)]

	glBegin(GL_QUADS)
	for i in xrange(6):
		glNormal3f(normals[i][0], normals[i][1], normals[i][2])
		for j in xrange(4):
			glVertex3f(vertices[i][j][0], vertices[i][j][1], vertices[i][j][2])
	glEnd()
	glEndList()

def make_cylinder():
	glNewList(G_OBJ_CYLINDER, GL_COMPILE)
	quad_c = gluNewQuadric()
	gluCylinder(quad_c, 0.5, 0.5, 1.5, 30, 30)
	gluDisk(quad_c, 0, 0.5, 30, 30)
	gluDeleteQuadric(quad_c)
	glEndList()	
	
def make_tetrahedron():
	glNewList(G_OBJ_TETRAHEDRON, GL_COMPILE)
	glutSolidTetrahedron()
	glEndList()

def init_primitives():
	make_plane()
	make_sphere()
	make_cube()
	make_cylinder()
	make_tetrahedron()
	
def init_primitives_nogrid():
	#make_plane()
	make_sphere()
	make_cube()
	make_cylinder()
	make_tetrahedron()