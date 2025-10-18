import pytesseract
from PIL import Image

# Tesseract 실행 파일 경로 설정
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 이미지 불러오기
image = Image.open('text2.png')

# 이미지에서 텍스트 추출 (한국어 + 영어)
text = pytesseract.image_to_string(image, lang='eng+kor')

# 추출된 텍스트 출력
print(text)