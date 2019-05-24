import threading
import guiModel as gm
import random as r

print("running")

def changeValues():
    
    ## Recursively executes changeValues in 2 second intervals
    threading.Timer(2.0, changeValues).start()
    ##
    ## Changes values of guiModel instance
    gm.setBatteryLevel(r.randint(1,101))
    gm.setBatteryTemperature(r.randint(1,101))
    gm.setStartupStatus(r.randint(0,3))
    gm.setMaxPower(r.randint(1,101))
    gm.setMotorTemperatureFour(r.randint(1,101))
    gm.setMotorTemperatureThree(r.randint(1,101))
    gm.setMotorTemperatureTwo(r.randint(1,101))
    gm.setMotorTemperatureOne(r.randint(1,101))
    # gm.setShutdown(r.randint(0,2))
    gm.setSpeed(r.randint(1,500))
    ##
changeValues()

