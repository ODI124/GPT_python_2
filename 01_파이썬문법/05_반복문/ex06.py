#r = random.choice(choices)
#print(r)
import random

choices = ['가위', '바위', '보']
user = ' '
win = True

while win :
    computer = random.choice(choices)
    user = input('가위바위보 입력:')
    print("컴퓨터 : " + computer)
    print("나 : " + user)
    
    # 이겼을 때
    win1 = (user == '가위' and computer == '보')
    win2 = (user == '바위' and computer == '가위')
    win3 = (user == '보' and computer == '바위')
    
    if win1 or win2 or win3:
        print("이겼습니다!")
    elif user == computer:
        print("비겼습니다!")
    else:
        win = False
        print("졌습니다!")