# https://www.luogu.com.cn/problem/P5253
n = int(input())
total = 1  # 存储n²的因数总个数
i = 2
# 试除法分解质因数
while i * i <= n:
    if n % i == 0:
        cnt = 0  # 统计当前质因子的指数
        while n % i == 0:
            cnt += 1
            n = n // i
        # 总因数个数 *= (2*指数 +1)
        total *= (2 * cnt + 1)
    i += 1
if n > 1:
    total *= 3

ans = (total + 1) // 2
print(ans)