# 中国剩余定理（CRT）

> Made by Aki.
> 最后更新于 2026.04.30

韩信点兵，物不知数——中国剩余定理处理的是竞赛中一类经典问题：在模不同数的条件下同时求出一个 $x$。

---

## 一、引言

《孙子算经》有一道名题：

> 今有物不知其数，三三数之剩二，五五数之剩三，七七数之剩二，问物几何？

翻译成数学语言：

$$
\begin{cases}
x \equiv 2 \pmod{3} \\
x \equiv 3 \pmod{5} \\
x \equiv 2 \pmod{7}
\end{cases}
$$

求最小的正整数 $x$。答案 $x = 23$ 是古人早已算出的，但**方法**——如何系统求解任意多个同余方程——正是中国剩余定理（CRT）的内容。

---

## 二、前置知识

- [第 12 篇：线性同余方程](../01-数论/12-线性同余方程.md)——将 $a_i x \equiv b_i$ 化为 $x \equiv r_i$
- [第 9 篇：乘法逆元](../01-数论/09-乘法逆元.md)——CRT 公式中的模逆元计算
- [第 8 篇：扩展欧几里得](../01-数论/08-扩展欧几里得算法.md)——exCRT 的合并步骤

---

## 三、核心推导

### 3.1 问题形式

CRT 处理的是以下形式的同余方程组：

$$
\begin{cases}
x \equiv r_1 \pmod{m_1} \\
x \equiv r_2 \pmod{m_2} \\
\quad \vdots \\
x \equiv r_k \pmod{m_k}
\end{cases}
$$

其中**各模数两两互质**（$\gcd(m_i, m_j) = 1$，$i \neq j$）。

---

### 3.2 CRT 的构造性证明

设 $M = \prod_{i=1}^k m_i$（所有模数的乘积）。对每个 $i$，定义：

$$
M_i = \frac{M}{m_i}
$$

由于 $\gcd(m_i, m_j) = 1$（$i \neq j$），$M_i$ 与 $m_i$ 互质。因此 $M_i$ 在模 $m_i$ 下有逆元，记作 $t_i = M_i^{-1} \pmod{m_i}$。

**CRT 公式**：

$$
\boxed{x \equiv \sum_{i=1}^k r_i \cdot M_i \cdot t_i \pmod{M}}
$$

**为什么这个公式成立？** 对任意 $i$，考虑第 $i$ 项 $r_i \cdot M_i \cdot t_i$ 模 $m_j$ 的值：

- 当 $j = i$：$M_i \cdot t_i \equiv 1 \pmod{m_i}$（因为 $t_i$ 就是 $M_i$ 的逆元），所以该项 $\equiv r_i \times 1 \equiv r_i \pmod{m_i}$。
- 当 $j \neq i$：$M_i$ 是 $M/m_i$，其中包含了 $m_j$ 作为因子，所以 $M_i \equiv 0 \pmod{m_j}$，该项 $\equiv 0 \pmod{m_j}$。

因此对每个方程 $j$，求和式中只有第 $j$ 项贡献非零值 $r_j$，满足 $x \equiv r_j \pmod{m_j}$。

**这个构造的妙处在于**：每一项 $r_i M_i t_i$ 是独立设计的——它对第 $i$ 个方程贡献 $r_i$，对其它所有方程贡献 $0$。求和就是把所有独立贡献叠加起来。

---

### 3.3 手动计算——韩信点兵

回到引言中的题：

$$
x \equiv 2 \pmod{3},\; x \equiv 3 \pmod{5},\; x \equiv 2 \pmod{7}
$$

- $M = 3 \times 5 \times 7 = 105$
- $M_1 = 35$，$t_1 = 35^{-1} \bmod 3$。$35 \equiv 2 \pmod{3}$，$2^{-1} \bmod 3 = 2$，所以 $t_1 = 2$
- $M_2 = 21$，$t_2 = 21^{-1} \bmod 5$。$21 \equiv 1 \pmod{5}$，$1^{-1} = 1$，所以 $t_2 = 1$
- $M_3 = 15$，$t_3 = 15^{-1} \bmod 7$。$15 \equiv 1 \pmod{7}$，$1^{-1} = 1$，所以 $t_3 = 1$

代入：

$$
x \equiv 2 \times 35 \times 2 + 3 \times 21 \times 1 + 2 \times 15 \times 1 \pmod{105}
$$

$$
x \equiv 140 + 63 + 30 \equiv 233 \equiv 23 \pmod{105}
$$

最小的正整数 $x = 23$。验证：$23 \bmod 3 = 2$ ✓，$23 \bmod 5 = 3$ ✓，$23 \bmod 7 = 2$ ✓。

---

### 3.4 扩展 CRT（exCRT）——模数不互质怎么办？

当 $\gcd(m_i, m_j) \neq 1$ 时，$M_i$ 在模 $m_i$ 下可能没有逆元，标准 CRT 公式失效。

exCRT 的思路完全不同：**逐个合并方程**。每次合并两个同余式，用 exgcd 处理可能的不一致。

**合并两个方程** $x \equiv r_1 \pmod{m_1}$ 和 $x \equiv r_2 \pmod{m_2}$：

设 $x = r_1 + m_1 \cdot k$，代入第二个方程：

$$
r_1 + m_1 \cdot k \equiv r_2 \pmod{m_2}
$$

整理：

$$
m_1 \cdot k \equiv r_2 - r_1 \pmod{m_2}
$$

这正是一个线性同余方程。由第 12 篇，它有解当且仅当 $\gcd(m_1, m_2) \mid (r_2 - r_1)$。若无解，方程组无解。

