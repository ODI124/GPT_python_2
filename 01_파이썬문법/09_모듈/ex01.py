import math

# 원주율
print('math.pi {}'.format( math.pi ))

# ceil() 올림
print('math.ceil(1.1) : {}'.format( math.ceil(1.1) ))

# floor() 내림
print('math.floor(1.9) : {}'.format( math.floor(1.9) ))

# round() 반올림 - Math 모듈 외 기본 내장함수
print('round(2.5, 1) : {}'.format( round(2.5, 1) ))
print('round(2.4, 1) : {}'.format( round(2.4, 1) ))


# 파이썬에의 round() 함수 특징
# x.5
# 원래 값과 올림한 값의 차이 = 원래 값과 내림한 값의 차이가 같은 경우
# 짝수가 되는 크기로 올림 또는 내림한다.

print( round(0.5) )     # 1
print( round(1.5) )     # 2
print( round(2.5) )     # 3
print( round(3.5) )     # 4
print( round(4.5) )     # 5
print( round(5.5) )     # 6

print('----------------------')

print( round(0.6) )     # 1
print( round(1.6) )     # 2
print( round(2.6) )     # 3
print( round(3.6) )     # 4
print( round(4.6) )     # 5
print( round(5.6) )     # 6



# trunc() 절사 (특정 자리수 이하를 없앰)
print('trunc(1.9) : {}'.format( math.trunc(1.9) ))

# sqrt() 제곱근
print('sqrt(9) : {}'.format( math.sqrt(9) ))

# pow() 제곱
print('pow(9) : {}'.format( math.pow(3, 2) ))