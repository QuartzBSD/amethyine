import sdl2
import sdl2.ext
import sdl2.sdlttf
from sdl2 import sdlgfx
import socket
import os
import json
import threading

sdl2.sdlttf.TTF_Init()
fonts_path = sdl2.ext.Resources(__file__, "../../resources/fonts")

satoshi = sdl2.sdlttf.TTF_OpenFont(fonts_path.get_path("Satoshi-Regular.ttf").encode("utf-8"), 20)
satoshimedium = sdl2.sdlttf.TTF_OpenFont(fonts_path.get_path("Satoshi-Medium.ttf").encode("utf-8"), 17)


# Initilize Crucial Variables
factory = None
window = None
renderer = None
composited_windows = None

windows = [] # For open applications, not SDL2
dragging = False
dragged_window_index = None
# drag_start_mouse_pos = (0, 0)
# drag_start_window_pos = (0, 0)


class wm:
	### Jasmine API Related Variables ###
	server = None
	client = None

	def init(factory_arg, window_arg, renderer_arg):
		global factory, window, renderer, composited_windows
		factory = factory_arg
		window = window_arg
		renderer = renderer_arg
		composited_windows = factory.create_sprite(size=(window.size))
		sdl2.SDL_SetTextureBlendMode(composited_windows.texture, sdl2.SDL_BLENDMODE_BLEND)
		sdl2.SDL_SetRenderDrawBlendMode(renderer, sdl2.SDL_BLENDMODE_BLEND)

		if os.path.exists('/tmp/amethyine-wm-quartz.sock'):
			os.remove('/tmp/amethyine-wm-quartz.sock')

		wm.server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
		wm.server.bind('/tmp/amethyine-wm-quartz.sock')
		wm.server.listen(1)
		wm.server.setblocking(False)
		wm.client = None

		# self.windows = [] # For open applications, not SDL2
		# self.dragging = False
		# self.dragged_window_index = None
		# self.drag_start_mouse_pos = (0, 0)
		# self.drag_start_window_pos = (0, 0)

	def create_window(name, data=None):
		global renderer
		if data == None:
			data = { 
				"x": 0,
				"y": 0
			}
		# Window Creation SF
		# window_sprite = factory.create_sprite(size=(400, 400), bpp=32)
		# sdl2.ext.fill(window, (255, 255, 255, 50))
		# sdl2.SDL_SetSurfaceBlendMode(window_sprite.surface, sdl2.SDL_BLENDMODE_BLEND)
		# sdl2.SDL_FillRect(window_sprite.surface, None, sdl2.SDL_MapRGBA(window_sprite.surface.format, 255, 255, 255, 128))

		# Window Creation HW
		window_surface = sdl2.SDL_CreateRGBSurfaceWithFormat(0, 400, 400, 32, sdl2.SDL_PIXELFORMAT_RGBA32)
		sdl2.SDL_FillRect(window_surface, None, sdl2.SDL_MapRGBA(window_surface.contents.format, 255, 255, 255, 128))

		# Titlebar SF
		# window_title_background = factory.create_sprite(size=(400, 37)) # debug
		# sdl2.ext.fill(window_title_background, (200, 200, 200))

		# Titlebar HW
		titlebar = sdl2.SDL_Rect(0, 0, 400, 37)
		sdl2.SDL_FillRect(window_surface, titlebar, sdl2.SDL_MapRGBA(window_surface.contents.format, 255, 255, 255, 180))

		# Window Title
		window_title_text = sdl2.sdlttf.TTF_RenderUTF8_Blended(satoshimedium, name.encode("utf-8"),
			sdl2.SDL_Color(0, 0, 0, 255)
		)
		window_title_surface = sdl2.SDL_Rect(15, 7, 0, 0)
		sdl2.SDL_BlitSurface(window_title_text, None, window_surface, window_title_surface)

		window_texture = sdl2.SDL_CreateTextureFromSurface(renderer, window_surface)

		sdl2.SDL_FreeSurface(window_surface)
		sdl2.SDL_FreeSurface(window_title_text)

		# sdl2.surface.SDL_BlitSurface(window_title_background.surface, None, window_sprite.surface, sdl2.SDL_Rect(0, 0, 0, 0))
		# sdl2.surface.SDL_BlitSurface(window_title, None, window_sprite.surface, sdl2.SDL_Rect(15, 7, 0, 0))
		# sdl2.surface.SDL_BlitSurface(window_sprite.surface, None, composited_windows.surface, sdl2.SDL_Rect(0, 0, 0, 0))

		final_rect = sdl2.SDL_Rect(data["x"], data["y"], 400, 400)

		# windows.append((window_sprite, (data['x'], data['y'])))
		windows.append((window_texture, final_rect))
		return window

	# def create_window(name, data=None):
	#     global renderer
	#     if data is None:
	#         data = {"x": 100, "y": 100}
	#     x, y = data["x"], data["y"]
	#     w, h = 400, 400
	#     radius = 12

	#     # Draw rounded rectangle to renderer (background)
	#     sdlgfx.roundedBoxRGBA(renderer, x, y, x + w, y + h, radius, 255, 255, 255, 200)  # white bg with alpha
	#     sdlgfx.roundedBoxRGBA(renderer, x, y, x + w, y + 37, radius, 200, 200, 200, 255)  # titlebar

	#     # Now draw text using a surface
	#     window_title_text = sdl2.sdlttf.TTF_RenderUTF8_Blended(satoshimedium, name.encode("utf-8"), sdl2.SDL_Color(0, 0, 0, 255))
	#     text_rect = sdl2.SDL_Rect(x + 15, y + 7, 0, 0)
	#     sdl2.SDL_BlitSurface(window_title_text, None, sdl2.SDL_GetWindowSurface(window.window), text_rect)
	#     sdl2.SDL_FreeSurface(window_title_text)

		# Store a dummy rect to track position for dragging
		# windows.append(("gfx", sdl2.SDL_Rect(x, y, w, h)))

	def fetch_window_display():
		# SF Rendering
		# sdl2.SDL_FillRect(composited_windows.texture, None, 0)
		# for window_sprite, (x, y) in windows:
		# 	sdl2.surface.SDL_BlitSurface(window_sprite.surface, None, composited_windows.surface, sdl2.SDL_Rect(x, y, 0, 0))
		# return composited_windows

		# HW Rendering
		for texture, final_rect in windows:
			print(texture)
			sdl2.SDL_RenderCopy(renderer, texture, None, final_rect)

			# Draw Window Border
			sdl2.SDL_SetRenderDrawColor(renderer, 255, 255, 255, 77)
			sdl2.SDL_RenderDrawRect(renderer, final_rect)

		# Reset render draw color to white (or whatever you want)
		sdl2.SDL_SetRenderDrawColor(renderer, 255, 255, 255, 77)

	def handle_event(event):
		global dragging, dragged_window_index

		if event.type == sdl2.SDL_MOUSEBUTTONDOWN:
			if event.button.button == sdl2.SDL_BUTTON_LEFT:
				mouse_x, mouse_y = event.button.x, event.button.y

				for i, (texture, rect) in enumerate(windows):
					if rect.x <= mouse_x <= rect.x + rect.w and rect.y <= mouse_y <= rect.y + 37:
						dragging = True
						dragged_window_index = i
						break

		elif event.type == sdl2.SDL_MOUSEBUTTONUP:
			if event.button.button == sdl2.SDL_BUTTON_LEFT and dragging:
				dragging = False
				dragged_window_index = None

		elif event.type == sdl2.SDL_MOUSEMOTION and dragging:
			mouse_x, mouse_y = event.motion.x, event.motion.y
			texture, old_rect = windows[dragged_window_index]

			# Move the window directly to the mouse position
			new_rect = sdl2.SDL_Rect(mouse_x, mouse_y, old_rect.w, old_rect.h)
			windows[dragged_window_index] = (texture, new_rect)

	def check_socket():
		if wm.client is None:
			try:
				wm.client, _ = wm.server.accept()
				wm.client.setblocking(False)
				print("✅ Jasmine API connected")
			except BlockingIOError:
				pass

		if wm.client:
			try:
				data = wm.client.recv(1024)
				if data:
					print("Jasmine says:", data.decode())
					msg = json.loads(data.decode())
					print(msg)

					if msg.get("type") == "create_window":
						wm.create_window(msg.get("title"), msg.get("data"))

					wm.client.sendall(b"ACK\n")
			except BlockingIOError:
				pass
			except json.JSONDecodeError:
				print("❌ Invalid JSON from Jasmine")

### Jasmine API Integration ###


# if os.path.exists('/tmp/amethyine-wm-quartz.sock'):
#     os.remove('/tmp/amethyine-wm-quartz.sock')


# server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
# server.bind('/tmp/amethyine-wm-quartz.sock')
# server.listen()

# print('Listening for Jasmine API Calls')

# conn, _ = server.accept()
# print("Client connected (Jasmine API)")

# while True:
#     data = conn.recv(1024)
#     if not data:
#         break
#     print("Received:", data.decode())
#     try:
#     	message = json.loads(data.decode())
#     except json.JSONDecodeError:
#     	print('Invalid JSON')
#     	continue

#     if message.get('type') == 'create_window':
# 	    wm.create_window(message.get('title'))
#     # Echo back
#     conn.sendall(b"ACK\n")

### Jasmine API Integration ###

# wm.create_window('hihihihih')