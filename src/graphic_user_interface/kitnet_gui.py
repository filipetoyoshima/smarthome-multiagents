from tkinter import * 
from constants import *

class Application(Frame):
    
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.mouse_handler()    

    def create_widgets(self):
        self.master.title("Kitnet automation system")

        # creating the 'Canvas' area of width and height 1000px
        self.canvas = Canvas(self.master, width = CANVAS_WIDTH, height = CANVAS_HEIGHT)
        self.canvas.pack()
        
        self.create_rooms()        
        self.create_doors()

    def create_rooms(self):
        # Create kitnet's rooms. Parameters of create_rectangle:(x1, y1, x2, y2, fill)
        room = self.canvas.create_rectangle(ROOM_X1, ROOM_Y1, ROOM_X2, ROOM_Y2, fill = "grey", width = 5, tags="room")
        room_text = self.canvas.create_text(ROOM_TEXT_X, ROOM_TEXT_Y, text="Room", font=("Papyrus", 22), fill='black',tags="room_text")
        
        bedroom = self.canvas.create_rectangle(BEDROOM_X1, BEDROOM_Y1, BEDROOM_X2, BEDROOM_Y2, fill = "grey", width = 5, tags="bedroom")
        bedroom_text = self.canvas.create_text(BEDROOM_TEXT_X, BEDROOM_TEXT_Y, text="Bedroom", font=("Papyrus", 22), fill='black',tags="bedroom_text")
        
        kitchen = self.canvas.create_rectangle(KITCHEN_X1, KITCHEN_Y1, KITCHEN_X2, KITCHEN_Y2, fill = "grey", width = 5, tags="kitchen")
        kitchen_text = self.canvas.create_text(KITCHEN_TEXT_X, KITCHEN_TEXT_Y, text="Kitchen", font=("Papyrus", 22), fill='black',tags="kitchen_text")

        bathroom = self.canvas.create_rectangle(BATHROOM_X1, BATHROOM_Y1, BATHROOM_X2, BATHROOM_Y2, fill = "grey", width = 5, tags="bathroom")
        bathroom_text = self.canvas.create_text(BATHROOM_TEXT_X, BATHROOM_TEXT_Y, text="Bathroom", font=("Papyrus", 22), fill='black',tags="bathroom_text")

    def create_doors(self):
        # Create kitnet's automatic doors.        
        room_door = self.canvas.create_rectangle(ROOM_DOOR_X1, ROOM_DOOR_Y1, ROOM_DOOR_X2, ROOM_DOOR_Y2, fill = "red")
        bathroom_door = self.canvas.create_rectangle(BATHROOM_DOOR_X1, BATHROOM_DOOR_Y1, BATHROOM_DOOR_X2, BATHROOM_DOOR_Y2, fill = "red")
        bedroom_door = self.canvas.create_rectangle(BEDROOM_DOOR_X1, BEDROOM_DOOR_Y1, BEDROOM_DOOR_X2, BEDROOM_DOOR_Y2, fill = "red")

    def mouse_handler(self):
        # Get mouse motion
        self.canvas.bind('<Motion>', self.mouse_motion)

    def mouse_motion(self, event):
        x, y = event.x, event.y
        print('{}, {}'.format(x, y))

        # Test if the person is into some room's house and turn on the room light
        if x > ROOM_X1 and x < ROOM_X2 and y > ROOM_Y1 and y < ROOM_Y2:            
            self.turn_on_room_light()
        elif x > BEDROOM_X1 and x < BEDROOM_X2 and y > BEDROOM_Y1 and y < BEDROOM_Y2:
            self.turn_on_bedroom_light()
        elif x > KITCHEN_X1 and x < KITCHEN_X2 and y > KITCHEN_Y1 and y < KITCHEN_Y2:
            self.turn_on_kitchen_light()
        elif x > BATHROOM_X1 and x < BATHROOM_X2 and y > BATHROOM_Y1 and y < BATHROOM_Y2:
            self.turn_on_bathroom_light()

    def turn_on_room_light(self):
        room = self.canvas.find_withtag('room')
        self.canvas.itemconfig(room, fill='yellow')

    def turn_on_bedroom_light(self):
        room = self.canvas.find_withtag('bedroom')
        self.canvas.itemconfig(room, fill='yellow')

    def turn_on_kitchen_light(self):
        room = self.canvas.find_withtag('kitchen')
        self.canvas.itemconfig(room, fill='yellow')

    def turn_on_bathroom_light(self):
        room = self.canvas.find_withtag('bathroom')
        self.canvas.itemconfig(room, fill='yellow')

        

root = Tk()
app = Application(master=root)
app.mainloop()
