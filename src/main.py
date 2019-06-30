from osbrain import run_agent
from osbrain import run_nameserver

"""
TODO: create handlers

def switch(agent, message):
    agent.log_info('received message')
"""

def getTemperature(self, message):
    if message > 293:
        self.isHeat = True
    else:
        self.isHeat = False


def seePresence(self, message):
    self.presence = message


if __name__ == '__main__':

    ### System Deployment ###
    ### This will define the agents on program
    
    ns = run_nameserver()  # Register main server where the agents will be registered by alias
    
    # 'External' Input
    person = run_agent(
        name = 'person',
        attributes = dict(
            x = 0,
            y = 0
        )
    )
    environment = run_agent(
        name = 'environment',
        attributes = dict(
            light = 1000, # the unit is lx, see https://en.wikipedia.org/wiki/Lux#Illuminance
            temperature = 293 # the unit is °k
        )
    )
    
    # Sensors
    temperatureSensor = run_agent('tempertature')
    luminositySensor = run_agent('luminous')
    presenceSensor = run_agent('presence')
    proximitySensor = run_agent('proximity')

    # Controllers
    eletricController = run_agent(
        'eletric',
        attributes = dict (
            power = True
        )
    )
    arConditionerController = run_agent(
        'arConditioner',
        attributes = dict (
            presence = False,
            isHeat = False,
            power = False,
            airTemperature = 289
        )
    )
    lampController = run_agent(
        'lamp',
        attributes = dict (
            presence = False,
            isNeeded = False,
            power = False
        )
    )
    doorController = run_agent(
        'door',
        attributes = dict (
            open = False
        )
    )

    # Follow the steps

    temperatureSensor.log_info('temperature sensor is running')
    luminositySensor.log_info('luminous sensor is running')
    presenceSensor.log_info('presence sensor is running')
    proximitySensor.log_info('proximity sensor is running')
    eletricController.log_info('temperature sensor is running')
    arConditionerController.log_info('luminous sensor is running')
    lampController.log_info('presence sensor is running')
    doorController.log_info('proximity sensor is running')

    ### System Setup ###
    ### This will connect agents that must send/receive data

    # Two sensors that will observe the person in home
    personAddr = person.bind('PUB', alias='person')
    presenceSensor.connect(personAddr, handler=checkLocation)
    proximitySensor.connect(personAddr, handler=checkDistance)
    
    # Two sensors that will observe enviroment details
    environAddr = environment.bind('PUB', alias='environment')
    temperatureSensor.connect(environAddr, handler=setTemperature)
    luminositySensor.connect(environAddr, handler=setLight)

    # Temperature sensor will send data to the arConditioner
    temperatureAddr = temperatureSensor('PUB', alias='temperature')
    arConditionerController.connect(temperatureAddr, handler=getTemperature)
    
    # Light sensor will send data to the lamps
    luminousAddr = luminositySensor('PUB', alias='light')
    lampController.connect(luminousAddr, handler=receiveLight)

    # Presence sensor will send data to the arConditioner and to the lamps
    presenceAddr = presenceSensor('PUB', alias='presence')
    arConditionerController.connect(presenceAddr, handler=seePresence)
    lampController.connect(presenceAddr, handler=seePresence)

    # Proximity sensor will send data to the doors controlers
    proxAddr = proximitySensor('PUB', alias='proximity')
    doorController.connect(proxAddr, handler=setOpen)
    

    # Send message
    """ TODO: monitor things in smart home
    """