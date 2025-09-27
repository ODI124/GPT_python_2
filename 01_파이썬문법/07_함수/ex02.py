# 숫자 맞추기 게임

import random

def guess_number():
    answer = random.randint(1, 10) # 1~10 까지 랜덤 수
    count = 0 
    
    while True:
        guess = int(input("입력 : "))
        count += 1
        if guess < answer:
            print("UP")
        elif guess > answer:
            print("DOWN")
        else:
            print("정답입니다! 시도 횟수 : {}".format(count))
            break
        
# 함수 호출
guess_number()
