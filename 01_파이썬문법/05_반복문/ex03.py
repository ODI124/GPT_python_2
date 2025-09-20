menu = ["샌드위치", "김밥", "컵라면", "햄버거"]
for food in menu:
    print("오늘 점심 메뉴는 : {}".format(food))
print()

stars = ("마동석", "김태리", "박보검", "강하늘", "이정재")
for star in stars:
    print("오늘의 스타는 : {}".format(star))
print()

burger_king_set = {"와퍼", "프랜치프라이", "콜라"}
for item in burger_king_set:
    print(item)
print()

users = {
    "joeun" : "123456",
    "user"  : "user1004",
    "admin" : "1q2w3e"
}
for id, pw in users.items():
    print("아이디 : {}, 비밀번호 : {}".format(id, pw))