from OpenGL.GL import *
from OpenGL.constants import GLfloat_3, GLfloat_4
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy
from numpy.linalg import norm, inv
from primitive import *
import color
from scene import *
from node import *
from interaction import Interaction
import sys

class Viewer(object):
	def __init__(self):
		self.init_interface()
		self.init_opengl()
		self.init_scene()
		self.init_interaction()
		init_primitives()
		
	def init_nogrid(self):
		self.init_interface()
		self.init_opengl()
		self.init_scene()
		self.init_interaction()
		init_primitives_nogrid()

	def init_interface(self):
		global winid
		glutInit()
		glutInitWindowSize(640, 480)
		glutInitWindowPosition(100,100)
		winid = glutCreateWindow("3D Modeller")
		glutInitDisplayMode(GLUT_SINGLE|GLUT_RGBA)
		glutDisplayFunc(self.render)

	def init_opengl(self):
		self.inverseModelView = numpy.identity(4)
		self.modelView = numpy.identity(4)

		glEnable(GL_CULL_FACE)
		glCullFace(GL_BACK)
		glEnable(GL_DEPTH_TEST)
		glDepthFunc(GL_LESS)
		glEnable(GL_LIGHT0)

		glLightfv(GL_LIGHT0, GL_POSITION, GLfloat_4(0,0,1,0))
		glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, GLfloat_3(0,0,-1))
		glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
		glEnable(GL_COLOR_MATERIAL)

		glClearColor(0.5, 0.5, 0.5, 0.0)

	def init_scene(self):
		self.scene = Scene()
		self.create_sample_scene()

	def create_sample_scene(self):
		cube_node = Cube()
		cube_node.translate(2, 0, 2)
		cube_node.color_index = 1
		self.scene.add_node(cube_node)

		sphere_node = Sphere()
		sphere_node.color_index = 2
		sphere_node.translate(2,2,0)
		#sphere_node.scale(4)
		self.scene.add_node(sphere_node)
		
		cylinder_node = Cylinder()
		cylinder_node.color_index = 3
		cylinder_node.translate(0,-2,2)
		self.scene.add_node(cylinder_node)
		
		tetrahedron_node = Tetrahedron()
		tetrahedron_node.color_index = 4
		tetrahedron_node.translate(2,-2,-2)
		self.scene.add_node(tetrahedron_node)

		hierarchical_node = SnowFigure()
		hierarchical_node.translate(-2, 0, -2)
		#hierarchical_node.scale(2)
		self.scene.add_node(hierarchical_node)

	def init_interaction(self):
		self.interaction = Interaction()
		self.interaction.register_callback('pick', self.pick)
		self.interaction.register_callback('move', self.move)
		self.interaction.register_callback('place', self.place)
		self.interaction.register_callback('rotate_color', self.rotate_color)
		self.interaction.register_callback('scale', self.scale)
		self.interaction.register_callback('close', self.close)
		self.interaction.register_callback('reset', self.reset)
		self.interaction.register_callback('nogrid', self.nogrid)

	def pick(self, x, y):
		start, direction = self.get_ray(x, y)
		self.scene.pick(start, direction, self.modelView)

	def move(self, x, y):
		start, direction = self.get_ray(x, y)
		self.scene.move_selected(start, direction, self.inverseModelView)

	def place(self, shape, x, y):
		start, direction = self.get_ray(x, y)
		self.scene.place(shape, start, direction, self.inverseModelView)

	def rotate_color(self, forward):
		self.scene.rotate_selected_color(forward)

	def scale(self, up):
		self.scene.scale_selected(up)

	def main_loop(self):
		glutMainLoop()

	def render(self):
		self.init_view()

		glEnable(GL_LIGHTING)
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

		glMatrixMode(GL_MODELVIEW)
		glPushMatrix()
		glLoadIdentity()
		loc = self.interaction.translation
		glTranslated(loc[0], loc[1], loc[2])
		glMultMatrixf(self.interaction.trackball.matrix)

		currentModelView = numpy.array(glGetFloatv(GL_MODELVIEW_MATRIX))
		self.modelView = numpy.transpose(currentModelView)
		self.inverseModelView = inv(numpy.transpose(currentModelView))

		self.scene.render()

		glDisable(GL_LIGHTING)
		glCallList(G_OBJ_PLANE)
		glPopMatrix()

		glFlush()

	def init_view(self):
		xSize, ySize = glutGet(GLUT_WINDOW_WIDTH),glutGet(GLUT_WINDOW_HEIGHT)
		aspect_ratio = float(xSize) / float(ySize)

		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()

		glViewport(0, 0, xSize, ySize)
		gluPerspective(70, aspect_ratio, 0.1, 1000.0)
		glTranslate(0, 0, -15)

	def get_ray(self, x, y):
		self.init_view()

		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()

		start = numpy.array(gluUnProject(x, y, 0.001))
		end = numpy.array(gluUnProject(x, y, 0.999))

		direction = end - start
		direction = direction / norm(direction)

		return (start, direction)

	def close(self):
		global winid
		glutDestroyWindow(winid)
		sys.exit()

	def reset(self):
		self.init_scene()
		
	def nogrid(self, grid):
		global winid
		glutDestroyWindow(winid)
		if grid:
			self.__init__()
		else:
			self.init_nogrid()

if __name__ == "__main__":
	view = Viewer()
	view.main_loop()

