quiz = {
    1: {
        "question" : "순서가 없고 중복 불가능한 컬렉션은?",
        "choices" : ["1.리스트" , "2.튜플 ", "3.세트", "4.딕셔너리"]
    },
    2: {
        "question" : "다음 중 파이썬의 반복문은?",
        "choices" : ["1.loop" , "2.repeat ", "3.cycle", "4.while"]
    },
    3: {
        "question" : "다음 중 기타 제어문은?",
        "choices" : ["1.brake" , "2.break ", "3.break dance", "4.break time"]
    }
}

answer = {
    1 : 3,
    2 : 4,
    3 : 2
}

score = 0

for no, content in quiz.items():
    print("{}.{}".format( no, content['question']))
    
    for choice in content['choices']:
        print(' ' + choice)
    
    user = input("답 : ")
    
    if int(user) == answer[no]:
        print("정답입니다!")
        score = score + 10
    else:
        print("틀렸습니다. 정답은 {} 입니다.".format( answer[no]))
        
print("점수는 {} 점입니다.".format(score))