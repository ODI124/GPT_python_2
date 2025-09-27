'''
시퀀스 내장 함수
1. enumerate() 함수
    : 리스트와 함께 사용하여,  
     (index, 요소) 형태로 튜플로 반환하는 함수
    ex) for item in enumerate( ['a','b','c'] )
            print(item)
        (결과)
        (0, 'a')
        (1, 'b')
        (2, 'c')
        
2. range() 함수
    : 전달받은 값에 따라서 특정 범위에 데이터를 반환하는 함수
    
    i) range(끝)
    : 0부터 (끝-1)에 지정하는 번호까지 정수를 생성
    
    ii) range(시작, 끝)
    : 시작부터 (끝-1)에 사이의 모든 정수를 생성
    
    iii) range(시작, 끝, 단계)
    : 시작부터 (끝-1)에 사이의 수들을 단계의 크기만큼 증감하여 생성
    
    
3. len() 함수
    : 함수의 전달된 객체의 길이(개수) 반환하는 함수
    ex) li = [1,2,3,4]
      len(li) --> 4
    
4. sorted() 함수
    : 반복가능한 객체를 오름차순으로 정렬한 결과를 반환하는 함수
    ex) li = [10, 3, 9, 2, 5]
        sorted(li) --> [2, 3, 5, 9, 10]
        
5. zip() 함수
    : 여러 개의 반복가능한 객체들을 요소끼리 묶어서 반환하는 함수
    ex) names = [ 'C', 'JAVA', 'PYTHON' ]
        scores = [ 100, 90, 80 ]
        zip( names, scores )
        --> ('C', 100),
            ('JAVA', 90),
            ('PYTHON', 80)
    
'''

# C언어, Python, Java
# 0, 1, 2
# enumerate(  )
'''
    (0, 'C언어'),
    (1, 'Python'),
    (2, 'Java'),
'''
prog = ['C언어', 'Python', 'Java']
for item in enumerate(prog):
    print(item)
print()
for item in enumerate(prog):
    print('{}. {}'.format( item[0]+1, item[1] ))
print()
    
    
# range(10)     : 0 1 2 3 4 5 6 7 8 9
for i in range(10):
    print(i, end=' ')
print()
# range(1,11)     : 1 2 3 4 5 6 7 8 9 10
for i in range(1, 11):
    print(i, end=' ')
print()
# range( ?, ?, ? )
# 1 3 5 7 9 11 13 15 17 19
for i in range(1, 20, 2):
    print(i, end=' ')
print()
# 2 4 6 8 10 12 14 16 18 20
for i in range(2, 21, 2):
    print(i, end=' ')
print()

# len
li = ['월','화','수','목','금','토','일']
print(li)
print('li 의 요소의 개수 : {}'.format( len(li) ))
# sorted
# * 원본은 바뀌지 않는다!
# - 해당 리스트를 정렬한 새 리스트를 반환하는 함수
# sorted( 리스트, reverse=False )   : 오름차순
# sorted( 리스트, reverse=True )    : 내림차순
scores = [100, 90, 65, 80, 70]
print(scores)
print( sorted(scores) )
print( sorted(scores, reverse=True) )
print( sorted(scores, reverse=False) )
print(scores)
# sort
# * 원본을 정렬 해준다!
# - 해당 리스트를 정렬하여 갱신하는 함수
# 리스트.sort(reverse=False)       : 오름차순
# 리스트.sort(reverse=True)        : 내림차순
scores.sort(reverse=True)
print(scores)
scores.sort(reverse=False)
print(scores)
# zip
names = ['s1','s2','s3','s4','s5']
scores = [100, 90, 65, 80, 70]
for student in zip(names, scores):
    print(student)