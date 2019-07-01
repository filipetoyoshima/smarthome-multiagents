from tkinter import * 
from .constants import *

class EnvironmentGUI(Frame):
    
    def __init__(self, master=None, agent=None):
        super().__init__(master)
        self.master = master
        self.agent = agent
        self.pack()
        self.create_widgets()
        self.mouse_handler() 

    def create_widgets(self):
        self.master.title("Kitnet Automation System")

        # creating the 'Canvas' area of width and height 1000px
        self.canvas = Canvas(self.master, width = CANVAS_WIDTH, height = CANVAS_HEIGHT)
        self.canvas.pack()
        
        self.create_rooms()        
        self.create_doors()
        self.create_air_conditioners()

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
        room_door = self.canvas.create_rectangle(ROOM_DOOR_X1, ROOM_DOOR_Y1, ROOM_DOOR_X2, ROOM_DOOR_Y2, fill = "red", tags="room_door")
        bathroom_door = self.canvas.create_rectangle(BATHROOM_DOOR_X1, BATHROOM_DOOR_Y1, BATHROOM_DOOR_X2, BATHROOM_DOOR_Y2, fill = "red", tags="bathroom_door")
        bedroom_door = self.canvas.create_rectangle(BEDROOM_DOOR_X1, BEDROOM_DOOR_Y1, BEDROOM_DOOR_X2, BEDROOM_DOOR_Y2, fill = "red", tags="bedroom_door")

    def create_air_conditioners(self):
        room_air = self.canvas.create_rectangle(ROOM_AIR_X1, ROOM_AIR_Y1, ROOM_AIR_X2, ROOM_AIR_Y2, fill = "white", tags="room_air")
        room_air_text = self.canvas.create_text(ROOM_AIR_TEXT_X, ROOM_AIR_TEXT_Y, text="0 C", font=("Papyrus", 12), fill='black',tags="room_air_text")

        bedroom_air = self.canvas.create_rectangle(BEDROOM_AIR_X1, BEDROOM_AIR_Y1, BEDROOM_AIR_X2, BEDROOM_AIR_Y2, fill = "white", tags="bedroom_air")
        bedroom_text = self.canvas.create_text(BEDROOM_AIR_TEXT_X, BEDROOM_AIR_TEXT_Y, text="0 C", font=("Papyrus", 12), fill='black',tags="bedroom_air_text")        

    def mouse_handler(self):
        # Get mouse motion
        self.canvas.bind('<Motion>', self.mouse_motion)

    def mouse_motion(self, event):
        x, y = event.x, event.y
        self.agent.send('from_gui', str((x,y)), topic='person_position')

    def turn_on_light(self, tag):
        element = self.canvas.find_withtag(tag)
        self.canvas.itemconfig(element, fill='yellow')

    def turn_off_light(self, tag):
        element = self.canvas.find_withtag(tag)
        self.canvas.itemconfig(element, fill='grey')

    def turn_on_air_conditioner(self, tag):
        element = self.canvas.find_withtag(tag)
        self.canvas.itemconfig(element, fill='blue')

    def turn_off_air_conditioner(self, tag):
        element = self.canvas.find_withtag(tag)
        self.canvas.itemconfig(element, fill='white')

    def open_doors(self, x, y):
        if x > ROOM_DOOR_X1 - 20 and x < ROOM_DOOR_X2 + 20 and y > ROOM_DOOR_Y1 and y < ROOM_DOOR_Y2:
            self.open_room_door()
        elif x > BATHROOM_DOOR_X1 and x < BATHROOM_DOOR_X2 and y > BATHROOM_DOOR_Y1 - 20 and y < BATHROOM_DOOR_Y2 + 20:
            self.open_bathroom_door()
        elif x > BEDROOM_DOOR_X1 - 20 and x < BEDROOM_DOOR_X2 + 20 and y > BEDROOM_DOOR_Y1 and y < BEDROOM_DOOR_Y2:
            self.open_bedroom_door()

    def open_room_door(self):
        room_door = self.canvas.find_withtag('room_door')
        self.canvas.itemconfig(room_door, fill='green')

    def open_bathroom_door(self):
        bathroom_door = self.canvas.find_withtag('bathroom_door')
        self.canvas.itemconfig(bathroom_door, fill='green')

    def open_bedroom_door(self):
        bedroom_door = self.canvas.find_withtag('bedroom_door')
        self.canvas.itemconfig(bedroom_door, fill='green')
       


