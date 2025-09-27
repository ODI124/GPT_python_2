'''
    ▶️지역변수
    : 함수 내부에서 선언한 변수
      함수 내부에서만 접근 가능하고, 외부에서는 접근할 수 없다.
      
    ▶️전역변수
    : 함수 외부에서는 선언한 변수
      함수 내부나 외부 모든 영역에서 접근할 수 있다.
'''

def func():
    a = 10      # 지역변수
    print('func() 내부 - a : {}'.format(a))
    
    
func()          # 함수호출

# print('func() 외부 - a : {}'.format(a))
# 에러 발생
# NameError : 'a' is not defined (변수 'a'가 선언되어있지 않습니다.)

b = 10          # 전역변수

def test():
    print('func() 내부 - b : {}'.format(b))
    
test()          # 함수호출
print('func() 외부 - b : {}'.format(b))