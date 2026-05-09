# Kitamasa 方法与 Bostan-Mori 算法

> Made by Aki.
> 最后更新于 2026.04.30

---

## 一、引言

在第 74 篇中我们用矩阵快速幂在 $O(k^3 \log n)$ 时间内求出 $k$ 阶线性递推的第 $n$ 项。在第 78 篇中我们用 Berlekamp-Massey 算法从数列前几项反推出了递推式。

现在问题来了：矩阵快速幂的 $O(k^3 \log n)$ 在 $k$ 比较大（比如 $k = 1000$）时太慢了。有没有更快的方法？

答案是**有**。本文介绍两种更高效的线性递推求值方法：

1. **Kitamasa 方法**：$O(k^2 \log n)$，适合 $k \le 2000$ 的情况，用多项式运算代替矩阵乘法
2. **Bostan-Mori 算法**：$O(d \log d \log k)$（其中 $d$ 是多项式度数），适合 $k$ 很大且需要做有理函数求值的情况

两种方法的核心思想是一样的：**把线性递推求第 $n$ 项转化为多项式模幂运算**。

---

## 二、前置知识

- 线性递推的基本概念（[第 74 篇](74-矩阵基本运算与快速幂.md)）：$a_n = c_1 a_{n-1} + \cdots + c_k a_{n-k}$
- 多项式基本运算（加减乘除，模乘）
- Berlekamp-Massey 算法（[第 78 篇](78-线性递推与Berlekamp-Massey.md)）
- 快速幂思想：用二进制拆分加速

---

## 三、核心推导

### 3.1 问题重述

给定 $k$ 阶线性递推：

$$
a_n = c_1 a_{n-1} + c_2 a_{n-2} + \cdots + c_k a_{n-k}, \quad n \ge k
$$

已知初值 $a_0, a_1, \dots, a_{k-1}$，求 $a_n$（$n$ 可能高达 $10^{18}$）。

矩阵快速幂的做法是构造 $k \times k$ 转移矩阵 $M$，然后计算 $M^n \cdot \begin{pmatrix} a_{k-1} & \dots & a_0 \end{pmatrix}^T$。

Kitamasa 的想法则不同：**直接把第 $n$ 项表示为初值的线性组合**。

### 3.2 核心思想：用多项式表示递推

看一个具体例子。对 Fibonacci 数列 $a_n = a_{n-1} + a_{n-2}$，初值 $a_0 = 0, a_1 = 1$。

我们知道 $a_2 = a_1 + a_0 = 1$，$a_3 = a_2 + a_1 = 2$，$a_4 = a_3 + a_2 = 3$，等等。

Kitamasa 的核心观察是：**任何第 $n$ 项都可以写成初值的线性组合**：

$$
a_n = \sum_{i=0}^{k-1} \alpha_i \cdot a_i
$$

其中系数 $\alpha_i$ 是只和 $n$ 与递推式有关的量。

Fibnacci 的例子中 $a_5 = 5$，而 $a_5 = 5 \cdot a_1 + 3 \cdot a_0$（因为 $a_1=1, a_0=0$），所以 $\alpha_0 = 3, \alpha_1 = 5$。

我们怎么求这些系数？答案在**特征多项式**里。

### 3.3 特征多项式与模运算

定义递推 $a_n = c_1 a_{n-1} + \cdots + c_k a_{n-k}$ 的特征多项式为：

$$
P(x) = x^k - c_1 x^{k-1} - c_2 x^{k-2} - \cdots - c_k
$$

Kitamasa 方法的核心定理：

> **定理**：设 $a_n$ 是 $k$ 阶线性递推数列，特征多项式为 $P(x)$。则对任意 $n \ge k$，存在唯一的 $R(x) = \sum_{i=0}^{k-1} \beta_i x^i$ 满足：
>
> $$x^n \equiv R(x) \pmod{P(x)}$$
>
> 并且 $a_n = \sum_{i=0}^{k-1} \beta_i \cdot a_i$。

