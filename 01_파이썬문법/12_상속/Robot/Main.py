# Main.py
from Robot import Robot
from DroneRobot import DroneRobot
from CleanRobot import CleanRobot

print('# Robot #')
robot = Robot('휴먼로봇', 'ON', 100)
robot.move('왼쪽')
robot.charge()
print()

print('# DroneRotbot #')
drone = DroneRobot('드론로봇', 'ON', 100, 10)
drone.move('앞쪽', 50)
print()

print('# CleanRobot #')
cleanRobot = CleanRobot('로봇청소기', 'ON', 100, 0)
cleanRobot.mapping()
cleanRobot.move('앞쪽')
cleanRobot.vacate()