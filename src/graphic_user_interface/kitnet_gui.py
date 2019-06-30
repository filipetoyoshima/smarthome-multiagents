from tkinter import * 

class Application(Frame):
    
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        """
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")
        """

        self.master.title("Kitnet automation system")

        # creating the 'Canvas' area of width and height 1000px
        canvas = Canvas(self.master, width = 1000, height = 1000)
        canvas.pack()

        # Create kitnet's rooms. Parameters of create_rectangle:(x1, y1, x2, y2, fill)

        room = canvas.create_rectangle(25, 25, 285, 285, fill = "grey", width = 5)
        bedroom = canvas.create_rectangle(285, 135, 545, 395, fill = "grey", width = 5)
        kitchen = canvas.create_rectangle(285, 25, 545, 135, fill = "grey", width = 5)
        bathroom = canvas.create_rectangle(25, 285, 285, 395, fill = "grey", width = 5)

        # Create kitnet's automatic doors. 
        
        room_door = canvas.create_rectangle(20, 50, 30, 100, fill = "red")
        bathroom_door = canvas.create_rectangle(200, 280, 250, 290, fill = "red")
        bedroom_door = canvas.create_rectangle(280, 175, 290, 225, fill = "red")

    def say_hi(self):
        print("hi there, everyone!")

root = Tk()
app = Application(master=root)
app.mainloop()
