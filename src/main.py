import time
import threading
from tkinter import *
from random import randint
from graphic_user_interface.constants import *
from graphic_user_interface.kitnet_gui import EnvironmentGUI
from osbrain import (
    run_nameserver,
    run_agent,
    Agent
)

# Will wait for messages to react
class PassiveDevice(Agent):

    def __call__(self):
        raise NotImplementedError(
            "Abstract class! Not meant to be instantiated"
        )

    def on_init(self):
        self.is_on = False
        self.element_tag = ""
        self.is_personpresent = False
        self.active_area = [10, 10, 400, 400]
 
        main_addr = self.bind('PUB', alias='to_gui')


    def turn_on(self, topic):
        self.is_on = True
        self.log_info(f">>>>>> Turned {self.__class__.__name__} on <<<<<<")

    def turn_off(self, topic):
        self.is_on = False
        self.log_info(f">>>>>> Turned {self.__class__.__name__} off! <<<<<<")

    def connect(self, addr):
        assert_msg = "Set topics for " + self.__class__.__name__ + "!!!"

        super().connect(addr, alias='from_gui', handler=self.topics)


    # At smarthome all passive devices depends on presence
    def handle_presence(self, message):
        # Format of message: (x, y)
        person_x, person_y = (int(c.strip()) for c in message[1:-1].split(','))
        area_x1, area_y1, area_x2, area_y2 = self.active_area

        old_state = self.is_personpresent
        self.is_personpresent = (
            person_x > area_x1 and person_x  < area_x2
            and person_y > area_y1 and person_y < area_y2
        )

        if old_state != self.is_personpresent:
            return self.handle_state(f" Presence changed, now: {self.is_personpresent}")

        return None, None

    def handle_state(self):
        # If something, turn on. Else, turn off
        raise NotImplementedError(
            "Passive devices must override handle_state"
            "and subscribe to update_state topic"
        )


class AirConditioner(PassiveDevice):

    def on_init(self):
        super().on_init()

        self.is_hot = False
        self.is_cold = False
        self.upper_temperature = 26
        self.lower_temperature = 19
        self.topics = {
            # **self.topics, 
            'temperature': AirConditioner.handle_temperature,
        }

    def handle_temperature(self, temperature_string):
        temperature = int(temperature_string)

        old_state_hot = self.is_hot
        old_state_cold = self.is_cold

        # Not hot doesn't mean is cold
        self.is_hot = temperature >= self.upper_temperature
        self.is_cold = temperature <= self.lower_temperature

        if old_state_hot != self.is_hot or old_state_cold != self.is_cold:
            self.handle_state(f" Temperature changed: {temperature}º")

    def handle_state(self, message=""):
        state = (None, None)

        if self.is_personpresent and self.is_hot and not self.is_on:
            self.turn_on()
            state = ('air', True)
        elif not self.is_personpresent and self.is_cold and self.is_on:
            self.turn_off()
            state = ('air', False)

        self.log_info(
            f"State from {self.__class__.__name__} updated!" + message
        )

        return state

    def turn_on(self):        
        assert self.element_tag, 'You didn\'t set the element tag'
        super().turn_on("turn_on_air")
    
    def turn_off(self):        
        assert self.element_tag, 'You didn\'t set the element tag' 
        super().turn_off("turn_off_air")


class Lamp(PassiveDevice):

    def on_init(self):
        super().on_init()

    def handle_state(self, message=""):
        state = (None, None)
        if self.is_personpresent:
            self.turn_on()
            state = ('lamp', True)
        else:
            self.turn_off()
            state = ('lamp', False)

        self.log_info(
            f"State from {self.__class__.__name__} changed" + message
        )

        return state

    def turn_on(self):        
        assert self.element_tag, 'You didn\'t set the element tag'
        super().turn_on("turn_on_light")
    
    def turn_off(self):        
        assert self.element_tag, 'You didn\'t set the element tag' 
        super().turn_off("turn_off_light")

class Door(PassiveDevice):

    def on_init(self):
        super().on_init()

    def handle_state(self, message=""):
        state = (None, None)
        if self.is_personpresent:
            self.turn_on()
            state = ('door', True)
        else:
            self.turn_off()
            state = ('door', False)

        self.log_info(
            f"State from {self.__class__.__name__} changed" + message
        )

        return state

    def turn_on(self):        
        assert self.element_tag, 'You didn\'t set the element tag'
        super().turn_on("open_door")
    
    def turn_off(self):        
        assert self.element_tag, 'You didn\'t set the element tag' 
        super().turn_off("close_door")

    

