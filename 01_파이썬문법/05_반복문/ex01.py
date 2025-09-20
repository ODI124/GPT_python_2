i= 1
while i <=10:
    print(i, end=' ')
    i=i+1
print()

a = 1
sum = 0
while a<= 10:
    sum = sum + a
    print(a, end=' ')
    
    if a != 10:
        print("+", end=' ')
    a = a+1
print("={}".format(sum))
print("sum = {}".format(sum))