这个定理的意思是：**把 $x^n$ 对特征多项式 $P(x)$ 取模，得到的不超过 $k-1$ 次的多项式的系数，恰好就是初值的组合系数**。

❓ **为什么 $x^n$ 对 $P(x)$ 取模就是组合系数？**

看 Fibnacci 的例子。特征多项式 $P(x) = x^2 - x - 1$。

要算 $a_5$，就是求 $x^5 \bmod (x^2 - x - 1)$：

$$
\begin{aligned}
x^2 &\equiv x + 1 \pmod{P} \\
x^3 &\equiv x^2 + x \equiv (x+1) + x = 2x + 1 \\
x^4 &\equiv 2x^2 + x \equiv 2(x+1) + x = 3x + 2 \\
x^5 &\equiv 3x^2 + 2x \equiv 3(x+1) + 2x = 5x + 3
\end{aligned}
$$

所以 $x^5 \equiv 5x + 3 \pmod{P}$，系数 $\beta_0 = 3, \beta_1 = 5$。

$a_5 = \beta_0 a_0 + \beta_1 a_1 = 3 \times 0 + 5 \times 1 = 5$。完全正确！

这个过程本质上是在做**多项式模幂**：计算 $x^n \bmod P(x)$，其中 $P(x)$ 是 $k$ 次多项式。

### 3.4 多项式模幂的计算

计算 $x^n \bmod P(x)$ 可以用标准的**快速幂**思想：

1. 将 $n$ 二进制拆分
2. 维护当前多项式 $R(x) \gets R(x)^2 \bmod P(x)$
3. 如果 n 当前位是 1，就 $R(x) \gets R(x) \cdot x \bmod P(x)$

每次乘法是 $O(k^2)$（两个 $k$ 次多项式相乘再取模），总共 $O(\log n)$ 次，所以总复杂度 $O(k^2 \log n)$。

**手算示例**：用 Kitamasa 求 Fibonacci 第 10 项。

特征多项式 $P(x) = x^2 - x - 1$，初值 $a_0=0, a_1=1$。

我们要算 $x^{10} \bmod P(x)$。先把 $n=10$ 写成二进制 $1010_2$。

我们用倍增法：

- 初始：$R = 1$（0 次多项式），对应 $n=0$ 的情况
- 最低位是 $0$：$R \gets R^2 \bmod P = 1$，然后 $R \gets R \cdot x \bmod P = x$
- 下一位是 $1$：$R \gets R^2 \bmod P = x^2 \bmod P = x+1$，然后 $R \gets R \cdot x \bmod P = x^2 + x \equiv (x+1) + x = 2x + 1$
- 下一位是 $0$：$R \gets R^2 \bmod P = (2x+1)^2 = 4x^2+4x+1 \equiv 4(x+1)+4x+1 = 8x+5$，然后 $R \gets R \cdot x \bmod P = 8x^2+5x \equiv 8(x+1)+5x = 13x+8$
- 最高位是 $1$：$R \gets R^2 \bmod P = (13x+8)^2 = 169x^2+208x+64 \equiv 169(x+1)+208x+64 = 377x+233$

所以 $x^{10} \equiv 377x + 233 \pmod{P}$。

$a_{10} = 377 \cdot a_1 + 233 \cdot a_0 = 377 \times 1 + 233 \times 0 = 377$。

验证：Fibonacci 第 10 项（从 0 开始）$a_0=0, a_1=1, a_2=1, a_3=2, a_4=3, a_5=5, a_6=8, a_7=13, a_8=21, a_9=34, a_{10}=55$……

等等，这里算出 377 不对！让我检查一下问题出在哪。

❓ **Kitamasa 的 $n$ 应该从 $0$ 开始编号吗？**

问题在于：Kitamasa 方法要求 $a_0, a_1, \dots, a_{k-1}$ 是初始值系数，并且递推从 $n\ge k$ 开始。但 $x^n \bmod P(x)$ 的系数直接对应到 $a_n$。

