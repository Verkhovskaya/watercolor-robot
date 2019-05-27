from tkinter import *
from tkinter.colorchooser import askcolor
import os
import sys

class Text:
    def __init__(self, path):
        self.path = path
        self.file = open(path, "w")

    def write(self, new_line):
        self.file.write(new_line)
        self.file.write("\n")
        print(new_line)

    def exec(self):
        self.file.close()
        os.system('python ' + self.path)
        self.file = open(self.path, "a")

text = Text("painting.py")

class Paint(object):

    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'dark-green'
    DEFAULT_BRUSH = 1
    CANVAS_WIDTH = 1000
    CANVAS_HEIGHT = 600
    RATIO = 0.9

    COLORS = {
        'light-purple': "#CAA9D4",
        'dark-purple': "#65187A",
        'light-green': '#90EE90',
        'dark-green': '#006400',
        'brown': '#8b4513',
        'dark-grey': '#808080',
        'dark-red': '#8b0000',
    }

    def __init__(self):
        self.brush_x = None
        self.brush_y = None
        self.text = text
        self.text.write("from control import *")
        self.root = Tk()

        self.choose_size_button = Scale(self.root, from_=1, to=10, orient=HORIZONTAL)
        #self.choose_size_button.grid(row=0, column=4)

        # Choose brush type
        self.current_brush = self.DEFAULT_BRUSH;
        brush_var = StringVar(self.root)
        brushes = { 1, 2, 3, 4, 5}
        brush_var.set(self.DEFAULT_BRUSH) # set the default option
        self.choose_brush = OptionMenu(self.root, brush_var, *brushes, command=self.change_brush)
        self.choose_brush.grid(row = 0, column = 2)

        # Choose paint color
        self.current_color = self.DEFAULT_COLOR;
        color_var = StringVar(self.root)
        color_var.set(self.DEFAULT_COLOR) # set the default option
        self.choose_color = OptionMenu(self.root, color_var, *self.COLORS.keys(), command=self.change_color)
        self.choose_color.grid(row = 0, column = 3)

        # Send to robot
        self.print_button = Button(self.root, text='send to robot', command=self.send_to_robot)
        self.print_button.grid(row=0, column=4)

        self.c = Canvas(self.root, bg='white', width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT)
        self.c.grid(row=1, columnspan=5)

        self.setup()
        self.root.mainloop()

    def change_color(self, new_color):
        self.text.write("end_line()")
        self.current_color = new_color

    def change_brush(self, new_brush):
        self.text.write("clean()")
        self.text.write("switch_brush(" + str(new_brush) + ")")
        self.current_brush = new_brush

    def setup(self):
        self.count = 0
        self.line_start = None
        self.color = self.DEFAULT_COLOR
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.click_release)

    def send_to_robot(self):
        self.text.write("clean()")
        self.text.write("reset()")
        text.exec()

    def scale_x(self, x):
        return str(x*100/self.CANVAS_WIDTH)

    def scale_y(self, y):
        return str(y*100/self.CANVAS_HEIGHT)

    def click_release(self, event):
        self.text.write("end_line()")
        self.line_start = None
        self.count = 0

    def paint(self, event):
        if not self.line_start:
            self.line_start = (event.x, event.y)
            self.text.write("clean()")
            self.text.write("load_color('" + self.current_color + "')")
            self.c.create_line(event.x-15, event.y-15, event.x+15, event.y+15, width = 5, fill=self.COLORS[self.current_color])
            self.c.create_line(event.x-15, event.y+15, event.x+15, event.y-15, width = 5, fill=self.COLORS[self.current_color])
        else:
            if (self.count == 20):
                self.text.write("start_at(" + self.scale_x(self.line_start[0]) + "," + self.scale_y(self.line_start[1]) + "," + self.scale_x(event.x)+ "," + self.scale_y(event.y)+")")
            if (self.count % 20 == 0) and self.count > 0:
                self.text.write("move_to(" + self.scale_x(event.x) + "," + self.scale_y(event.y)+")")
                self.c.create_line(self.line_start[0], self.line_start[1], event.x, event.y,
                                   width=5*self.current_brush, fill=self.COLORS[self.current_color],
                                   capstyle=ROUND, smooth=TRUE, splinesteps=36)
                self.line_start = (event.x, event.y)
            self.count += 1
