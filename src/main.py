from window import *
from field import *
from snake import *

def main():
	window = Window()

	field = Field(16, 16)
	snake = Snake(field)

	snake.draw_on(field)

	while window.is_running():
		window.poll_events()
		window.begin_frame()

		if imgui.begin_main_menu_bar():
			if imgui.begin_menu("File", True):

				clicked_quit, selected_quit = imgui.menu_item(
					"Quit", 'Cmd+Q', False, True
				)

				if clicked_quit:
					exit(1)

				imgui.end_menu()
			imgui.end_main_menu_bar()

		imgui.begin('custom window')
		
		boundings = ChildWindowBoundings()

		cell_size = 20

		for x in field.get_width_range():
			for y in field.get_height_range():
				color = field.get_color_of(x, y).components
				imgui.get_window_draw_list().add_rect_filled(
					boundings.min.x + cell_size * x, 		boundings.min.y + cell_size * y,
					boundings.min.x + cell_size * (x + 1), 	boundings.min.y + cell_size * (y + 1),
					imgui.get_color_u32_rgba(color[0], color[1], color[2], color[3])
				)

		imgui.end()

		imgui.show_test_window()

		glClearColor(0, 0, 0, 1)
		glClear(GL_COLOR_BUFFER_BIT)
		imgui.render()

		window.end_frame()

if __name__ == "__main__":
	main()