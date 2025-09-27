# converter 모듈 
# : 규격이나 단위를 변환하는 함수를 제공하는 모듈
import converter
# from converter import *

# 150km  -->  miles 로 변환
miles = converter.kilometer_to_miles(150)
print( '150km = {} miles'.format(miles) )

# 1000g --> pound 로 변환
pound = converter.gram_to_pound(1000)
print('1000g = {} pound'.format(pound) )
