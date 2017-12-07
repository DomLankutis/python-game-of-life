from tkinter import *
from tkinter import messagebox


step = False


class Application(Frame):

    width = 0
    height = 0

    def __init__(self,x, y, master=None):
        super().__init__(master)
        self.x = x
        self.y = y
        self.grid = [[None for y in range(y)] for x in range(x)]
        self.pack()
        self.createWidgets()
        self.createCanvas()

    def roundCheck(self, xpos, ypos):
        alive = 0
        for x in (xpos - 1, xpos, xpos + 1):
            for y in (ypos - 1, ypos, ypos +1):
                if x == xpos and y == ypos:
                    alive += 0
                elif self.grid[y % self.y][x % self.x]:
                    alive += 1
        return alive

    def updateGrid(self):
        create = []
        delete = []
        for x in range(len(self.grid)):
            for y in range(len(self.grid[x])):
                alive = self.roundCheck(x, y)
                if not self.grid[y][x]:
                    if alive == 3:
                        create.append([x, y])
                else:
                    if alive == 2 or alive == 3:
                        pass
                    else:
                        delete.append([x, y])

        for c in range(len(create)):
            cx, cy = create[c][0], create[c][1]
            self.grid[cy][cx] = self.display.create_rectangle(cx * width, cy * height, (cx + 1) * width,
                                                            (cy + 1) * height, fill="black")
        for d in range(len(delete)):
            dx, dy = delete[d][0], delete[d][1]
            self.display.delete(self.grid[dy][dx])
            self.grid[dy][dx] = None

    def createWidgets(self):
        self.bParent = Frame(self).pack(side="bottom")

        self.bSwitch = Button(self.bParent, text="Start", command=self.switch)
        self.bSwitch.pack(side="left")

        self.bStep = Button(self.bParent, text="Step", command=self.updateGrid)
        self.bStep.pack(side="left")

        self.bClear = Button(self.bParent, text="Clear", command=self.clear)
        self.bClear.pack(side="left")

        self.bExit = Button(self.bParent, text="Quit", fg="red", command=self.master.destroy)
        self.bExit.pack(side="left")

    def createCanvas(self):
        self.display = Canvas(self, width=(self.x * 10), height=(self.y * 10), borderwidth=0,
                              background='white')
        self.display.pack(side="top")

    def canvasUpdate(self, event):
        global width, height, x, y
        width = self.display.winfo_width() / self.x
        height = self.display.winfo_width() / self.y

        x = event.x // width
        y = event.y // height
        x, y = int(x), int(y)

        if not self.grid[y][x]:
            self.grid[y][x] = self.display.create_rectangle(x*width, y*height, (x+1)*width, (y+1)*height, fill="black")
        else:
            self.display.delete(self.grid[y][x])
            self.grid[y][x] = None

    def switch(self):
        global step
        step = not step
        if not step:
            self.bSwitch["text"] = "Start"
        else:
            self.bSwitch["text"] = "Stop"

    def longUpdateGrid(self):
        global step, DELAY
        if step:
            self.updateGrid()
        self.after(int(DELAY.get()), self.longUpdateGrid)

    def clear(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                self.display.delete(self.grid[y][x])
                self.grid[y][x] = None


class InitApplication(Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        global x, y, DELAY
        x, y, DELAY = StringVar(), StringVar(), StringVar()
        self.xLabel = Label(self, text="X:").grid(row=0)
        self.fieldX = Entry(self, textvariable=x).grid(row=0, column=1)

        self.yLabel = Label(self, text="Y:").grid(row=1)
        self.fieldY = Entry(self, textvariable=y).grid(row=1, column=1)

        self.dLabel = Label(self, text="Delay:").grid(row=2)
        self.fieldD = Entry(self, textvariable=DELAY).grid(row=2, column=1)

        self.bSubmit = Button(self, text="Submit", command=self.check)
        self.bSubmit.grid(row=2, column=1, sticky="E")

    def check(self):
        try:
            int(x.get()); int(y.get()); int(DELAY.get())
            self.master.destroy()
        except ValueError:
            messagebox.showerror('Value Error', 'All values must be Numbers')

    def enterCheck(self, event):
        self.check()


x, y, DELAY = 0, 0, 0

temp = Tk()
initapp = InitApplication(master=temp)
temp.bind('<Return>', initapp.enterCheck)
initapp.mainloop()

root = Tk()
app = Application(int(x.get()), int(y.get()), master=root)
app.display.bind("<Button-1>", app.canvasUpdate)
app.after(int(DELAY.get()), app.longUpdateGrid)
app.mainloop()
