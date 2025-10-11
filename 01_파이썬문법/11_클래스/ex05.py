class Person:
    def __init__(self):
        self.__name = ""    # private 변수
    
    #  property : 해당 변수를 데코레이터 기능을 사용하도록 지정
    #           - getter, setter 로 사용가능
    #           - @property 로 지정한 변수는 __변수와 같은 형태로 사용
    #           - @property 로 지정한 메소드가 getter 역할을 한다.
    @property               # getter
    def name(self):
        return self.__name
    
    # @변수.setter : 해당 메소드를 setter 메소드로 지정
    @name.setter           # setter
    def name(self, value):
        if len(value) > 0:
            self.__name = value
        else:
            print("이름은 비어있을 수 없습니다.")

# @변수.getter : 해당 메소드를 getter 메소드로 지정
#              - (객체.변수) 실행 시, 지정한 getter 메소드가 실행 
    @name.getter
    def name(self):
        return self.__name

person = Person()
person.name = "홍길동"     # setter 호출
print(person.name)        # getter 호출