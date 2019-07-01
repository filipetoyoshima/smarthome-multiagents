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
        self.topics = {
            'person_position': self.handle_presence,
            'update_state': self.handle_state
        }

        main_addr = self.bind('PUB', alias='to_gui')


    def turn_on(self, topic):
        self.is_on = True
        self.send('to_gui', self.element_tag, topic=topic)
        self.log_info(f">>>>>> Turned {self.__class__.__name__} on <<<<<<")

    def turn_off(self, topic):
        self.is_on = False
        self.send('to_gui', self.element_tag, topic=topic)
        self.log_info(f">>>>>> Turned {self.__class__.__name__} off! <<<<<<")

    def connect(self, addr):
        assert_msg = "Set topics for " + self.__class__.__name__ + "!!!"
        assert self.topics, assert_msg

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
            self.handle_state(f" Presence changed, now: {self.is_personpresent}")

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
            **self.topics, 
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
        if self.is_personpresent and self.is_hot and not self.is_on:
            self.turn_on()
        elif not self.is_personpresent and self.is_cold and self.is_on:
            self.turn_off()

        self.log_info(
            f"State from {self.__class__.__name__} updated!" + message
        )

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
        if self.is_personpresent:
            self.turn_on()
        else:
            self.turn_off()

        self.log_info(
            f"State from {self.__class__.__name__} changed" + message
        )

    def turn_on(self):        
        assert self.element_tag, 'You didn\'t set the element tag'
        super().turn_on("turn_on_light")
    
    def turn_off(self):        
        assert self.element_tag, 'You didn\'t set the element tag' 
        super().turn_off("turn_off_light")
    

class Environment(Agent):

    def on_init(self):
        super().on_init()

        main_addr = self.bind('PUB', alias='from_gui')               

    def connect(self, addr):
        super().connect(addr, alias='to_gui', handler={'turn_on_light': self.handler_turn_on_lights,
                                                         'turn_off_light': self.handler_turn_off_lights,
                                                         'turn_off_air': self.handler_turn_off_air,
                                                         'turn_on_air': self.handler_turn_on_air,
                                                         'start_gui': self.start_gui})

    def start_gui(self, msg=""):
        self.root = Tk()
        self.app = EnvironmentGUI(master=self.root, agent=self)
        self.root.mainloop()
        
    def handler_turn_on_lights(self, tag):
        self.app.turn_on_light(tag)
    
    def handler_turn_off_lights(self, tag):
        self.app.turn_off_light(tag)
    
    def handler_turn_on_air(self, tag):
        self.app.turn_on_air_conditioner(tag)

    def handler_turn_off_air(self, tag):
        self.app.turn_off_air_conditioner(tag)


if __name__ == '__main__':
    ns = run_nameserver()

    room_lamp = run_agent('room_lamp', base=Lamp)
    room_lamp.set_attr(active_area=[ROOM_X1, ROOM_Y1, ROOM_X2, ROOM_Y2], element_tag='room')    

    environment = run_agent('environment', base=Environment)

    environment.connect(room_lamp.addr('to_gui'))
    room_lamp.connect(environment.addr('from_gui'))

    """room_air_conditioner = run_agent('air_conditioner', base=AirConditioner)
    room_air_conditioner.set_attr(active_area=[ROOM_X1, ROOM_Y1, ROOM_X2, ROOM_Y2], element_tag='room_air')
    room_air_conditioner.connect(environment.addr('from_gui'))"""

    environment.start_gui()
    
    ns.shutdown()
    