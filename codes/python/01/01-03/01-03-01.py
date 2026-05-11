# https://www.luogu.com.cn/problem/P4549
from math import gcd
n = int(input())
outs = []
nums = [abs(int(i)) for i in input().split()]
ans = 0
for i in range(n):
    ans = gcd(nums[i],ans)
outs.append(ans)   
print('\n'.join(map(str,outs)))