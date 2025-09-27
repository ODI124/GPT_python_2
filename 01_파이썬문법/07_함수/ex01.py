'''
    사용자 함수
    : 사용자가 직접 정의한 함수
    
    # 함수 정의 키워드 : def
    
    def 함수명( 매개변수1, 매개변수2, ... ):
        실행할 문장
        실행할 문장
        return (값)
    
    # return
    1. 함수를 종료
    2. (값)을 함수를 호출한 자리로 반환
    
    # 용어
    1. 함수 정의    : def 키워드로 사용자 함수를 새로 만드는 것
    2. 함수 호출    : 정의된 함수가 실행되도록 명령을 작성하는 것
    3. 인수         : 함수호출을 할 때 전달(입력)하는 값 (argument)
    4. 매개변수     : 인수를 전달받는 변수 (parameter)
    5. 반환값       : 함수가 반환하는 값, return 다음에 작성한 값
    
    # 함수 호출
    함수명( 인수1, 인수2, ... )
    
    #함수의 형태
    1. 인수X, 반환값X       : 함수명()
    2. 인수O, 반환값X       : 함수명(인수)
    3. 인수X, 반환값O       : 변수 = 함수명()
    4. 인수O, 반환값O       : 변수 = 함수명(인수)
    
'''

a = 10
b = 20

def plus(a,b):
    return a+b

def minus(a,b):
    return a-b

def mul(a,b):
    return a*b

def div(a,b):
    return a/b

print('a+b={}'.format( plus(a,b)))
print('a-b={}'.format( minus(a,b)))
print('a*b={}'.format( mul(a,b)))
print('a/b={}'.format( div(a,b)))