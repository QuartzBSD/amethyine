import sdl2
import sdl2.ext

# def draw_wallpaper(factory, window):
# 	# [ Colored Wallpaper ]
# 	# wallpaper = factory.create_sprite(size=(window.size))
# 	# sdl2.ext.fill(wallpaper, (0, 0, 0))

# 	# [ Image Wallpaper ]
# 	wallpapers_path = sdl2.ext.Resources(__file__, "../resources/wallpapers")
# 	source_image = factory.from_image(wallpapers_path.get_path("demo.png"))
# 	# wallpaper = factory.from_image(wallpapers_path.get_path("demo.png"))

# 	wallpaper = factory.create_sprite(size=window.size)

# 	sdl2.surface.SDL_BlitScaled(source_image.surface, None, wallpaper.surface, None) # Software Rendering

# 	# spriterenderer = factory.create_sprite_render_system(window)
# 	# spriterenderer.render(wallpaper)
# 	return wallpaper

def draw_wallpaper(renderer, window):
	# [ Colored Wallpaper ]
	# wallpaper = factory.create_sprite(size=(window.size))
	# sdl2.ext.fill(wallpaper, (0, 0, 0))

	# [ Image Wallpaper ]
	wallpapers_path = sdl2.ext.Resources(__file__, "../resources/wallpapers")
	source_image = sdl2.ext.load_image(wallpapers_path.get_path("demo.png"))

	texture = sdl2.SDL_CreateTextureFromSurface(renderer, source_image)

	sdl2.SDL_FreeSurface(source_image)

	wallpaper_rect = sdl2.SDL_Rect(0, 0, window.size[0], window.size[1])

	sdl2.SDL_RenderClear(renderer)

	sdl2.SDL_RenderCopy(renderer, texture, None, wallpaper_rect)

	sdl2.SDL_DestroyTexture(texture)
	# sdl2.surface.SDL_BlitScaled(source_image.surface, None, wallpaper.surface, None) # Software Rendering

	# spriterenderer = factory.create_sprite_render_system(window)
	# spriterenderer.render(wallpaper)


	return texture
