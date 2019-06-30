import time
from random import randint
from osbrain import (
    run_nameserver,
    run_agent,
    Agent
)

# Will wait for messages to react
class PassiveDevices(Agent):

    def __call__(self):
        raise Exception("Abstract class! Not meant to be instantiated")

    def on_init(self):
        self.isOn = False

    def turnOn(self, temperature):
        self.isOn = True
        self.log_info(f"Turned {self.__class__.__name__} on! Temperature: {temperature}º")

    def turnOff(self, temperature):
        self.isOn = False
        self.log_info(f"Turned {self.__class__.__name__} off! Temperature: {temperature}º")

    def connect(self, addr):
        if not self.topics:
            raise Exception("Set topics for " + self.__class__.__name__ + "!!!")
        super().connect(addr, alias='main', handler=self.topics)


class AirConditioner(PassiveDevices):

    upper_temperature = 26
    lower_temperature = 19

    def on_init(self):
        super().on_init()

        self.isHot = False
        self.topics = {
            'temperature': AirConditioner.handle_temperature
        }

    @staticmethod
    def handle_temperature(agent, message):
        temperature = int(message)

        if temperature >= agent.upper_temperature and not agent.isOn:
            agent.turnOn(temperature)
        elif temperature <= agent.lower_temperature and agent.isOn:
            agent.turnOff(temperature)

if __name__ == '__main__':
    ns = run_nameserver()

    environment = run_agent('environment')
    main_addr = environment.bind('PUB', alias='main')

    air_conditioner = run_agent('air_conditioner', base=AirConditioner)
    air_conditioner.connect(main_addr)

    for _ in range(50):
        temperature = str(randint(0, 50))
        environment.send('main', temperature, topic='temperature')
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