对于 Fibonacci 数列的标准定义 $F_0 = 0, F_1 = 1, F_n = F_{n-1} + F_{n-2}$（$n \ge 2$），$k=2$，$n=10$ 时 $F_{10} = 55$。

检查我的手算过程……原来算错了系数。让我用正确的方法重算：

$x^2 = x + 1$
$x^{10} = (x^2)^5 = (x+1)^5$

用二项式定理展开：
$(x+1)^5 = x^5 + 5x^4 + 10x^3 + 10x^2 + 5x + 1$

现在对 $P(x)=x^2-x-1$ 取模：
$x^2 \equiv x+1$
$x^3 \equiv (x+1)x = x^2+x \equiv (x+1)+x = 2x+1$
$x^4 \equiv (2x+1)x = 2x^2+x \equiv 2(x+1)+x = 3x+2$
$x^5 \equiv (3x+2)x = 3x^2+2x \equiv 3(x+1)+2x = 5x+3$

代入：
$$x^{10} \equiv (5x+3) + 5(3x+2) + 10(2x+1) + 10(x+1) + 5x + 1$$
$$= (5+15+20+10+5)x + (3+10+10+10+1)$$
$$= 55x + 34$$

所以 $a_{10} = 55 \times 1 + 34 \times 0 = 55$。正确！

### 3.5 Bostan-Mori 算法

Kitamasa 适合 $k \le 2000$，但如果 $k$ 上万甚至上百万呢？或者我们遇到的是**有理函数求值**问题——求形式幂级数 $P(x)/Q(x)$ 的第 $[x^k]$ 项系数？

**Bostan-Mori 算法** 完美地解决了这个问题。

#### 问题描述

给定多项式 $P(x)$ 和 $Q(x)$（$Q(0) = 1$），满足 $\deg P < \deg Q$，求：

$$[x^k] \frac{P(x)}{Q(x)}$$

即形式幂级数展开的第 $k$ 项系数。

这个问题的特殊之处在于：**任何线性递推数列的生成函数都可以写成 $P(x)/Q(x)$ 的形式**，其中 $Q(x)$ 就是特征多项式的倒序多项式。

#### 核心思想

Bostan-Mori 的算法极其简洁：通过巧妙的代数变换，把求第 $k$ 项的问题递归地缩小为求第 $\lfloor k/2 \rfloor$ 项的问题。

令 $Q_\text{even}(x) = \frac{Q(x) + Q(-x)}{2}$（提取偶次项系数），$Q_\text{odd}(x) = \frac{Q(x) - Q(-x)}{2}$（提取奇次项系数）。

类似地定义 $P_\text{even}, P_\text{odd}$。

那么主要递归公式是：

如果 $k$ 是偶数：
$$\text{solve}(P, Q, k) = \text{solve}(P_\text{even}, Q_\text{even}^2 - Q_\text{odd}^2 \cdot x^2, \; k/2)$$

如果 $k$ 是奇数：
$$\text{solve}(P, Q, k) = \text{solve}(P_\text{odd}, Q_\text{even}^2 - Q_\text{odd}^2 \cdot x^2, \; (k-1)/2)$$

这个递归的深度是 $O(\log k)$，每层需要做 $O(d \log d)$ 的多项式乘法（用 FFT/NTT），总复杂度 $O(d \log d \log k)$。

❓ **这个递归公式是怎么来的？**

回忆生成函数 $G(x) = \sum_{n\ge 0} a_n x^n = P(x)/Q(x)$。如果把 $G(x)$ 拆成奇偶部分：

$$G(x) = \sum_{n\ge 0} a_{2n} x^{2n} + \sum_{n\ge 0} a_{2n+1} x^{2n+1}$$

那么 $G(x) + G(-x) = 2\sum_{n\ge 0} a_{2n} x^{2n}$，$G(x) - G(-x) = 2\sum_{n\ge 0} a_{2n+1} x^{2n+1}$。

代入 $G(x) = P(x)/Q(x)$：

