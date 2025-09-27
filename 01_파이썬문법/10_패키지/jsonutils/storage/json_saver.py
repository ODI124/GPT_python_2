import json
'''
   JSON 데이터 저장 함수
'''
def save_json(data, filepath):
    # 쓰기 모드로 파일 열기
    with open(filepath, 'w', encoding='utf-8') as f:
        # data 를 JSON 형식으로 파일 저장
        # ensure_ascii : False 아스키 문자가 아닌 것도 그대로 저장
        # indent : 들여쓰기를 2칸으로 지정
        json.dump(data, f, ensure_ascii=False, indent=2)