若有解，用 exgcd 求出 $k \equiv k_0 \pmod{m_2 / \gcd(m_1, m_2)}$，然后 $x \equiv r_1 + m_1 k_0 \pmod{\operatorname{lcm}(m_1, m_2)}$。

依次合并所有方程，最终得到一个 $x \equiv R \pmod{M_{\text{final}}}$ 的解。

---

## 四、代码实现

### 4.1 CRT（模数互质）

```cpp
using ll = long long;

// 求解 x ≡ r[i] (mod m[i])，m[i] 两两互质
// 返回最小非负解，无解返回 -1（互质时不会无解）
ll crt(const vector<ll> &r, const vector<ll> &m) {
    int k = r.size();
    ll M = 1;
    for (ll mi : m) M *= mi;
    ll ans = 0;
    for (int i = 0; i < k; i++) {
        ll Mi = M / m[i];
        ll ti = inv_exgcd(Mi % m[i], m[i]);  // Mi^{-1} mod m[i]
        ans = (ans + r[i] * Mi % M * ti) % M;
    }
    return ans;
}
```

### 4.2 exCRT（模数任意）

```cpp
// 逐个合并：每次解 x ≡ r1 (mod m1), x ≡ r2 (mod m2)
// 返回合并后的 (R, M) 或 {-1, -1} 表示无解
pair<ll, ll> merge_crt(ll r1, ll m1, ll r2, ll m2) {
    ll g = gcd(m1, m2);
    if ((r2 - r1) % g != 0) return {-1, -1};  // 无解
    ll x, y;
    exgcd(m1 / g, m2 / g, x, y);
    ll l = m1 / g * m2;                        // lcm(m1, m2)
    ll t = (r2 - r1) / g * x % (m2 / g);
    ll R = ((r1 + m1 * t) % l + l) % l;
    return {R, l};
}

ll excrt(const vector<ll> &r, const vector<ll> &m) {
    ll R = 0, M = 1;
    for (int i = 0; i < (int)r.size(); i++) {
        auto [newR, newM] = merge_crt(R, M, r[i], m[i]);
        if (newR == -1) return -1;
        R = newR; M = newM;
    }
    return R;
}
```

使用示例：

```cpp
// CRT: 韩信点兵
vector<ll> r = {2, 3, 2}, m = {3, 5, 7};
cout << crt(r, m) << endl;        // 23

// exCRT: 模数不互质
r = {2, 3}; m = {4, 6};
cout << excrt(r, m) << endl;      // 无解（2≡? mod gcd(4,6)=2 vs 3-2=1 ∤ 2）

// 实际有解的情况
r = {3, 5}; m = {5, 9};
cout << excrt(r, m) << endl;      // 23
// 验证: 23%5=3 ✓, 23%9=5 ✓
```

---

## 五、复杂度与正确性分析

| 方法 | 时间复杂度 | 适用条件 |
|------|-----------|----------|
| CRT | $O(k \log M)$ | 模数两两互质 |
| exCRT | $O(k \log M)$ | 模数任意 |

CRT 的正确性由 3.2 节的构造性证明保证——每个 $M_i t_i$ 在方程 $i$ 中为 $1$，在其他方程中为 $0$。exCRT 的正确性由逐次合并的正确性保证——每次合并等价于解一个线性同余方程，再由 exgcd 和裴蜀定理确定有解性。

---

## 六、典型应用场景

1. **同余方程组的唯一表示**：当题目给出多个模条件时，CRT 将它们合并为一个 $x \equiv R \pmod{M}$，使后续处理简化。

2. **大模数拆分**：有时模数 $p$ 本身很难处理，但可以分解为 $p = p_1 p_2 \cdots$（互质因子），对每个因子分别求解再用 CRT 合并。这是处理模合数的通用策略。

3. **计数问题中的循环周期**：多个周期运动的首次重合时间，本质上是解 $t \equiv r_i \pmod{T_i}$ 的 CRT 问题。

**推荐练习题**：

- [洛谷 P1495](https://www.luogu.com.cn/problem/P1495) — 【模板】中国剩余定理（CRT）。模数互质的标准 CRT
- [洛谷 P4777](https://www.luogu.com.cn/problem/P4777) — 【模板】扩展中国剩余定理（exCRT）。模数不互质，需要逐个合并
- [Codeforces 338D](https://codeforces.com/problemset/problem/338/D) — GCD Table。将表格条件转化为同余方程组，exCRT 求解

---

## 七、小结

CRT 和 exCRT 分别代表了处理同余方程组的两种哲学：

- **CRT**：一次性构造。通过设计 $M_i t_i$ 使得每项只在目标方程有贡献，直接写出通解公式。
- **exCRT**：逐个合并。每次处理两个方程，将问题规模逐步缩减，最终归结为单个同余式。

在竞赛中，exCRT 的实现频率高于 CRT，因为题目中的模数往往是数据给定的，不一定互质。但 CRT 的构造思想（线性叠加、每项独立贡献）是整个数论思想体系中的一颗宝石，值得掌握。

下一篇是**组合数取模**——我们将汇总前面所学的所有工具（逆元、CRT、质因数分解、Lucas 定理）来攻克竞赛中最常见的组合数问题。

---

> **系列索引**：本文是 ACM 竞赛数学系列的第 13 篇。
> 上一篇：[#12 线性同余方程](../01-数论/12-线性同余方程.md)
> 下一篇：[#14 组合数取模](../01-数论/14-组合数取模.md)
