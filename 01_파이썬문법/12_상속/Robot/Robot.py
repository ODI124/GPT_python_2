# Robot.py

class Robot:
    def __init__(self, name, power, battery):
        self.name = name
        self.power = power
        self.battery = battery
        
    def power(self, power):
        self.power = power
        print('power : ', power)
        
    def move(self, direction):
        print('{} (으/)로 이동합니다.'.format(direction))
        
    def charge(self):
        self.battery = 100
        print('충전이 완료되었습니다.')
