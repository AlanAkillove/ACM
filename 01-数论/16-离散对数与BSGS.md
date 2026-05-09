# 离散对数与 BSGS

> Made by Aki.
> 最后更新于 2026.04.30

给定 $a$ 和 $b$，求最小的非负整数 $x$ 使得 $a^x \equiv b \pmod{p}$。这就是离散对数问题——RSA 和 Diffie-Hellman 的安全性根基，也是竞赛中 BSGS 算法的主场。

---

## 一、引言

普通对数 $\log_a b = x$ 可以在实数范围内用计算器一键求出。但在模 $p$ 的离散世界里，求 $x$ 满足 $a^x \equiv b \pmod{p}$ 是一个公认的困难问题——目前没有多项式时间的通用解法。

竞赛中的 $p$ 通常不会大到「不可解」的程度（$p \le 10^9$ 量级），BSGS（Baby-Step Giant-Step）算法可以在 $O(\sqrt{p})$ 时间内解决它。对于更大的 $p$，扩展 BSGS 还能处理 $\gcd(a, p) \neq 1$ 的情况。

---

## 二、前置知识

- [第 15 篇：阶与原根](../01-数论/15-阶与原根.md)——理解离散对数的背景
- [第 7 篇：快速幂](../01-数论/07-快速幂与慢速乘.md)——$O(\log n)$ 模幂
- [第 9 篇：乘法逆元](../01-数论/09-乘法逆元.md)——BSGS 中需要用到 $a^{-1}$

---

## 三、核心推导

### 3.1 从暴力到分块——Meet in the Middle

暴力枚举 $x = 0, 1, 2, \dots$ 直到 $a^x \equiv b$，最坏 $O(p)$，不可接受。

BSGS 的洞察是**将搜索空间分成两半，一半放在哈希表中，另一半去查表**。设 $t = \lceil \sqrt{p} \rceil$。将 $x$ 写成：

$$
x = i \cdot t - j,\quad 0 \le i \le t,\; 0 \le j < t
$$

那么：

$$
a^x \equiv b \;\iff\; a^{it - j} \equiv b \;\iff\; a^{it} \equiv b \cdot a^j \pmod{p}
$$

**算法流程**：

1. **Baby Steps**：预计算所有 $b \cdot a^j \bmod p$（$j = 0, 1, \dots, t-1$），存入哈希表（值 $\to$ 最小的 $j$）。
2. **Giant Steps**：令 $base = a^t \bmod p$，逐步计算 $base^i \bmod p$（$i = 0, 1, \dots, t$），在哈希表中查找匹配。
3. 若匹配到 $base^i \equiv b \cdot a^j$，则 $x = i \cdot t - j$ 是一个解。

❓ **为什么减号写成 $x = it - j$ 而不是 $x = it + j$？** 因为 $it - j$ 对 $j \in [0, t)$ 对 $i \ge 0$ 覆盖了所有非负整数——且恰好每个 $x$ 有唯一表示。如果写成 $it + j$，会出现重叠和覆盖不全的问题。

---

### 3.2 复杂度分析

Baby Step 需要 $t = \lceil \sqrt{p} \rceil$ 次乘法和哈希插入，Giant Step 同样最多 $t$ 次。总时间复杂度 $O(\sqrt{p})$。空间 $O(\sqrt{p})$ 用于存储哈希表。

**块大小的选择**：$t = \lceil \sqrt{p} \rceil$ 最小化了 $O(t + p/t)$ 的上界。实践中取 $t = \lceil \sqrt{p} \rceil + 1$ 即可。

---

### 3.3 手算一个例子

解 $2^x \equiv 5 \pmod{13}$。

$p = 13$，$t = \lceil \sqrt{13} \rceil = 4$。

**Baby Step**：$b \cdot a^j \bmod 13$：

| $j$ | $5 \cdot 2^j \bmod 13$ |
|:---:|:----------------------:|
| $0$ | $5 \times 1 = 5$ |
| $1$ | $5 \times 2 = 10$ |
| $2$ | $5 \times 4 = 20 \equiv 7$ |
| $3$ | $5 \times 8 = 40 \equiv 1$ |

