import matplotlib.pyplot as plt

# 샘플 데이터
x = [1, 2, 3, 4, 5]
y = [10, 20, 15, 30, 25]

# 선 그래프 그리기
plt.plot(x, y, marker="o")
plt.title("샘플 선 그래프")
plt.xlabel("X축")
plt.ylabel("Y축")
plt.grid(True)
plt.show()