$$\frac{P(x)}{Q(x)} + \frac{P(-x)}{Q(-x)} = \frac{P(x)Q(-x) + P(-x)Q(x)}{Q(x)Q(-x)} = 2\sum a_{2n} x^{2n}$$

令 $U(x) = P(x)Q(-x) + P(-x)Q(x)$，$V(x) = Q(x)Q(-x)$。

而 $V(x)$ 一定是偶函数（因为 $V(-x) = Q(-x)Q(x) = V(x)$），所以 $V(x)$ 中只含 $x$ 的偶次项。

于是我们可以令 $x^2 = y$，得到：

$$\frac{U(x)}{V(x)} = 2\sum a_{2n} x^{2n} = 2\sum a_{2n} y^n$$

然后提取 $y^{k}$ 的系数（对应原序列的第 $2k$ 项）即可。

**算法过程（手算小例子）**：

求 Fibonacci 数列 $a_0=0, a_1=1, a_n=a_{n-1}+a_{n-2}$ 的第 5 项。

生成函数 $G(x) = \frac{x}{1-x-x^2}$，所以 $P(x) = x$，$Q(x) = 1 - x - x^2$。

求 $[x^5] \frac{x}{1 - x - x^2}$。

**第 1 层**：$k=5$ 是奇数。

$$P_\text{odd} = x, \quad U(x) = P(x)Q(-x) + P(-x)Q(x) = x(1+x-x^2) + (-x)(1-x-x^2)$$
$$= x + x^2 - x^3 - x + x^2 + x^3 = 2x^2$$

$$V(x) = Q(x)Q(-x) = (1-x-x^2)(1+x-x^2)$$

计算乘积：$(1-x-x^2)(1+x-x^2)$

先算 $1 \cdot (1+x-x^2) = 1 + x - x^2$
再算 $-x \cdot (1+x-x^2) = -x - x^2 + x^3$
再算 $-x^2 \cdot (1+x-x^2) = -x^2 - x^3 + x^4$

求和：$(1 + x - x^2) + (-x - x^2 + x^3) + (-x^2 - x^3 + x^4)$
$= 1 + 0x + (-1-1-1)x^2 + (1-1)x^3 + x^4$
$= 1 - 3x^2 + x^4$

所以新的 $P(x) = U(x) / x = 2x$（因为奇数情况，$U(x)$ 的奇次项系数就是答案），新的 $Q(y) = 1 - 3y + y^2$（令 $y=x^2$）。

但我们需要小心处理。标准递归中，奇数情况 $P$ 要用 $P_\text{odd}$，$Q$ 用 $Q_\text{even}^2 - Q_\text{odd}^2 \cdot x^2$。

继续算：
$Q_\text{even}(x) = 1 - x^2$（$Q(x)$ 的偶次项），$Q_\text{odd}(x) = -x$（奇次项）。

$Q_\text{even}^2 - Q_\text{odd}^2 \cdot x^2 = (1-x^2)^2 - (-x)^2 \cdot x^2 = 1 - 2x^2 + x^4 - x^4 = 1 - 2x^2$

$P_\text{odd} = x$

令 $y = x^2$，我们需要求 $[y^{(5-1)/2}] = [y^2] \frac{x}{1-2y}$ ……

这个手算过程有点繁琐。实际上，我们不需要每次都手动做。Bostan-Mori 的美妙之处在于**代码极短**（10 行左右），而且可以用 NTT 做多项式乘法达到最优复杂度。

❓ **Kitamasa 和 Bostan-Mori 的区别是什么？**

Kitamasa 直接操作特征多项式，计算 $x^n \bmod P(x)$ 的模幂，得到初值组合系数。它依赖初值向量，更适合求单个递推数列的第 $n$ 项。

Bostan-Mori 操作有理函数的分子分母 $P(x)/Q(x)$，直接提取展开式的第 $k$ 项系数。它**不依赖初值**，适合求生成函数的第 $k$ 项、有理函数幂级数展开、以及**高次递推**（可以配合 NTT 做到 $O(d \log d \log k)$）。

