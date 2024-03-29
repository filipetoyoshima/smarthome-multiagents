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
        room_air_text = self.canvas.create_text(ROOM_AIR_TEXT_X, ROOM_AIR_TEXT_Y, text="0 ºC", font=("Papyrus", 12), fill='black',tags="room_air_text")

        bedroom_air = self.canvas.create_rectangle(BEDROOM_AIR_X1, BEDROOM_AIR_Y1, BEDROOM_AIR_X2, BEDROOM_AIR_Y2, fill = "white", tags="bedroom_air")
        bedroom_text = self.canvas.create_text(BEDROOM_AIR_TEXT_X, BEDROOM_AIR_TEXT_Y, text="0 ºC", font=("Papyrus", 12), fill='black',tags="bedroom_air_text")        

    def mouse_handler(self):
        # Get mouse motion
        self.canvas.bind('<Motion>', self.agent.mouse_handler)

    def turn_on_light(self, tag):
        element = self.canvas.find_withtag(tag)
        self.canvas.itemconfig(element, fill='yellow')

    def turn_off_light(self, tag):
        element = self.canvas.find_withtag(tag)
        self.canvas.itemconfig(element, fill='grey')

    def turn_on_air_conditioner(self, tag, text, temperature):
        element = self.canvas.find_withtag(tag)
        self.canvas.itemconfig(element, fill='blue')
        element_text = self.canvas.find_withtag(text)
        self.canvas.itemconfig(element_text, text=temperature + " ºC")

    def turn_off_air_conditioner(self, tag, text, temperature):
        element = self.canvas.find_withtag(tag)
        self.canvas.itemconfig(element, fill='white')
        element_text = self.canvas.find_withtag(text)
        self.canvas.itemconfig(element_text, text=temperature + " ºC")

    def open_door(self, tag):
        element = self.canvas.find_withtag(tag)
        self.canvas.itemconfig(element, fill='green')

    def close_door(self, tag):
        element = self.canvas.find_withtag(tag)
        self.canvas.itemconfig(element, fill='red')
       


