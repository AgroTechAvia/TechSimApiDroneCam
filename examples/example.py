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

    client.setHeight(2.0)    

    time.sleep(8)



    try:
        while True:
            print(f"-" * 30)
            print(client.getUltrasonic())
            print(client.getRPY())

            time.sleep(0.05)


    except Exception as err:
        print(err)


    client.disconnect()





if __name__ == "__main__":
    main()

