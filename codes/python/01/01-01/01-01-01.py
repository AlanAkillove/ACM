# https://codeforces.com/problemset/problem/1328/A
t = int(input())
for _ in range(t):
    a, b = map(int, input().split())
    print((b - a % b) % b)