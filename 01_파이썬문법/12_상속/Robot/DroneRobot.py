# DroneRobot.py
from Robot import Robot

class DroneRobot(Robot):
    max_height = 50
    
    def __init__(self, name, power, battery, height):
        super().__init__(name, power, battery)
        self.height = height
        
    def move(self, direction, height):
        if height > DroneRobot.max_height:
            print('{}m 이상으로는 비행할 수 없습니다'.format(DroneRobot.max_height))
            return
            
        self.height = height
        print('고도 : {}'.format(height))
        print('{} (으/)로 방향으로 비행합니다.'.format(direction))
