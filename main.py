from tkinter import *
from tkinter import messagebox
import random


step = False

# Enter to start / Stop
class Application(Frame):

    width = 0
    height = 0
    mx, my = 0, 0

    def __init__(self,x, y, master=None):
        super().__init__(master)
        self.master.attributes("-fullscreen", True)
        self.x = x
        self.y = y
        self.mHold = False
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

    def updateGrid(self, create=None, delete=None):
        if not delete and not create:
            create = []
            delete = []
            for x in range(len(self.grid)):
                for y in range(len(self.grid[x])):
                    alive = self.roundCheck(x, y)
                    if not self.grid[y][x]:
                        if alive == 3:
                            create.append([x, y])
                    else:
                        if alive in [2, 3]:
                            pass
                        else:
                            delete.append([x, y])

        for c in range(len(create)):
            cx, cy = create[c][0], create[c][1]
            self.grid[cy][cx] = self.display.create_rectangle(cx * width, cy * height, (cx + 1) * width, (cy + 1) *
                                                              height, fill="black")
        try:
            for d in range(len(delete)):
                dx, dy = delete[d][0], delete[d][1]
                self.display.delete(self.grid[dy][dx])
                self.grid[dy][dx] = None
        except TypeError:
            pass
            # Nothing to delete


    def createWidgets(self):
        self.bParent = Frame(self).pack(side="bottom")

        self.bSwitch = Button(self.bParent, text="Start", command=self.switch)
        self.bSwitch.pack(side="left")

        self.bStep = Button(self.bParent, text="Step", command=self.updateGrid)
        self.bStep.pack(side="left")

        self.bClear = Button(self.bParent, text="Clear", command=self.clear)
        self.bClear.pack(side="left")

        Button(self.bParent, text="Generate", command=self.generate).pack(side="left")

        self.bExit = Button(self.bParent, text="Quit", fg="red", command=self.master.destroy)
        self.bExit.pack(side="left")

    def createCanvas(self):
        self.display = Canvas(self, width=(self.x * 10), height=(self.y * 10), borderwidth=0,
                              background='white')
        self.display.pack(side="top")

    def canvasUpdate(self):
        global width, height, x, y, mx, my
        width = self.display.winfo_width() / self.x
        height = self.display.winfo_width() / self.y


        x = mx // width
        y = my // height
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

    def buSwitch(self, event):
        self.switch()

    def longUpdateGrid(self):
        global step, DELAY
        if step:
            self.updateGrid()
        self.after(int(DELAY.get()), self.longUpdateGrid)

    def mUpdate(self):
        if self.mHold:
            self.canvasUpdate()
        app.after(75, self.mUpdate)

    def mSwitch(self, event):
        self.mHold = not self.mHold

    def mGetPos(self, event):
        global mx, my
        mx, my = event.x, event.y

    def clear(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                self.display.delete(self.grid[y][x])
                self.grid[y][x] = None

    def generate(self):
        density = IntVar()
        self.toplevel = Toplevel()
        self.toplevel.title("Generate Settings")
        data = [("Low", 10), ("Medium", 30), ("High", 50)]
        for d in data:
            r = Radiobutton(self.toplevel, text=d[0], variable=density, value=d[1])
            r.pack(side="left")
        Button(self.toplevel, text="Submit", command=lambda: self.genSubmit(density.get())).pack(side="bottom")

    def genSubmit(self, density):
        self.toplevel.destroy()
        self.clear()
        self.canvasUpdate()
        create = []
        requiredPercent = density
        currentPercent = 0
        maxcells = len(self.grid)**2
        while currentPercent < requiredPercent:
            newCord = [random.randint(0, len(self.grid) - 1), random.randint(0, len(self.grid) - 1)]
            if newCord not in create:
                create.append(newCord)
            currentPercent = len(create) / maxcells * 100
        self.updateGrid(create=create)

class InitApplication(Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        global SIZE, DELAY
        SIZE, DELAY = StringVar(), StringVar()
        self.gLabel = Label(self, text="Grid:").grid(row=0)
        self.fieldG = Entry(self, textvariable=SIZE).grid(row=0, column=1)
        SIZE.set(100)

        self.dLabel = Label(self, text="Delay:").grid(row=2)
        self.fieldD = Entry(self, textvariable=DELAY).grid(row=2, column=1)
        DELAY.set(50)

        self.bSubmit = Button(self, text="Submit", command=self.check)
        self.bSubmit.grid(row=2, column=1, sticky="E")

    def check(self):
        try:
            int(SIZE.get()); int(DELAY.get())
            self.master.destroy()
        except ValueError:
            messagebox.showerror('Value Error', 'All values must be Numbers')

    def enterCheck(self, event):
        self.check()


SIZE, DELAY = 0, 0

temp = Tk()
initapp = InitApplication(master=temp)
temp.bind('<Return>', initapp.enterCheck)
initapp.mainloop()

root = Tk()
app = Application(int(SIZE.get()), int(SIZE.get()), master=root)
app.master.bind("<Return>", app.buSwitch)
app.display.bind("<Motion>", app.mGetPos)
app.display.bind("<Button-1>", app.mSwitch)
app.display.bind("<ButtonRelease-1>", app.mSwitch)
app.after(10, app.mUpdate)
app.after(int(DELAY.get()), app.longUpdateGrid)
app.mainloop()
