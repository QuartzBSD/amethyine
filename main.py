# main.py
import sys
import sdl2
import sdl2.ext
import tkinter as tk # For Screen Resolution Detection

root = tk.Tk()

displayWidth = root.winfo_screenwidth()
displayHeight = root.winfo_screenheight()

sdl2.ext.init()
# window = sdl2.ext.Window("Quartz Compositor ( Amethyine )", size=(1280, 720))
# window = sdl2.ext.Window("Quartz Compositor ( Amethyine )", size=(1600, 900))
window = sdl2.ext.Window("Quartz Compositor ( Amethyine )", size=(displayWidth, displayHeight))
sdl2.SDL_SetWindowFullscreen(window.window, sdl2.SDL_WINDOW_FULLSCREEN)


window.show()

# factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
hw_renderer = renderer_hw = sdl2.ext.renderer.Renderer(
    window,
    flags=sdl2.SDL_RENDERER_ACCELERATED | sdl2.SDL_RENDERER_PRESENTVSYNC
)
factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=hw_renderer)
# renderer = factory.create_sprite_render_system(window)

def run():
	# Wallpaper Initilization
    from core.wallpaper import draw_wallpaper
    # background = draw_wallpaper(factory, window) # Software Rendering
    # background = draw_wallpaper(hw_renderer.renderer, window) 

    from core.wm.main import wm
    wm.init(factory, window, hw_renderer.renderer)

    # from core.wm.main import fetch_window_display
    # from core.wm.main import create_window

    # windows = wm.fetch_window_display()

    wm.create_window('Window Title 1', {'x':10, 'y':10})
    wm.create_window('Window Title 2', {'x':100, 'y':50})

    # sdl2.SDL_SetSurfaceBlendMode(windows.surface, sdl2.SDL_BLENDMODE_BLEND)

    # final_composite = sdl2.SDL_CreateRGBSurfaceWithFormat(0, 1280, 720, 
    #     window.get_surface().format.contents.BitsPerPixel,
    #     window.get_surface().format.contents.format
    # )

    running = True
    while running:
        for event in sdl2.ext.get_events():
            if event.type == sdl2.SDL_QUIT:
                running = False
                break

            # print(event.type)
            wm.handle_event(event)


        # renderer.clear() # For hardware-acclerated rendering ( later implementation)
        # window_surface = window.get_surface()
        # if sdl2.SDL_MUSTLOCK(window_surface):
        #     sdl2.SDL_LockSurface(window_surface)

        # sdl2.ext.fill(window_surface, sdl2.ext.Color(0, 0, 0))
        # renderer.render(background)
        # windows = wm.fetch_window_display()

        wm.check_socket()
        hw_renderer.clear()
        draw_wallpaper(hw_renderer.renderer, window)
        wm.fetch_window_display()
        hw_renderer.present()
        # renderer.render(windows)

        # window.refresh()
        # renderer.render(final_composite)

        # window.refresh()

        sdl2.SDL_Delay(16) # For 60 FPS

    sdl2.ext.quit()
    return 0

if __name__ == "__main__":
    sys.exit(run())
