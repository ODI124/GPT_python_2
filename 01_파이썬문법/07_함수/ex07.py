def print_user_info(**kwargs):
    print("전달받은 사용자 정보 :", kwargs)
    # kwargs 는 딕셔너리 형태로 전달됨
    for key, value in kwargs.items():
        print(f"{key} = {value}")

#호출
print_user_info(name="김조은", age="20")
print_user_info(name="김조은", age="20", city="인천")