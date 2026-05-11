# https://www.luogu.com.cn/problem/B3736
def gcd(a, b):
    while b != 0:
        r = a % b
        a = b
        b = r
    return a
x, y, z = map(int, input().split())
print(gcd(gcd(x, y), z))