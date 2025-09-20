li = [100, 12.34, 'hello']
print('li : ', li)

print('li[0] :', li[0])
print('li[1] :', li[1])
print('li[2] :', li[2])

li2 = ['월', '화' ,'수' , '목','금', '토', '일']
print('li2[0:5] :', li2[0:5])
print('li2[5:7] :', li2[5:7])
print('li2[:5] :', li2[:5])
print('li2[5:] :', li2[5:])

# 요소 추가 및 삭제
# - 요소 추가함수           : append(), insert()
# - 요소 삭제함수           : pop()
# append()                  : 마지막에 요소 추가
print("### append() ###")
li3 = [1,2,3,4,5]
print(li3)
li3.append(6)
print(li3)
li3.append(7)
print(li3)

# insert(index, 추가할 요소)
# : 특정 index 에 요소 추가
print("### insert() ###")
li4 = [1,3,5,7,9]
print(li4)
li4.insert(1, 2)
print(li4)
li4.insert(3, 4)
print(li4)
li4.insert(5, 6)
print(li4)
li4.insert(7, 8)
print(li4)
# pop(index) 
# : 특정 index 를 지정하여 삭제
# * index 를 생략하면 마자막 요소 삭제
print('### pop() ###')
print(li4)
li4.pop()
li4.pop()
li4.pop()
li4.pop()
print(li4)
li4.pop(2)
print(li4)