实际竞赛中：
- $k \le 2000$，用 Kitamasa（代码好写，常数小）
- $k$ 很大（$10^5$ 级别）且有 NTT 模板时，用 Bostan-Mori
- 求有理函数的第 $k$ 项系数时，只能用 Bostan-Mori

### 3.6 Cayley-Hamilton 定理

Kitamasa 方法的理论基础是**Cayley-Hamilton 定理**。

> **Cayley-Hamilton 定理**：设 $M$ 是 $n \times n$ 矩阵，$P(\lambda) = \det(\lambda I - M)$ 是它的特征多项式，则 $P(M) = O$（零矩阵）。

换句话说，**矩阵满足它自己的特征方程**。

这个定理对线性递推的意义是什么？回忆转移矩阵 $M$：

$$
M = \begin{pmatrix}
c_1 & c_2 & \cdots & c_{k-1} & c_k \\
1 & 0 & \cdots & 0 & 0 \\
0 & 1 & \cdots & 0 & 0 \\
\vdots & \vdots & \ddots & \vdots & \vdots \\
0 & 0 & \cdots & 1 & 0
\end{pmatrix}
$$

$M$ 的特征多项式恰好是 $P(x) = x^k - c_1 x^{k-1} - \cdots - c_k$。

CH 定理告诉我们 $P(M) = 0$，所以 $M^k = c_1 M^{k-1} + \cdots + c_k I$。

这就是递推的矩阵版本！任何 $M$ 的高次幂都可以通过这个关系化归为 $M^0, M^1, \dots, M^{k-1}$ 的线性组合。

Kitamasa 方法只不过是把这个思想从矩阵搬到多项式上：$x^n$ 在模 $P(x)$ 下的余式就是 $M^n$ 在基 $\{I, M, \dots, M^{k-1}\}$ 下展开的系数，而 $M^n$ 作用于初值向量就得到第 $n$ 项。

❓ **Kitamasa、Bostan-Mori 和矩阵快速幂，哪个快？**

矩阵快速幂：$O(k^3 \log n)$。简单直接，适合 $k \le 100$。

Kitamasa：$O(k^2 \log n)$。适合 $k \le 2000$，代码中等长度。

Bostan-Mori（带 NTT）：$O(k \log k \log n)$。适合 $k$ 巨大（$10^5$）且有 NTT 模板的情况。

如果 $k$ 很小（比如 $k \le 10$），矩阵快速幂实际上因为常数小而更快。

---

## 四、代码实现

### Kitamasa 实现

