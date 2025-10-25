import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, 
                           QTextEdit, QLabel, QMainWindow)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from datetime import datetime, date
import calendar

class HolidayAnalyzer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # 메인 위젯과 레이아웃 설정
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # 2025년 법정 공휴일
        self.holidays = {
            (1, 1): "신정",
            (3, 1): "삼일절",
            (5, 5): "어린이날",
            (6, 6): "현충일",
            (8, 15): "광복절",
            (10, 3): "개천절",
            (10, 9): "한글날",
            (12, 25): "크리스마스"
        }
        
        # 2025년 설날과 추석 (음력 기준 양력 날짜)
        self.lunar_holidays = {
            (1, 28): "설날 연휴",
            (1, 29): "설날",
            (1, 30): "설날 연휴",
            (10, 6): "추석 연휴",
            (10, 7): "추석",
            (10, 8): "추석 연휴"
        }
        
        # UI 구성요소
        title = QLabel('2025년 공휴일 분석 프로그램')
        title.setFont(QFont('맑은 고딕', 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel('공휴일과 주말을 포함한 빨간날 분석')
        subtitle.setFont(QFont('맑은 고딕', 10))
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        analyze_btn = QPushButton('빨간날 분석하기')
        analyze_btn.setFont(QFont('맑은 고딕', 11))
        analyze_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF6B6B;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #FF5252;
            }
        """)
        analyze_btn.clicked.connect(self.analyze_holidays)
        layout.addWidget(analyze_btn)
        
        self.result_text = QTextEdit()
        self.result_text.setFont(QFont('맑은 고딕', 10))
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_text)
        
        # 윈도우 설정
        self.setWindowTitle('2025년 빨간날 분석기')
        self.setGeometry(300, 300, 600, 500)
        self.setStyleSheet("background-color: white;")
        
    def analyze_holidays(self):
        result = []
        total_holidays = 0
        weekday_count = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}  # 월~일
        weekday_names = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
        
        # 월별 분석
        for month in range(1, 13):
            month_holidays = []
            
            # 해당 월의 모든 날짜 확인
            cal = calendar.monthcalendar(2025, month)
            for week in cal:
                for i, day in enumerate(week):
                    if day == 0:
                        continue
                    
                    current_date = (month, day)
                    weekday = date(2025, month, day).weekday()
                    is_holiday = False
                    holiday_name = ""
                    
                    # 주말 체크
                    if weekday in [5, 6]:  # 토요일(5), 일요일(6)
                        is_holiday = True
                        holiday_name = "주말"
                    
                    # 공휴일 체크
                    elif current_date in self.holidays:
                        is_holiday = True
                        holiday_name = self.holidays[current_date]
                    
                    # 설날/추석 체크
                    elif current_date in self.lunar_holidays:
                        is_holiday = True
                        holiday_name = self.lunar_holidays[current_date]
                    
                    if is_holiday:
                        weekday_count[weekday] += 1
                        total_holidays += 1
                        if holiday_name != "주말":
                            month_holidays.append(f"{month}월 {day}일 ({weekday_names[weekday]}): {holiday_name}")
            
            if month_holidays:
                result.append(f"\n[{month}월 공휴일]")
                result.extend(month_holidays)
        
        # 결과 텍스트 구성
        final_result = [
            "📅 2025년 빨간날 분석 결과",
            "=" * 40,
            f"🔴 총 빨간날 수: {total_holidays}일",
            "\n📊 요일별 빨간날 통계:"
        ]
        
        for i, count in weekday_count.items():
            if count > 0:
                final_result.append(f"- {weekday_names[i]}: {count}일")
        
        final_result.append("\n📌 월별 공휴일 목록 (주말 제외)")
        final_result.extend(result)
        
        # 결과 출력
        self.result_text.setText("\n".join(final_result))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # 기본 폰트 설정
    font = QFont('맑은 고딕', 10)
    app.setFont(font)
    
    ex = HolidayAnalyzer()
    ex.show()
    sys.exit(app.exec_())
