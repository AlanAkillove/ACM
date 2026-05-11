# https://www.luogu.com.cn/problem/P1424
x, n = map(int, input().split())
cnt = 0
for i in range(n):
    day = (x + i - 1) % 7 + 1
    cnt += 1 if 1 <= day <=5 else 0
print(cnt * 250)