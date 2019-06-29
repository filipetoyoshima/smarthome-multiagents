from osbrain import run_agent
from osbrain import run_nameserver

"""
TODO: create handlers

def switch(agent, message):
    agent.log_info('received message')
"""

if __name__ == '__main__':

    ### System Deployment ###
    
    ns = run_nameserver()
    
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
            light = 1000, # lx, see https://en.wikipedia.org/wiki/Lux#Illuminance
            temperature = 293 # °k
        )
    )
    
    # Sensors
    temperatureSensor = run_agent('tempertature')
    luminousSensor = run_agent('luminous')
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
            power = False,
            airTemperature = 289,
        )
    )
    lampController = run_agent(
        'lamp',
        attributes = dict (
            power = False
        )
    )
    doorController = run_agent(
        'door',
        attributes = dict (
            open = False
        )
    )


    ### System Setup ###
    # Two sensors that will observe the person in home
    personAddr = person.bind('PUB', alias='person')
    presenceSensor.connect(personAddr, handler=checkLocation)
    proximitySensor.connect(personAddr, handler=checkDistance)
    
    # Two sensors that will observe enviroment details
    environAddr = environment.bind('PUB', alias='environment')
    temperatureSensor.connect(environAddr, handler=setTemperature)
    luminousSensor.connect(environAddr, handler=setLight)

    # Temperature sensor will send data to the arConditioner
    temperatureAddr = temperatureSensor('PUB', alias='temperature')
    arConditionerController.connect(temperatureAddr, handler=getTemperature)
    
    # Light sensor will send data to the lamps
    luminousAddr = luminousSensor('PUB', alias='light')
    lampController.connect(luminousAddr, handler=receiveLight)

    # Presence sensor will send data to the arConditioner and to the lamps
    presenceAddr = presenceSensor('PUB', alias='presence')
    arConditionerController.connect(presenceAddr, handler=seekPresence)
    lampController.connect(presenceAddr, handler=setLight)

    # Proximity sensor will send data to the doors controlers
    proxAddr = proximitySensor('PUB', alias='proximity')
    doorController.connect(proxAddr, handler=setOpen)
    

    # Send message
    """ TODO: monitor things in smart home
    """