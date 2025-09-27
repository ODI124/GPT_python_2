import datetime


# [모듈].[객체].함수()
nowtime = datetime.datetime.now()
print('현재 날짜와 시간 : {}'.format(nowtime))

today = datetime.date(2023, 1, 19)
print('현재 날짜와 시간 : {}'.format(today))

lastDay = datetime.date(2023, 6, 29)
print('종강일 : {}'.format(lastDay))

t1 = datetime.time(11,15,0)
print('현재시간 : {}'.format(t1)) 

t2 = datetime.time(15,30,0)
print('수업종료 : {}'.format(t2))

today = datetime.datetime.now()
print( datetime.datetime.today().strftime('%Y-%m-%d') )


print('{} 년'.format( today.year) )
print('{} 월'.format( today.month ) )
print( '%02d' % today.month )   # leading zero
print('{} 일'.format( today.day) )
print('{} 시'.format( today.hour) )
print('{} 분'.format( today.minute) )
print('{} 초'.format( today.second) )

#오늘 날짜
today = datetime.datetime.today()

#종강일
last_day = datetime.datetime(2025,10,25)

#남은 시간 계산
gap = last_day - today

print("종강일까지 {}일 남았습니다.".format(gap.days))

gap_seconds = gap.total_seconds()
gap_hours = gap_seconds / 3600
gap_mins = gap_seconds / 60
print("남은시간 : {}시".format( int(gap_hours)))
print("남은시간 : {}분".format( int(gap_mins)))
print("남은시간 : {}초".format( int(gap_seconds)))