class Environment(Agent):

    agents = []

    def on_init(self):
        super().on_init()
        main_addr = self.bind('PUB', alias='from_gui')

        self.create_lamp_agents()
        self.create_air_agents()
        self.create_door_agents()


    def create_lamp_agents(self):
        # Room Lamp Agent
        self.room_lamp = run_agent('room_lamp', base=Lamp)
        self.agents.append(self.room_lamp)
        self.room_lamp.set_attr(active_area=[ROOM_X1, ROOM_Y1, ROOM_X2, ROOM_Y2], element_tag='room')

        # Bedroom Lamp Agent
        self.bedroom_lamp = run_agent('bedroom_lamp', base=Lamp)
        self.agents.append(self.bedroom_lamp)
        self.bedroom_lamp.set_attr(active_area=[BEDROOM_X1, BEDROOM_Y1, BEDROOM_X2, BEDROOM_Y2], element_tag='bedroom')

        # Kitchen Lamp Agent
        self.kitchen_lamp = run_agent('kitchen_lamp', base=Lamp)
        self.agents.append(self.kitchen_lamp)
        self.kitchen_lamp.set_attr(active_area=[KITCHEN_X1, KITCHEN_Y1, KITCHEN_X2, KITCHEN_Y2], element_tag='kitchen')

        # Kitchen Lamp Agent
        self.bathroom_lamp = run_agent('bathroom_lamp', base=Lamp)
        self.agents.append(self.bathroom_lamp)
        self.bathroom_lamp.set_attr(active_area=[BATHROOM_X1, BATHROOM_Y1, BATHROOM_X2, BATHROOM_Y2], element_tag='bathroom')


    def create_air_agents(self):
        # Room Air Agent
        self.room_air = run_agent('room_air', base=AirConditioner)
        self.agents.append(self.room_air)
        self.room_air.set_attr(active_area=[ROOM_X1, ROOM_Y1, ROOM_X2, ROOM_Y2], element_tag='room')

        # self.connect(self.room_air.addr('to_gui'))
        self.room_air.connect(self.addr('from_gui'))

        # Bedroom Air Agent
        self.bedroom_air = run_agent('bedroom_air', base=AirConditioner)
        self.agents.append(self.bedroom_air)
        self.bedroom_air.set_attr(active_area=[BEDROOM_X1, BEDROOM_Y1, BEDROOM_X2, BEDROOM_Y2], element_tag='bedroom')
        
        # self.connect(self.bedroom_air.addr('to_gui'))
        self.bedroom_air.connect(self.addr('from_gui'))

    def create_door_agents(self):
        # Room Door Agent
        self.room_door = run_agent('room_door', base=Door)
        self.agents.append(self.room_door)
        self.room_door.set_attr(active_area=[ROOM_DOOR_X1 - 20, ROOM_DOOR_Y1, ROOM_DOOR_X2 + 20, ROOM_DOOR_Y2], element_tag='room_door')

        # Bedroom Door Agent
        self.bedroom_door = run_agent('bedroom_door', base=Door)
        self.agents.append(self.bedroom_door)
        self.bedroom_door.set_attr(active_area=[BEDROOM_DOOR_X1 - 20, BEDROOM_DOOR_Y1, BEDROOM_DOOR_X2 + 20, BEDROOM_DOOR_Y2], element_tag='bedroom_door')

        # Bathroom Door Agent
        self.bathroom_door = run_agent('bathroom_door', base=Door)
        self.agents.append(self.bathroom_door)
        self.bathroom_door.set_attr(active_area=[BATHROOM_DOOR_X1, BATHROOM_DOOR_Y1 - 20, BATHROOM_DOOR_X2, BATHROOM_DOOR_Y2 + 20], element_tag='bathroom_door')


    def start_gui(self, msg=""):
        self.root = Tk()
        self.app = EnvironmentGUI(master=self.root, agent=self)
        self.root.mainloop()

    def mouse_handler(self, event):

        
        temperature = str(randint(0, 50))
        print("===================================")
        print(temperature)
        print("===================================")
        self.send('from_gui', temperature, topic='temperature')

        # time.sleep(1)

        x, y = event.x, event.y        

        for agent in self.agents:
            element, action = agent.handle_presence(str((x,y)))

            if(element is None or action is None):
                continue
            if(element == 'air' and action is True):
                tag = agent.get_attr('element_tag') + "_air"
                text = tag + "_text"
                self.app.turn_on_air_conditioner(tag, text)
            elif(element == 'air' and action is False):
                tag = agent.get_attr('element_tag') + "_air"
                text = tag + "_text"
                self.app.turn_off_air_conditioner(tag, text)
            elif(element == 'lamp' and action is True):
                self.app.turn_on_light(agent.get_attr('element_tag'))
            elif(element == 'lamp' and action is False):
                self.app.turn_off_light(agent.get_attr('element_tag'))
            elif(element == 'door' and action is True):
                self.app.open_door(agent.get_attr('element_tag'))
            elif(element == 'door' and action is False):
                self.app.close_door(agent.get_attr('element_tag'))
                


if __name__ == '__main__':
    ns = run_nameserver()    

    environment = run_agent('environment', base=Environment)
    environment.start_gui()

    ns.shutdown()
    