d = { 'a' : 'apple', 'b' : 'banana'}
print('d :', d)

print('d[\'a\'] : ',d['a'])
print('d[\'b\'] : ',d['b'])

# 딕셔너리에 요소 추가
d['c'] = 'melon'
print('d : ', d)
# 추가 방법2
d.setdefault('d', 'dog')
print('d : ', d)
# 딕셔너리 수정
d.update(d='cat')
print('d : ', d)
# 딕셔너리 삭제
d.pop('d')
print('d : ', d)