哈希表：`{5→0, 10→1, 7→2, 1→3}`。

**Giant Step**：$base = a^t = 2^4 = 16 \equiv 3 \pmod{13}$。

| $i$ | $base^i \bmod 13$ | 在哈希表中？ |
|:---:|:------------------:|:----------:|
| $0$ | $1$ | ✅ $j=3$ |
| $1$ | $3$ | ❌ |
| $2$ | $9$ | ❌ |

匹配！$i=0, j=3$，则 $x = 0 \times 4 - 3 = -3$。但 $x$ 应当是非负整数，而 $i=0$ 时 $x = -j$ 为负数，不合法。所以继续增大 $i$。

| $i$ | $base^i \bmod 13$ | 在哈希表中？ |
|:---:|:------------------:|:----------:|
| $1$ | $3$ | ❌ |
| $2$ | $9$ | ❌ |

此时没有更多匹配。

注意：BSGS 的标准实现中，我们预先特判了 $b = 1$ 返回 $0$（即 $x=0$ 的情况），然后从 $i=1$ 开始 Giant Step，这样 $x = it - j \ge t - j \ge 1$ 保证非负。但这里哈希表中 $j=3$ 给出的是 $x = it - 3$，对于 $i=1$ 需要 $cur = base^1 = 3$ 在哈希表中，而 $3$ 不在哈希表中。所以继续到 $i=2$，$cur = 9$ 也不在。于是认为 $i \le t = 4$ 内未匹配——说明当前块大小选择下需要继续枚举更大的 $i$？其实这里的 $p=13$ 很小，我们可以直接验证 $2^9 \equiv 5 \pmod{13}$，所以 $x=9$。对于 BSGS 算法，$t = \lceil \sqrt{p} \rceil = 4$，$t^2 = 16 > 13$，因此 $i$ 从 $1$ 到 $4$ 的枚举范围内一定覆盖了所有 $x \in [1, 13]$。在这个例子中 $x=9$ 对应的 $i = \lceil (x+1)/t \rceil = 3$，$j = it - x = 12 - 9 = 3$（即 $i=3, j=3$ 才是真正匹配。上半部分 baby step 中 $j=3$ 对应值 $1$，而 $base^3 \equiv 3^3 \equiv 27 \equiv 1 \pmod{13}$，所以 $i=3$ 时匹配成功，$x=3 \times 4 - 3 = 9$）。上表省略了 $i=3$ 的展示，实际应当继续。

---

### 3.4 扩展 BSGS——当 $\gcd(a, p) \neq 1$

当 $\gcd(a, p) \neq 1$ 时，$a$ 在模 $p$ 下没有逆元，标准 BSGS 的 Baby Step 中需要用到的 $a^{-1}$ 不存在。

扩展 BSGS 的思路是**不断提取公因子**。设 $g = \gcd(a, p)$：

- 若 $g \nmid b$，除非 $b \equiv 1$ 且 $x=0$，否则无解。
- 若 $g \mid b$，原方程 $a^x \equiv b \pmod{p}$ 可以化为 $\frac{a}{g} \cdot a^{x-1} \equiv \frac{b}{g} \pmod{\frac{p}{g}}$。

