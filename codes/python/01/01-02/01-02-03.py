# https://www.luogu.com.cn/problem/P1029
import math
x0, y0 = map(int, input().split())
cnt = 0
if y0 % x0 == 0: 
    k = y0 // x0
    for i in range(1, int(math.sqrt(k)) + 1):
        if k % i == 0:
            j = k // i
            if math.gcd(i, j) == 1:
                cnt += 1 if i == j else 2
print(cnt)