from osbrain import run_agent
from osbrain import run_nameserver

"""
TODO: create handlers

def switch(agent, message):
    agent.log_info('received message')
"""

if __name__ == '__main__':

    # System Deployment
    """ TODO: instantiate all agents
    sensorA = run_agent('sensorA')
    lampA = run_agent('lampA')
    """
    ns = run_nameserver()
    temperatureSensor = run_agent('tempertature')
    luminousSensor = run_agent('luminous')
    presenceSensor = run_agent('presence')
    proximitySensor = run_agent('proximity')
    eletricController = run_agent('eletric')
    arConditionerController = run_agent('arConditioner')
    lampController = run_agent('lamp')
    doorController = run_agent('door')
    person = run_agent('person')
    environment = run_agent('environment')


    # System SetUp
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