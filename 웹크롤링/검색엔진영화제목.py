# 라이브러리 설치
# 터미널 >
# pip install requests
# pip install beautifulsoup4
# pip install lxml
 
import requests
from bs4 import BeautifulSoup

# 특정 사이트의 html 가져오기
url = "https://movie.naver.com/movie/bi/mi/basic.naver?code=74977"
html = requests.get(url)

# print(html)

# html 분석
soup = BeautifulSoup(html.text, 'lxml')

# 영화 제목
span = soup.find('span', class_='area_text_title')
strong = span.find('strong')
text = strong.get_text()
# print(h3)
# print(a)

print(span)
print(strong)
print(text)