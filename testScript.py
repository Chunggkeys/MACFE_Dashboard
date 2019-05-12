import threading
import guiModel as gm
import random as r

print("running")

def changeValues():
    threading.Timer(2.0, changeValues).start()
    gm.setBatteryLevel(r.randint(1,101))
    gm.setBatteryTemperature(r.randint(1,101))
    gm.setHV(r.randint(0,2))
    gm.setLV(r.randint(0,2))
    gm.setMaxPower(r.randint(1,101))
    gm.setMotorTemperatureFour(r.randint(1,101))
    gm.setMotorTemperatureThree(r.randint(1,101))
    gm.setMotorTemperatureTwo(r.randint(1,101))
    gm.setMotorTemperatureOne(r.randint(1,101))
    # gm.setShutdown(r.randint(0,2))
    gm.setSpeed(r.randint(1,500))

changeValues()

