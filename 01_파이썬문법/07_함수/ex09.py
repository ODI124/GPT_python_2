# 키워드 전용 매개변수

def order(*, item, size, quantity):
    print("주문한 음료 정보")
    print("item : {}".format(item))
    print("size : {}".format(size))
    print("quantity : {}".format(quantity))
    
order(item="아메리카노", size="V", quantity=20)