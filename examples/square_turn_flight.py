from drone_control_api import Drone
from drone_control_api import PID

import time
import math

ip = '127.0.0.1'
port = "1233"


def main():

    client = Drone()

    client.connect(ip, port)
    
    client.armDrone()

    time.sleep(2.0)

    client.posholdOn()

    time.sleep(2.0)

    client.takeoff()   

    time.sleep(8)

    client.gotoXYdrone(3, 0)

    client.setYaw(-1.57)

    client.gotoXYdrone(3, 0)

    client.setYaw(3.14)
    
    client.gotoXYdrone(3, 0)

    client.setYaw(1.57)
    
    client.gotoXYdrone(3, 0)

    client.setYaw(0)

    client.boarding()

    time.sleep(1)

    client.disarmDrone()

    time.sleep(1)

    client.posholdOff()

    client.disconnect()



if __name__ == "__main__":
    main()

