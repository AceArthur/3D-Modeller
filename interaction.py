from collections import defaultdict
from OpenGL.GLUT import *
import trackball
import sys


class Interaction(object):
	def __init__(self):
		self.pressed = None
		self.translation = [0, 0, 0, 0]
		self.trackball = trackball.Trackball(theta = -25, distance=15)
		self.mouse_loc = None
		self.callbacks = defaultdict(list)

		self.register()

	def register(self):
		glutMouseFunc(self.handle_mouse_button)
		glutMotionFunc(self.handle_mouse_move)
		glutKeyboardFunc(self.handle_keystroke)
		glutSpecialFunc(self.handle_keystroke)
		
	def handle_mouse_button(self, button, mode, x, y):
		xSize, ySize = glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT)
		y = ySize - y  
		self.mouse_loc = (x, y)

		if mode == GLUT_DOWN:
			self.pressed = button
			if button == GLUT_RIGHT_BUTTON:
				pass
			elif button == GLUT_LEFT_BUTTON:  
				self.trigger('pick', x, y)
			elif button == 3:  # scroll up
				self.translate(0, 0, 1.0)
			elif button == 4:  # scroll down
				self.translate(0, 0, -1.0)
		else:  
			self.pressed = None
		glutPostRedisplay()
		
	def handle_mouse_move(self, x, screen_y):
		xSize, ySize = glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT)
		y = ySize - screen_y 
		if self.pressed is not None:
			dx = x - self.mouse_loc[0]
			dy = y - self.mouse_loc[1]
			if self.pressed == GLUT_RIGHT_BUTTON and self.trackball is not None:
				self.trackball.drag_to(self.mouse_loc[0], self.mouse_loc[1], dx, dy)
			elif self.pressed == GLUT_LEFT_BUTTON:
				self.trigger('move', x, y)
			elif self.pressed == GLUT_MIDDLE_BUTTON:
				self.translate(dx/60.0, dy/60.0, 0)
			else:
				pass
			glutPostRedisplay()
		self.mouse_loc = (x, y)

	def handle_keystroke(self, key, x, screen_y):
		xSize, ySize = glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT)
		y = ySize - screen_y
		if key == 'q':
			self.trigger('close')
		elif key == 'r':
			self.trigger('reset')
		elif key == 'n':
			self.trigger('nogrid', grid=False)
		elif key == 'g':
			self.trigger('nogrid', grid=True)
		elif key == 's':
			self.trigger('place', 'sphere', x, y)
		elif key == 'c':
			self.trigger('place', 'cube', x, y)
		elif key == 'y':
			self.trigger('place', 'cylinder', x, y)
		elif key == 't':
			self.trigger('place', 'tetrahedron', x, y)
		elif key == GLUT_KEY_UP:
			self.trigger('scale', up=True)
		elif key == GLUT_KEY_DOWN:
			self.trigger('scale', up=False)
		elif key == GLUT_KEY_LEFT:
			self.trigger('rotate_color', forward=True)
		elif key == GLUT_KEY_RIGHT:
			self.trigger('rotate_color', forward=False)
		glutPostRedisplay()
		
	def trigger(self, name, *args, **kwargs):
		for func in self.callbacks[name]:
			func(*args, **kwargs)
			
	def translate(self, x, y, z):
		""" translate the camera """
		self.translation[0] += x
		self.translation[1] += y
		self.translation[2] += z
			
	def register_callback(self, name, func):
		self.callbacks[name].append(func)