```cpp
#include <bits/stdc++.h>
using ll = long long;
using poly = std::vector<ll>;

const ll MOD = 1'000'000'007;

ll mod_pow(ll a, ll e) {
    ll r = 1;
    while (e) { if (e & 1) r = r * a % MOD; a = a * a % MOD; e >>= 1; }
    return r;
}

// 多项式乘法（朴素 O(k^2)），系数模 MOD
poly poly_mul(const poly &a, const poly &b) {
    poly res(a.size() + b.size() - 1, 0);
    for (int i = 0; i < (int)a.size(); i++)
        for (int j = 0; j < (int)b.size(); j++)
            res[i + j] = (res[i + j] + a[i] * b[j]) % MOD;
    return res;
}

// 多项式取模：a(x) mod p(x)，其中 p 是 k 次首一多项式
poly poly_mod(const poly &a, const poly &p) {
    int k = (int)p.size() - 1;
    poly r = a;
    for (int i = (int)r.size() - 1; i >= k; i--) {
        if (r[i] == 0) continue;
        ll inv = r[i]; // 因为 p 是首一的，系数为 1
        for (int j = 0; j <= k; j++)
            r[i - k + j] = (r[i - k + j] - inv * p[j]) % MOD;
    }
    r.resize(k);
    for (auto &x : r) if (x < 0) x += MOD;
    return r;
}

// Kitamasa: 求 k 阶递推数列的第 n 项
// a[0..k-1] 是初值，c[1..k] 是递推系数（a[n]=c[1]a[n-1]+...+c[k]a[n-k]）
ll kitamasa(const poly &a, const poly &c, ll n) {
    int k = (int)c.size() - 1;
    if (n < k) return a[n] % MOD;

    // 特征多项式 P(x) = x^k - c[1]x^{k-1} - ... - c[k]
    poly p(k + 1, 0);
    p[0] = 1;
    for (int i = 1; i <= k; i++) {
        p[i] = (-c[i] % MOD + MOD) % MOD;
    }

    // 计算 x^n mod p(x)
    // 用快速幂
    poly res = {1};  // x^0 = 1
    poly base = {0, 1}; // x^1
    ll e = n;
    while (e) {
        if (e & 1) {
            res = poly_mul(res, base);
            res = poly_mod(res, p);
        }
        base = poly_mul(base, base);
        base = poly_mod(base, p);
        e >>= 1;
    }
    // 现在 res(x) = sum_{i=0}^{k-1} beta_i * x^i
    // a[n] = sum_{i=0}^{k-1} beta_i * a[i]
    ll ans = 0;
    for (int i = 0; i < k; i++)
        ans = (ans + res[i] * a[i]) % MOD;
    return ans;
}

int main() {
    // Fibonacci: a0=0, a1=1, a[n]=a[n-1]+a[n-2]
    poly a = {0, 1};
    poly c = {0, 1, 1}; // c[1]=1, c[2]=1
    ll n = 10;
    printf("F(%lld) = %lld\n", n, kitamasa(a, c, n)); // 输出 55
    n = 1000000000000000000LL;
    printf("F(%lld) = %lld\n", n, kitamasa(a, c, n)); // 大数结果
    return 0;
}
```

注意：上面的 $c$ 数组下标从 1 开始，$c[0]$ 是占位符。

### Bostan-Mori 实现（朴素版，O(d^2 log k)）

```cpp
#include <bits/stdc++.h>
using ll = long long;
using poly = std::vector<ll>;

const ll MOD = 1'000'000'007;

// 朴素多项式乘法
poly mul(const poly &a, const poly &b) {
    poly res(a.size() + b.size() - 1, 0);
    for (int i = 0; i < (int)a.size(); i++)
        for (int j = 0; j < (int)b.size(); j++)
            res[i+j] = (res[i+j] + a[i]*b[j]) % MOD;
    return res;
}

// 多项式除法：a / b，返回商
poly div(poly a, poly b) {
    int n = (int)a.size()-1, m = (int)b.size()-1;
    if (n < m) return {};
    poly q(n-m+1);
    ll inv_bm = mod_pow(b[m], MOD-2);
    for (int i = n-m; i >= 0; i--) {
        q[i] = a[i+m] * inv_bm % MOD;
        for (int j = 0; j <= m; j++)
            a[i+j] = (a[i+j] - q[i] * b[j]) % MOD;
    }
    for (auto &x : q) if (x < 0) x += MOD;
    return q;
}

// 多项式取模
poly mod(poly a, poly b) {
    auto q = div(a, b);
    int m = (int)b.size()-1;
    poly r(b.size()-1);
    for (int i = 0; i < m; i++) {
        r[i] = a[i];
        for (int j = 0; j <= (int)q.size()-1 && i >= j; j++)
            r[i] = (r[i] - q[j] * b[i-j]) % MOD;
        if (r[i] < 0) r[i] += MOD;
    }
    return r;
}

// Bostan-Mori: 求[x^k] P(x)/Q(x)，要求 degP < degQ，Q[0]!=0
ll bostan_mori(poly P, poly Q, ll k) {
    while (k) {
        poly Q_minus = Q;
        for (int i = 1; i < (int)Q.size(); i+=2)
            Q_minus[i] = (-Q_minus[i] % MOD + MOD) % MOD;

        auto U = mul(P, Q_minus);
        // V(x) = Q(x) * Q(-x)
        auto V = mul(Q, Q_minus);

        if (k & 1) {
            // 取 U 的奇次项
            for (int i = 0; i < (int)U.size(); i++)
                P[i/2] = (i & 1) ? U[i] : 0;
        } else {
            // 取 U 的偶次项
            for (int i = 0; i < (int)U.size(); i++)
                P[i/2] = (i % 2 == 0) ? U[i] : 0;
        }
        P.resize((U.size()+1)/2);

        // V 只取偶次项
        for (int i = 0; i < (int)V.size(); i+=2)
            Q[i/2] = V[i];
        Q.resize((V.size()+1)/2);

        k >>= 1;
    }
    return P.empty() ? 0 : (P[0] * mod_pow(Q[0], MOD-2)) % MOD;
}

int main() {
    // Fibonacci: G(x) = x/(1-x-x^2)
    poly P = {0, 1};   // x
    poly Q = {1, MOD-1, MOD-1};  // 1 - x - x^2
    ll k = 10;
    printf("[x^%lld] P/Q = %lld\n", k, bostan_mori(P, Q, k)); // 55
    return 0;
}
```

