# https://www.luogu.com.cn/problem/P5736
import math

def isPrime(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

n = int(input())
a = [int(i) for i in input().split()]
for i in range(n):
    if isPrime(a[i]):
        print(a[i], end=' ')

