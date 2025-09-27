from jsonutils import read_json, filter_by_field, save_json

#student.json 파일 열기
data = read_json('student.json')

#gender가female인 데이터만 필터링
filtered = filter_by_field(data, 'gender', 'female')

#filtered.json 파일로 저장
save_json(filtered, 'filtered.json')
