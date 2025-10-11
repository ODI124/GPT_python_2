# getter, setter
#  - getter : 변수의 값을 가져오는 메소드
#  - setter : 변수의 값을 지정하는 메소드
class Person:
    
    def __init__(self,name=None):
        self.__name = name
    
    #getter
    def get_name(self):
        return self.name
    
    # setter
    def set_name(self, value):
        self.name = value
        
p = Person()
p.set_name('김조은')
print('p - name : {}'.format( p.get_name()))
# print('p__name : {}'.format(p.__name))