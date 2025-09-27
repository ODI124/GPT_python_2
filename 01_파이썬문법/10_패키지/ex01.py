import requests

# GET 요청
response = requests.get("https://jsonplaceholder.typicode.com/posts/1")

if response.status_code == 200:
    data = response.json()
    print("제목:", data["title"])
else:
    print("요청 실패:", response.status_code)