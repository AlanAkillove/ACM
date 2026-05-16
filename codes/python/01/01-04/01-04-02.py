# https://www.luogu.com.cn/problem/B2138
MAXN = 5005
maxp = [0] * MAXN
for i in range(2, MAXN):
    if maxp[i] == 0:  
        maxp[i] = i
        for j in range(i * 2, MAXN, i):
            maxp[j] = i
m, n = map(int, input().split())
res = [str(maxp[x]) for x in range(m, n + 1)]
print(",".join(res))