from drone_control_api import Drone
from drone_control_api import PID
import time
import cv2

ip = "127.0.0.1"
port = "1233"

#  Функция поиска маркера
def search_aruco (yaw_vel):
    client.setVelXYYaw(0, 0, yaw_vel)
    aruco_state = True
    while aruco_state: 
        errors = client.getArucos()
        if errors:
            aruco_state = False
            client.setVelXYYaw(0, 0, 0)

# Функция рассчета ошибок
def tracking_aruco():
    pid_pitch = PID(0.45, 0.0, 0.0)
    pid_roll = PID(0.5, 0.0, 0.0)
    distance = 1.5 # Целевая дистанция
    accuracy_yaw = 0.1 # Допустимая ошибка по yaw
    accuracy = 0.2 # Допустимая ошибка
    while True:
        error = client.getArucos()
        img = client.getArucosImage()
        cv2.imshow('img', img)
        cv2.waitKey(1)

        if error:
            distance_to_marker = error[0]['pose']['position']['z']
            pitch_error = distance_to_marker - distance
            roll_error = error[0]['pose']['position']['x']
            yaw_error = -1 * error[0]['pose']['orientation']['z']

            # Сначала выравниваемся по yaw
            if abs(yaw_error) > accuracy_yaw:
                if yaw_error > 0:
                    yaw = 0.2
                else:
                    yaw = -0.2
                client.setVelXYYaw(0.0, 0.0, yaw)
            
            # после выравнивания по yaw, выравниваемся по pitch и roll
            else:
                aruco_regulation (pitch_error, roll_error, yaw_error, pid_pitch, pid_roll)

            # если выравнивание произошло, выходим из цикла
            if abs(pitch_error) < accuracy and abs(roll_error) < accuracy:
                client.setVelXYYaw(0.0, 0.0, 0.0)
                print("Выравнивание произошло")
                break
        
        else:
            aruco_regulation (pitch_error, roll_error, 0)
            print (f"Маркер потерян! Поиск:")
            print (f"pitch_error = {pitch_error}, \
                   roll_error = {roll_error}")

# Функция выравнивания по маркеру
def aruco_regulation(pitch_error, roll_error, yaw_error, pid_pitch:PID, pid_roll:PID):
    pid_pitch.update_control(pitch_error)
    PID_pitch = pid_pitch.get_control()
    PID_pitch = constrain (PID_pitch, 0.25)
    pid_roll.update_control(roll_error)
    PID_roll = pid_roll.get_control()
    PID_roll = constrain (PID_roll, 0.25)

    client.setVelXYYaw(PID_pitch, PID_roll, 0.0)

# Функция ограничения значений
def constrain (value, threshold):
    if value > threshold:
        value = threshold
    if value < -threshold:
        value = -threshold
    return value
            
client = Drone()
# Подключаемся
print("connected?", client.connect(ip, port), "\n")

client.armDrone()
time.sleep(2.0)

client.posholdOn()
time.sleep(2.0)

# Сбрасываем скорости
print("VelCorrect", client.setVelXYYaw(0,0,0),"\n")

# Взлет
client.takeoff()
client.setHeight(1.5)
time.sleep(7)

# Ищем маркер
search_aruco(0.5)

# Выравнивание относительно маркера
tracking_aruco()

print("Посадка")
client.boarding()
time.sleep(3)

client.disarmDrone()
time.sleep(1)

client.posholdOff()

client.disconnect()