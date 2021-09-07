import glfw
import imgui

from imgui.integrations.glfw 	import GlfwRenderer
from OpenGL.GL 					import *
from enum 						import Enum

class ChildWindowBoundings:
	def __init__(self):
		self.min = imgui.get_window_content_region_min()
		self.max = imgui.get_window_content_region_max()
		self.min = imgui.Vec2(self.min.x + imgui.get_window_position().x, self.min.y + imgui.get_window_position().y)
		self.max = imgui.Vec2(self.max.x + imgui.get_window_position().x, self.max.y + imgui.get_window_position().y)		

class Input:
	states = {}

	class State(Enum):
		Idle = -1
		Pressed = glfw.PRESS
		Released = glfw.RELEASE

	@staticmethod
	def clear():
		Input.states.clear()

	@staticmethod
	def key_callback(handle, key, scancode, action, mods):
		if action != glfw.PRESS and action != glfw.RELEASE: action = -1
		Input.states[key] = Input.State(action)

	@staticmethod
	def key_is(key, state):
		if key not in Input.states: 
			return state == Input.State.Idle

		return Input.states[key] == state

class Time:
	last_time = 0
	current_time = 0
	delta_time = 0
	timers = {}

	@staticmethod
	def timer(every, id):
		ready = False
		if id in Time.timers:
			if Time.timers[id] >= every:
				Time.timers[id] = 0
				ready = True
		else:
			Time.timers[id] = 0

		Time.timers[id] += Time.delta_time

		return ready

	@staticmethod
	def measure():
		Time.current_time = glfw.get_time()
		Time.delta_time = Time.current_time - Time.last_time
		Time.last_time = Time.current_time

	@staticmethod
	def get_fps():
		return 1.0 / Time.delta_time

window_initialized = False

class Window:
	def __init__(self):
		imgui.create_context()
		width, height = 1280, 720
		window_name = "minimal ImGui/GLFW3 example"

		if not glfw.init():
			print("Could not initialize OpenGL context")
			exit(1)

		glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
		glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
		glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
		glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, glfw.TRUE)

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

		glfw.set_key_callback(self.handle, Input.key_callback)

		global window_initialized
		window_initialized = True

	def is_running(self):
		return not glfw.window_should_close(self.handle)

	def poll_events(self):
		glfw.poll_events()
		self.impl.process_inputs()

	def begin_frame(self):
		self.poll_events()
		Time.measure()
		imgui.new_frame()

	def end_frame(self):
		self.impl.render(imgui.get_draw_data())
		glfw.swap_buffers(self.handle)		
		Input.clear()

	def loop(self, callback):
		while self.is_running():
			self.begin_frame()
			callback()
			self.end_frame()

	def __del__(self):
		self.impl.shutdown()
		glfw.terminate()

if not window_initialized:
	window = Window()