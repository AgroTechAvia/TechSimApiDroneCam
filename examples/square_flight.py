from drone_control_api import Drone
from drone_control_api import PID

import time
import math

ip = '127.0.0.1'
port = "1233"


def main():

    client = Drone()
    # подключение
    client.connect(ip, port)
    # включаем моторы
    client.armDrone()

    time.sleep(2.0)
    # включаем пежим удержания позиции
    client.posholdOn()

    time.sleep(2.0)
    # взлет
    client.takeoff()
    # устанавливаем целевую высоту
    client.setHeight(1.5) 

    time.sleep(8)
    # обнуляем одометрию
    print(client.setZeroOdomOpticflow())

    # # полет в системе координат одометрии
    # print(client.gotoXYodom(2, 0))

    # print(client.gotoXYodom(2, -2))
    
    # print(client.gotoXYodom(0, -2))
    
    # print(client.gotoXYodom(0, 0))

    # полет в системе координат дрона
    print(client.gotoXYdrone(1, 0))

    print(client.gotoXYdrone(0, -1))
    
    print(client.gotoXYdrone(-1, 0))
    
    print(client.gotoXYdrone(0, 1))

    client.boarding()

    time.sleep(1)

    client.disarmDrone()

    time.sleep(1)

    client.posholdOff()

    client.disconnect()





if __name__ == "__main__":
    main()

