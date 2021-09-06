import glfw
import imgui

from OpenGL.GL import *
from imgui.integrations.glfw import GlfwRenderer

class ChildWindowBoundings:
	def __init__(self):
		self.min = imgui.get_window_content_region_min()
		self.max = imgui.get_window_content_region_max()
		self.min = imgui.Vec2(self.min.x + imgui.get_window_position().x, self.min.y + imgui.get_window_position().y)
		self.max = imgui.Vec2(self.max.x + imgui.get_window_position().x, self.max.y + imgui.get_window_position().y)		

class Window:
	def __init__(self):
		imgui.create_context()
		width, height = 1280, 720
		window_name = "minimal ImGui/GLFW3 example"

		if not glfw.init():
			print("Could not initialize OpenGL context")
			exit(1)

		# OS X supports only forward-compatible core profiles from 3.2
		glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
		glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
		glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

		glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)

		# Create a windowed mode window and its OpenGL context
		self.handle = glfw.create_window(
			int(width), int(height), window_name, None, None
		)
		glfw.make_context_current(self.handle)
		glfw.maximize_window(self.handle)
		glfw.swap_interval(0)

		if not self.handle:
			glfw.terminate()
			print("Could not initialize Window")
			exit(1)

		self.impl = GlfwRenderer(self.handle)

	def is_running(self):
		return not glfw.window_should_close(self.handle)

	def poll_events(self):
		glfw.poll_events()
		self.impl.process_inputs()

	def begin_frame(self):
		imgui.new_frame()

	def end_frame(self):
		self.impl.render(imgui.get_draw_data())
		glfw.swap_buffers(self.handle)

	def __del__(self):
		self.impl.shutdown()
		glfw.terminate()
