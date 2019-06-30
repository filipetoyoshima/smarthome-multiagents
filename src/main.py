import time
from random import randint
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
        self.isOn = False
        self.is_personpresent = False
        self.active_area = [10, 10, 400, 400]
        self.topics = {
            'person_position': self.handle_presence,
            'update_state': self.handle_state
        }

    def turnOn(self):
        self.isOn = True
        self.log_info(f">>>>>> Turned {self.__class__.__name__} on <<<<<<")

    def turnOff(self):
        self.isOn = False
        self.log_info(f">>>>>> Turned {self.__class__.__name__} off! <<<<<<")

    def connect(self, addr):
        assert_msg = "Set topics for " + self.__class__.__name__ + "!!!"
        assert self.topics, assert_msg

        super().connect(addr, alias='main', handler=self.topics)

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
        if self.is_personpresent and self.is_hot and not self.isOn:
            self.turnOn()
        elif not self.is_personpresent and self.is_cold and self.isOn:
            self.turnOff()

        self.log_info(
            f"State from {self.__class__.__name__} updated!" + message
        )


class Lamp(PassiveDevice):

    def on_init(self):
        super().on_init()

        self.active_area = [10, 10, 400, 400]


    def handle_state(self, message=""):
        if self.is_personpresent:
            self.turnOn()
        else:
            self.turnOff()

        self.log_info(
            f"State from {self.__class__.__name__} changed" + message
        )

        


if __name__ == '__main__':
    ns = run_nameserver()

    environment = run_agent('environment')
    main_addr = environment.bind('PUB', alias='main')

    air_conditioner = run_agent('air_conditioner', base=AirConditioner)
    air_conditioner.connect(main_addr)

    lamp = run_agent('lamp', base=Lamp)
    lamp.connect(main_addr)

    for _ in range(50):
        temperature = str(randint(0, 50))
        environment.send('main', temperature, topic='temperature')

        person_position = str((randint(0, 500), randint(0, 500)))
        environment.send('main', person_position, topic='person_position')

        time.sleep(1/20)

    ns.shutdown()
    
    ## 'External' Input
    #person = run_agent(
    #    name = 'person',
    #    attributes = dict(
    #        x = 0,
    #        y = 0
    #    )
    #)
    #
    ## Sensors
    #temperatureSensor = run_agent('tempertature')
    #luminositySensor = run_agent('luminous')
    #presenceSensor = run_agent('presence')
    #proximitySensor = run_agent('proximity')
    #
    ## Controllers
    #eletricController = run_agent(
    #    'eletric',
    #    attributes = dict (
    #        power = True
    #    )
    #)
    #lampController = run_agent(
    #    'lamp',
    #    attributes = dict (
    #        presence = False,
    #        isNeeded = False,
    #        power = False
    #    )
    #)
    #doorController = run_agent(
    #    'door',
    #    attributes = dict (
    #        open = False
    #    )
    #)


    #### System Setup ###
    #### This will connect agents that must send/receive data

    ## Two sensors that will observe the person in home
    #personAddr = person.bind('PUB', alias='person')
    #presenceSensor.connect(personAddr, handler=checkLocation)
    #proximitySensor.connect(personAddr, handler=checkDistance)
    #
    ## Two sensors that will observe enviroment details
    #environAddr = environment.bind('PUB', alias='environment')
    #temperatureSensor.connect(environAddr, handler=setTemperature)
    #luminositySensor.connect(environAddr, handler=setLight)

    ## Temperature sensor will send data to the arConditioner
    #temperatureAddr = temperatureSensor('PUB', alias='temperature')
    #arConditionerController.connect(temperatureAddr, handler=getTemperature)
    #
    ## Light sensor will send data to the lamps
    #luminousAddr = luminositySensor('PUB', alias='light')
    #lampController.connect(luminousAddr, handler=receiveLight)

    ## Presence sensor will send data to the arConditioner and to the lamps
    #presenceAddr = presenceSensor('PUB', alias='presence')
    #arConditionerController.connect(presenceAddr, handler=seePresence)
    #lampController.connect(presenceAddr, handler=seePresence)

    ## Proximity sensor will send data to the doors controlers
    #proxAddr = proximitySensor('PUB', alias='proximity')
    #doorController.connect(proxAddr, handler=setOpen)
    #
