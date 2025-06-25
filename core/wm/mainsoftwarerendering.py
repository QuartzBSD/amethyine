import sdl2
import sdl2.ext
import sdl2.sdlttf


sdl2.sdlttf.TTF_Init()
fonts_path = sdl2.ext.Resources(__file__, "../../resources/fonts")

satoshi = sdl2.sdlttf.TTF_OpenFont(fonts_path.get_path("Satoshi-Regular.ttf").encode("utf-8"), 20)
satoshimedium = sdl2.sdlttf.TTF_OpenFont(fonts_path.get_path("Satoshi-Medium.ttf").encode("utf-8"), 17)


# Initilize Crucial Variables
factory = None
window = None
composited_windows = None

windows = [] # For open applications, not SDL2
dragging = False
dragged_window_index = None
drag_start_mouse_pos = (0, 0)
drag_start_window_pos = (0, 0)


class wm:
	def init(factory_arg, window_arg):
		global factory, window, composited_windows
		factory = factory_arg
		window = window_arg
		composited_windows = factory.create_sprite(size=(window.size), bpp=32)
		sdl2.SDL_SetSurfaceBlendMode(composited_windows.surface, sdl2.SDL_BLENDMODE_BLEND)

		# self.windows = [] # For open applications, not SDL2
		# self.dragging = False
		# self.dragged_window_index = None
		# self.drag_start_mouse_pos = (0, 0)
		# self.drag_start_window_pos = (0, 0)

	def create_window(name, data=None):
		if data == None:
			data = { 
				"x": 0,
				"y": 0
			}
		# Window Creation
		window_sprite = factory.create_sprite(size=(400, 400), bpp=32)
		# sdl2.ext.fill(window, (255, 255, 255, 50))

		window_title_background = factory.create_sprite(size=(400, 37)) # debug
		sdl2.ext.fill(window_title_background, (200, 200, 200))

		sdl2.SDL_SetSurfaceBlendMode(window_sprite.surface, sdl2.SDL_BLENDMODE_BLEND)

		sdl2.SDL_FillRect(window_sprite.surface, None, sdl2.SDL_MapRGBA(window_sprite.surface.format, 255, 255, 255, 128))


		window_title = sdl2.sdlttf.TTF_RenderUTF8_Blended(satoshimedium, name.encode("utf-8"),
			sdl2.SDL_Color(0, 0, 0, 255)
		)

		sdl2.surface.SDL_BlitSurface(window_title_background.surface, None, window_sprite.surface, sdl2.SDL_Rect(0, 0, 0, 0))

		sdl2.surface.SDL_BlitSurface(window_title, None, window_sprite.surface, sdl2.SDL_Rect(15, 7, 0, 0))

		sdl2.surface.SDL_BlitSurface(window_sprite.surface, None, composited_windows.surface, sdl2.SDL_Rect(0, 0, 0, 0))

		windows.append((window_sprite, (data['x'], data['y'])))
		return window

	def fetch_window_display():
		sdl2.SDL_FillRect(composited_windows.surface, None, 0)
		for window_sprite, (x, y) in windows:
			sdl2.surface.SDL_BlitSurface(window_sprite.surface, None, composited_windows.surface, sdl2.SDL_Rect(x, y, 0, 0))
		return composited_windows

	def handle_event(event):
		# global dragging, dragged_window_index, drag_start_mouse_pos, drag_start_window_pos
		global dragging, dragged_window_index

		if event.type == sdl2.SDL_MOUSEBUTTONDOWN:
			button = event.button.button
			x = event.button.x
			y = event.button.y

			if button == sdl2.SDL_BUTTON_LEFT:
				mouse_x = event.button.x
				mouse_y = event.button.y
				for i, (window_sprite, (window_x, window_y)) in enumerate(windows):
					width = window_sprite.size[0]
					height = window_sprite.size[1]
					if window_x <= mouse_x <= window_x + width and window_y <= mouse_y <= window_y + height - (height - 37):
						# print('hai - jp yes')
						dragging = True
						dragged_window_index = i
						# drag_start_mouse_pos = (mouse_x, mouse_y)
						# drag_start_window_pos = (window_x, window_y)
						break;

		elif event.type == sdl2.SDL_MOUSEBUTTONUP:
			if event.button.button == sdl2.SDL_BUTTON_LEFT and dragging:
				dragging = False
				dragged_window_index = None

		elif event.type == sdl2.SDL_MOUSEMOTION and dragging:
			mouse_x = event.motion.x
			mouse_y = event.motion.y
			# print(mouse_x, mouse_y)

			# drag_x = mouse_x - drag_start_mouse_pos[0]
			# drag_y = mouse_y - drag_start_mouse_pos[1]
				# print(mouse_x)
			windows[dragged_window_index] = (windows[dragged_window_index][0], (mouse_x, mouse_y))
			print(windows[dragged_window_index])

			# if dragged_window_index is not None:
			# 	old_position = windows[dragged_window_index][1]
			# 	new_position = (dragged_window_index[0] + drag_x, drag_start_window_pos[1] + drag_y)
			# 	print(new_position)
			# 	windows[dragged_window_index] = (windows[dragged_window_index][0], new_position)