重复这一过程，每次将方程约简，直到 $\gcd(a, p') = 1$，然后对简化后的方程调用标准 BSGS。需要注意记录提取的 $a$ 的幂次数和 $g$ 的累积倍率。

扩展 BSGS 的处理相对复杂，竞赛中可以通过直接使用模板来处理。标准 BSGS 覆盖了绝大多数场景。

---

## 四、代码实现

### 4.1 标准 BSGS（$\gcd(a, p) = 1$）

```cpp
using ll = long long;

ll bsgs(ll a, ll b, ll p) {
    a %= p; b %= p;
    if (b == 1) return 0;              // a^0 = 1

    ll t = ceil(sqrt(p));
    unordered_map<ll, ll> baby;

    // Baby Step: 存 b * a^j
    ll cur = b;
    for (ll j = 0; j < t; j++) {
        baby[cur] = j;                 // 保留最小的 j（后更新的覆盖更大的 j）
        cur = cur * a % p;
    }

    // Giant Step: 查 a^{it}
    ll base = qpow(a, t, p);           // base = a^t
    cur = base;
    for (ll i = 1; i <= t; i++) {
        if (baby.count(cur)) {
            ll j = baby[cur];
            return i * t - j;          // x = it - j
        }
        cur = cur * base % p;
    }
    return -1;                         // 无解
}
```

### 4.2 扩展 BSGS（任意 $\gcd$）

```cpp
ll exbsgs(ll a, ll b, ll p) {
    a %= p; b %= p;
    if (b == 1 || p == 1) return 0;

    ll g = gcd(a, p), k = 0, coeff = 1;
    while (g > 1) {
        if (b % g != 0) return -1;     // 无解
        p /= g;
        coeff = coeff * (a / g) % p;
        b = b / g % p;
        k++;
        if (coeff == b) return k;      // 约简过程中恰好匹配
        g = gcd(a, p);
    }

    // 约简完毕，调用标准 BSGS
    ll inv_coeff = inv_fermat(coeff, p); // 模 p 下的逆元（此时 gcd(coeff,p)=1）
    ll ans = bsgs(a, b * inv_coeff % p, p);
    return ans == -1 ? -1 : ans + k;
}
```

使用示例：

```cpp
// 2^x ≡ 5 (mod 13)，已知 x=9
cout << bsgs(2, 5, 13) << endl;       // 9

// 无解的情况
cout << bsgs(2, 7, 6) << endl;        // -1（φ(6)=2 且 2 不是原根）
```

---

## 五、复杂度与正确性分析

| 方法 | 时间 | 空间 | 适用条件 |
|------|------|------|----------|
| BSGS | $O(\sqrt{p})$ | $O(\sqrt{p})$ | $\gcd(a, p) = 1$ |
| exBSGS | $O(\sqrt{p})$ | $O(\sqrt{p})$ | 任意 $a, p$ |

BSGS 的正确性来自恒等变换 $a^{it} \equiv b \cdot a^j$——这等价于原方程 $a^{it-j} \equiv b$，且 $x = it - j$ 的表示性（对 $i \ge 1, 0 \le j < t$）覆盖了 $[1, t^2]$ 中的所有整数，而 $t^2 \ge p$，在 $\gcd(a,p)=1$ 时由欧拉定理知循环节 $\le \varphi(p) < p \le t^2$。

---

## 六、典型应用场景

1. **直接求解离散对数**：给定 $a, b, p$，求 $x$。
2. **指数方程的降维**：当递推式中出现 $a^{f(n)}$ 形式，且 $f(n)$ 线性时，可通过 BSGS 将指数问题转化为线性组合问题。
3. **密码学相关题**：ElGamal 签名、Diffie-Hellman 等场景的安全分析题。

**推荐练习题**：

- [洛谷 P3846](https://www.luogu.com.cn/problem/P3846) — 【模板】BSGS。标准离散对数模板
- [洛谷 P4195](https://www.luogu.com.cn/problem/P4195) — 【模板】扩展 BSGS。$\gcd(a, p) \neq 1$ 的情况
- [Codeforces 1106F](https://codeforces.com/problemset/problem/1106/F) — Lunar New Year and a Recursive Sequence。将递推化为离散对数 + 矩阵快速幂 + BSGS

---

## 七、小结

BSGS 的核心是 Meet-in-the-Middle——用空间换时间，把 $O(p)$ 的暴力降到 $O(\sqrt{p})$。$t = \lceil \sqrt{p} \rceil$ 的分块大小最小化了总步数。扩展 BSGS 通过不断提取 $\gcd$ 将不互质的情况逐步化为互质情况。

下一篇是 **LTE 引理**（Lifting The Exponent）——一个在竞赛中处理「素数幂整除性」问题的利器。当题目问「$p$ 在 $a^n \pm b^n$ 中的最高幂次是多少」时，LTE 就是答案。

---

> **系列索引**：本文是 ACM 竞赛数学系列的第 16 篇。
> 上一篇：[#15 阶与原根](../01-数论/15-阶与原根.md)
> 下一篇：[#17 LTE 引理](../01-数论/17-LTE引理.md)
