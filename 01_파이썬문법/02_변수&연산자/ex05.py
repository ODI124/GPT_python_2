a=10
b=5

result1=a>7
result2=b>7
result3=a<7
result4=b<7

print('{}>7 and {} >7 : {}' .format(a,b, result1 and result2))
print('{}>7 or {} >7 : {}' .format(a,b, result1 or result2))
print('{}<7 and {} <7 : {}' .format(a,b, result3 and result4))
print('{}<7 or {} <7 : {}' .format(a,b, result3 or result4))

print('not:{}:{}'.format(a, not a))
print('not:{}:{}'.format(0, not 0))