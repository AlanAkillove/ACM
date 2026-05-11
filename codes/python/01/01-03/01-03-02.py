# https://codeforces.com/problemset/problem/1055/C
import math
# 计算区间重叠长度
def overlap(l1, r1, l2, r2):
    return max(0, min(r1, r2) - max(l1, l2) + 1)

la, ra, ta = map(int, input().split())
lb, rb, tb = map(int, input().split())
g = math.gcd(ta, tb)
# 找让两个区间起点最接近的2个最优偏移
delta = lb - la
shift1 = delta - delta % g  # 偏移1（向下取g的倍数）
shift2 = shift1 + g         # 偏移2（向上取g的倍数）

# 计算两种最优偏移下的重叠长度
ans = max(
    overlap(la + shift1, ra + shift1, lb, rb),
    overlap(la + shift2, ra + shift2, lb, rb)
)
print(ans)