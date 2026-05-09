# NTT 与多项式基础

> Made by Aki.
> 最后更新于 2026.04.30

多项式乘法是竞赛中一类特殊但又常见的问题。普通 $O(n^2)$ 的卷积在 $n=10^5$ 时不可行，FFT/NTT（快速傅里叶变换/数论变换）将其降至 $O(n \log n)$。NTT 是在模素数下避免浮点误差的 FFT 替代方案。

---

## 一、引言

两个 $n$ 次多项式 $A(x)$ 和 $B(x)$ 相乘，朴素 $O(n^2)$。FFT 通过「系数表示 → 点值表示 → 乘积 → 回到系数」的策略，利用单位根的分治性质降到 $O(n \log n)$。但在模素数环境下，浮点误差不可接受——NTT 用原根替代复数单位根，全程在模意义下精确计算。

---

## 二、前置知识

- [第 15 篇：原根](../01-数论/15-阶与原根.md)——NTT 的单位根需要原根生成
- [第 7 篇：快速幂](../01-数论/07-快速幂与慢速乘.md)

---

## 三、核心推导

### 3.1 为什么需要 NTT？

FFT 使用复数单位根 $\omega_n = e^{2\pi i/n}$ 作为变换基。它的阶为 $n$：$\omega_n^n = 1$，且消去引理成立：$\omega_{2n}^{2k} = \omega_n^k$。

在模素数 $p$ 下，如果 $p-1$ 能被 $n$ 整除，取 $g$ 为 $p$ 的原根，则 $\omega_n \equiv g^{(p-1)/n} \pmod{p}$ 就是一个「模意义下的 $n$ 次单位根」。它同样满足 $\omega_n^n \equiv 1$ 和 $\omega_{2n}^2 \equiv \omega_n$。

**NTT 的要求**：模数 $p$ 必须形如 $k \cdot 2^m + 1$（因为 FFT/NTT 要求在 $2$ 的幂次大小上做变换）。常用 NTT 素数：

| $p$ | 原根 | $2^m$ 最大 |
|-----|------|-----------|
| $998244353$ | $3$ | $2^{23}$ |
| $1004535809$ | $3$ | $2^{21}$ |
| $469762049$ | $3$ | $2^{26}$ |

---

### 3.2 NTT 的 Butterfly 变换

NTT 的结构与 FFT 完全一致，只是单位根换了。以 Cooley-Tukey 迭代实现为例：

1. **位逆序重排**（bit-reversal permutation）
2. **蝶形运算**：对每层 $len = 2, 4, 8, \dots, N$（$N$ 为 $2$ 的幂），步长为 $len/2$，旋转因子 $\omega_{len}$。

核心操作（合并两个长度为 $len/2$ 的子变换）：

$$
\begin{aligned}
u &= a[j] \\
v &= a[j + len/2] \times \omega_{len}^k \bmod p \\
a[j] &= u + v \\
a[j + len/2] &= u - v
\end{aligned}
$$

逆 NTT 只需将 $\omega$ 替换为其逆元，最后每个元素乘 $N^{-1}$。

---

## 四、代码实现

```cpp
const int MOD = 998244353, G = 3;  // G 是 MOD 的原根

void ntt(vector<ll> &a, bool invert) {
    int n = a.size();
    // 位逆序重排
    for (int i = 1, j = 0; i < n; i++) {
        int bit = n >> 1;
        for (; j & bit; bit >>= 1) j ^= bit;
        j ^= bit;
        if (i < j) swap(a[i], a[j]);
    }
    // 蝶形运算
    for (int len = 2; len <= n; len <<= 1) {
        ll wlen = qpow(G, (MOD - 1) / len, MOD);
        if (invert) wlen = qpow(wlen, MOD - 2, MOD);
        for (int i = 0; i < n; i += len) {
            ll w = 1;
            for (int j = 0; j < len / 2; j++) {
                ll u = a[i + j];
                ll v = a[i + j + len / 2] * w % MOD;
                a[i + j] = (u + v) % MOD;
                a[i + j + len / 2] = (u - v + MOD) % MOD;
                w = w * wlen % MOD;
            }
        }
    }
    if (invert) {
        ll inv_n = qpow(n, MOD - 2, MOD);
        for (ll &x : a) x = x * inv_n % MOD;
    }
}

vector<ll> multiply(vector<ll> a, vector<ll> b) {
    int n = 1, orig = a.size() + b.size() - 1;
    while (n < orig) n <<= 1;
    a.resize(n); b.resize(n);
    ntt(a, false); ntt(b, false);
    for (int i = 0; i < n; i++) a[i] = a[i] * b[i] % MOD;
    ntt(a, true);
    a.resize(orig);
    return a;
}
```

---

## 五、推荐练习题

- [洛谷 P3803](https://www.luogu.com.cn/problem/P3803) — 【模板】多项式乘法（FFT）。NTT 同理可过
- [洛谷 P4238](https://www.luogu.com.cn/problem/P4238) — 【模板】多项式乘法逆。NTT 框架上的逆元计算

---

> **系列索引**：本文是 ACM 竞赛数学系列的第 24 篇。
> 上一篇：[#23 杜教筛](../01-数论/23-杜教筛.md)
> 下一篇：[#25 生成函数入门](../01-数论/25-生成函数入门.md)
