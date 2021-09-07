from window import *
from field import *
from snake import *

def render_field(field: Field, cell_size = 20):
	boundings = ChildWindowBoundings()
	for x in field.get_width_range():
		for y in field.get_height_range():
			color = field.get_color_of(x, y).components
			imgui.get_window_draw_list().add_rect_filled(
				boundings.min.x + cell_size * x + x, 		boundings.min.y + cell_size * y + y,
				boundings.min.x + cell_size * (x + 1) + x, 	boundings.min.y + cell_size * (y + 1) + y,
				imgui.get_color_u32_rgba(color[0], color[1], color[2], color[3])
			)

field = Field(16, 16)
snake = Snake(field)

def loop():
	imgui.set_next_window_size(500, 500)
	imgui.begin('custom window')		

	snake.control()

	if Time.timer(0.2, 'Update snakes'):
		field.clear()
		snake.update(field)
		snake.draw_on(field)

	render_field(field)

	imgui.end()

	imgui.show_test_window()

	glClearColor(0, 0, 0, 1)
	glClear(GL_COLOR_BUFFER_BIT)
	imgui.render()

def main():
	window.loop(loop)

if __name__ == "__main__":
	main()