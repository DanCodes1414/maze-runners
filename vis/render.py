#!/usr/bin/env python3

"""
so, to quit the programme a user can press '4' or click the x on the window.
Pressing ctrl-Z suspends the process, putting it in the background (the same as sending the SIGTSTP signal).
The window becomes unresponsive, type 'fg' (foreground) in the terminal to resolve.
?TODO? : look at handling ctrl-\

"""
from mlx import Mlx

class MazeRender:

    EXIT_KEY = 52
    EXIT_BUTTON = 33

    def __init__(self) -> None:
        self.m = Mlx()
        self.mlx_ptr = None
        self.win_width = None
        self.win_height = None
        self.win_ptr = None
        self.img_ptr = None

    def free_and_quit(self):
        #self.m.mlx_destroy_image(self.mlx_ptr, self.img_ptr)
        self.m.mlx_destroy_window(self.mlx_ptr, self.win_ptr)
        self.m.mlx_release(self.mlx_ptr)

    def myclose(self, param):
        self.m.mlx_loop_exit(self.mlx_ptr)

    def mymouse(self, button, x, y, mystuff):
        #print(mystuff)
        print(f"Got mouse event! button {button} at {x}, {y}.")

    def mykey(self, keynum, mystuff):
        #print(f"Got key {keynum}, and got my stuff back:")
        #print(mystuff)
        if keynum == self.EXIT_KEY:
            self.m.mlx_loop_exit(self.mlx_ptr)
    
    def run_window(self) -> None:
        self.mlx_ptr = self.m.mlx_init()
        self.win_width, self.win_height = 960, 600
        self.win_ptr = self.m.mlx_new_window(self.mlx_ptr, self.win_width, self.win_height, "A-Maze-ing")
        self.m.mlx_clear_window(self.mlx_ptr, self.win_ptr)
        #self.m.mlx_string_put(self.mlx_ptr, self.win_ptr, int(self.win_width / 2), int(self.win_height / 2), 255, "Hello PyMlx!")
        #(ret, w, h) = self.m.mlx_get_screen_size(self.mlx_ptr)
        #self.img_ptr = self.m.mlx_new_image(self.mlx_ptr, self.win_width, self.win_height)
        #print(f"Got screen size: {w} x {h} .")
        stuff = [1, 2]
        self.m.mlx_hook(self.win_ptr, self.EXIT_BUTTON, 0, self.myclose, None)
        self.m.mlx_mouse_hook(self.win_ptr, self.mymouse, None)
        self.m.mlx_key_hook(self.win_ptr, self.mykey, stuff)
        self.m.mlx_loop(self.mlx_ptr)
        self.free_and_quit()
    
render = MazeRender()

render.run_window()