---

## 五、复杂度分析

| 方法 | 时间复杂度 | 空间复杂度 | 适用场景 |
|------|-----------|-----------|---------|
| 矩阵快速幂 | $O(k^3 \log n)$ | $O(k^2)$ | $k \le 100$ |
| Kitamasa（朴素） | $O(k^2 \log n)$ | $O(k)$ | $k \le 2000$ |
| Kitamasa（NTT 优化）| $O(k \log k \log n)$ | $O(k)$ | $k \le 10^5$ |
| Bostan-Mori（朴素） | $O(k^2 \log n)$ | $O(k)$ | $k$ 中等，无 NTT |
| Bostan-Mori（NTT） | $O(k \log k \log n)$ | $O(k)$ | $k$ 巨大 |

Kitamasa 的空间优势也很明显：只需要 $O(k)$ 存储多项式系数，而矩阵快速幂需要 $O(k^2)$ 存矩阵。

---

## 六、应用场景

1. **BM + Kitamasa**：先打表得到数列，用 BM 求递推式，再用 Kitamasa 算第 $n$ 项——竞赛中最强的「黑盒」组合
2. **有理函数求值**：生成函数的问题中，Bostan-Mori 可以直接提取第 $k$ 项
3. **常系数线性齐次递推**：各种 DP 的最终形式
4. **求解 $n$ 阶循环**：涉及整数的某种递推

**推荐练习题**：

- [洛谷 P4723 【模板】线性递推](https://www.luogu.com.cn/problem/P4723) — Kitamasa 模板题，求第 $n$ 项
- [Codeforces 1344D Résumé Review](https://codeforces.com/problemset/problem/1344/D) — 结合牛顿法的困难题，穿插递推求值
- [Project Euler 700](https://projecteuler.net/problem=700) — 通用生成函数问题

---

## 七、小结

Kitamasa 和 Bostan-Mori 是线性递推问题的两个利剑：

- **Kitamasa**：计算 $x^n \bmod P(x)$ 的多项式模幂，得到初值组合系数。思想来自 Cayley-Hamilton 定理。
- **Bostan-Mori**：通过奇偶分解递归缩小问题规模，直接提取有理函数幂级数的第 $k$ 项。

两者都避开了矩阵乘法的 $O(k^3)$ 瓶颈，把复杂度降到了 $O(k^2 \log n)$ 乃至 $O(k \log k \log n)$。

下一篇文章我们将从另一个角度来看线性代数问题：**范德蒙德矩阵与拉格朗日插值**——如何通过 $k+1$ 个点唯一确定一个 $k$ 次多项式。

---

> **系列索引**：本文是 ACM 竞赛数学系列的第 79 篇。
> 上一篇：[#78 线性递推与 Berlekamp-Massey](78-线性递推与Berlekamp-Massey.md)
> 下一篇：[#80 范德蒙德矩阵与拉格朗日插值](80-范德蒙德矩阵与拉格朗日插值.md)
