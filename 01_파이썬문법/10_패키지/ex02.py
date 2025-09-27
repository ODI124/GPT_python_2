import pandas as pd

# 간단한 데이터프레임 생성
data = {
    "name": ["Alice", "Bob", "Charlie"],
    "age": [20, 22, 23],
    "major": ["CS", "Math", "Physics"]
}

df = pd.DataFrame(data)

print("데이터프레임 출력:")
print(df)

# 나이 평균
print("\n평균 나이:", df["age"].mean())