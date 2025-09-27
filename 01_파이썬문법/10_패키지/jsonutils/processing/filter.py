'''
    리스트 필터링 함수
'''
def filter_by_field(data, field, value):
    # list 인스턴스가 아닐 때
    if not isinstance(data, list):
        # raise : 예외 강제 발생 키워드
        # ValueError : 적절한 값이 아닌 경우 발생하는 예외
        raise ValueError("리스트 형식이 아닙니다.")
    return [ item for item in data if item.get(field) == value ]
    