s1 = {1,2,3,4,5}
print(s1)

# 요소 추가 : add()
# 요소 삭제 
# - remove()    : 없으면 에러⭕
# - discard()   : 없어도 에러❌
s1.add(6)
print(s1)
s1.add(7)
print(s1)
s1.add(8)
print(s1)
# 중복된 값은 추가하지 않는다.
s1.add(5)
s1.add(5)
print(s1)
# 세트에서는 값을 찾아서 삭제한다
s1.remove(8)
print(s1)
s1.discard(7)
print(s1)
# s1.remove(10)  # 에러⭕
s1.discard(10)   # 에러❌