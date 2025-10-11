#  예외 여러 개 일 때
#  예외를 따로 처리하는 방법

print('X / Y')

try:
    X = int( input('X : ') )
    Y = int( input('Y : ') )
    result = X / Y
except ZeroDivisionError:
    print('0으로 나눌 수 없습니다')
except ValueError:
    print('숫자만 입력 가능합니다')
except:
    print('알 수 없는 예외가 발생하였습니다')
else:
    print(result)
