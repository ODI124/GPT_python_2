def getStudent(no, name, major):
    student = {
        'no': no,
        'name': name,
        'major': major
    }
    return student

no = input('학번 : ')
name = input('이름 : ')
major = input('전공명 : ')

student = getStudent(no, name, major)

# TODO: 출력문 내부를 완성하시오.
print('학번 : {}'.format(student['no']))
print('이름 : {}'.format(student['name']))
print('전공 : {}'.format(student['major']))