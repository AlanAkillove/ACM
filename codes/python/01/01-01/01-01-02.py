# https://codeforces.com/problemset/problem/1472/B
t = int(input())
ans = []
for _  in range(t):
    n = int(input())
    a = [int(i) for i in input().split()]
    s = sum(a)
    if s & 1:
        ans.append("NO")
    else:
        cnt1 = a.count(1)
        if (s // 2) & 1 and cnt1 == 0:
            ans.append("NO")
        else:
            ans.append("YES")
print("\n".join(map(str, ans)))