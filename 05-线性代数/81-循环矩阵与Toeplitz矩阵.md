# 循环矩阵与 Toeplitz 矩阵

> Made by Aki.
> 最后更新于 2026.04.30

---

## 一、引言

假设你在做一个**环形**结构的 DP：有 $n$ 个位置排成一个环，DP 转移只依赖于距离（比如每个位置的值是它前后 $k$ 个邻居的加权和）。这个 DP 对应一个**循环矩阵**（circulant matrix）的乘法。

又或者你在处理**卷积**相关的问题：卷积 $c_k = \sum_i a_i \cdot b_{k-i}$ 可以写成矩阵形式，这个矩阵是**Toeplitz 矩阵**。

普通矩阵乘法是 $O(n^3)$，即使是方阵乘向量也要 $O(n^2)$。但循环矩阵和 Toeplitz 矩阵有极强的结构，可以利用 **FFT** 把乘法加速到 $O(n \log n)$。

本文从循环矩阵开始，讨论它们如何被 DFT 对角化，然后扩展到 Toeplitz 矩阵，展示如何用嵌入法把 Toeplitz 矩阵乘法转化为循环矩阵乘法。

---

## 二、前置知识

- 矩阵乘法的基本概念（[第 74 篇](74-矩阵基本运算与快速幂.md)）
- DFT/FFT 的基本原理（[第 34 篇](../04-多项式/34-快速傅里叶变换FFT.md)）
- 卷积的定义与性质（[第 33 篇](../04-多项式/33-卷积与生成函数入门.md)）
- 复数单位根（[第 35 篇](../04-多项式/35-NTT与任意模数NTT.md)）

---

## 三、核心推导

### 3.1 循环矩阵的定义

一个 $n \times n$ 的**循环矩阵** $C$ 由它的第一行 $c = (c_0, c_1, \dots, c_{n-1})$ 完全确定。第 $i$ 行就是第一行**循环右移** $i$ 位：

$$
C = \begin{pmatrix}
c_0 & c_1 & c_2 & \cdots & c_{n-1} \\
c_{n-1} & c_0 & c_1 & \cdots & c_{n-2} \\
c_{n-2} & c_{n-1} & c_0 & \cdots & c_{n-3} \\
\vdots & \vdots & \vdots & \ddots & \vdots \\
c_1 & c_2 & c_3 & \cdots & c_0
\end{pmatrix}
$$

即 $C_{ij} = c_{(j-i) \bmod n}$。

三种典型的循环矩阵：
- 单位矩阵：第一行 $(1, 0, 0, \dots, 0)$
- 循环移位矩阵：第一行 $(0, 1, 0, \dots, 0)$
- 全 1 矩阵：第一行 $(1, 1, 1, \dots, 1)$

### 3.2 循环矩阵在 DFT 下对角化

循环矩阵最漂亮的性质：**所有循环矩阵可以被同一个正交基同时对角化**——这个基就是 DFT 矩阵。

**定理**：对于任何循环矩阵 $C$，有：

$$C = F^* \cdot \text{diag}(\sqrt{n} F c) \cdot F$$

其中 $F$ 是 DFT 矩阵（$F_{jk} = \frac{1}{\sqrt{n}} \omega_n^{jk}$，$F^*$ 是共轭转置），$F c$ 是 $c$ 的离散傅里叶变换。

更简单地写（去掉归一化因子）：如果 $\hat{c} = \text{DFT}(c)$（即 $c$ 的傅里叶变换），那么 $C$ 的特征值是 $\hat{c}_0, \hat{c}_1, \dots, \hat{c}_{n-1}$，特征向量是傅里叶基。

换句话说，**循环矩阵乘法等价于频域上的逐点乘法**。

❓ **这个性质有什么用？**

意味着循环矩阵乘向量 $C \cdot v$ 可以在 $O(n \log n)$ 内完成：

1. 对 $c$ 做 FFT，得到 $\hat{c}$（$O(n \log n)$）
2. 对 $v$ 做 FFT，得到 $\hat{v}$（$O(n \log n)$）
3. 逐点乘：$\hat{w}_k = \hat{c}_k \cdot \hat{v}_k$（$O(n)$）
4. 对 $\hat{w}$ 做 IFFT 得到 $w = Cv$（$O(n \log n)$）

总复杂度 $O(n \log n)$，远快于 $O(n^2)$。

更进一步，**两个循环矩阵相乘，结果也是循环矩阵**，而且可以用同样的方法加速：

$$C(a) \cdot C(b) = C(a * b)$$

其中 $*$ 是循环卷积。所以两个循环矩阵相乘也是 $O(n \log n)$。

**手算例子**：考虑 $3 \times 3$ 循环矩阵 $C$，第一行 $c = (1, 2, 3)$。

$$C = \begin{pmatrix}
1 & 2 & 3 \\
3 & 1 & 2 \\
2 & 3 & 1
\end{pmatrix}$$

计算 $C \cdot v$，其中 $v = (1, 0, 0)^T$。

直接算：$Cv = (1, 3, 2)^T$。

用 FFT 方法（为了手算，我们用三次单位根 $\omega_3$）：

$\hat{c} = \text{DFT}(1, 2, 3)$：

$$\hat{c}_0 = 1 + 2 + 3 = 6$$
$$\hat{c}_1 = 1 + 2\omega_3 + 3\omega_3^2$$
$$\hat{c}_2 = 1 + 2\omega_3^2 + 3\omega_3^4 = 1 + 2\omega_3^2 + 3\omega_3$$

其中 $\omega_3 = -\frac12 + \frac{\sqrt{3}}{2}i$。

$\hat{v} = \text{DFT}(1, 0, 0) = (1, 1, 1)$

$\hat{w} = \hat{c} \odot \hat{v} = (6, \hat{c}_1, \hat{c}_2)$

IFFT 后得到 $(1, 3, 2)$，和直接计算一致。

### 3.3 循环矩阵的另一条重要性质

**循环矩阵的乘积可交换**。即：对任意两个循环矩阵 $C_1, C_2$，有 $C_1 C_2 = C_2 C_1$。

这是因为在频域上它们都是对角矩阵，而对角矩阵的可交换性是显然的。

这条性质在分析环形结构时很有用：我们可以自由调整循环算子的顺序。

### 3.4 Toeplitz 矩阵的定义

**Toeplitz 矩阵**是每条对角线上的元素都相同的矩阵：

$$
T = \begin{pmatrix}
a_0 & a_{-1} & a_{-2} & \cdots & a_{-(n-1)} \\
a_1 & a_0 & a_{-1} & \cdots & a_{-(n-2)} \\
a_2 & a_1 & a_0 & \cdots & a_{-(n-3)} \\
\vdots & \vdots & \vdots & \ddots & \vdots \\
a_{n-1} & a_{n-2} & a_{n-3} & \cdots & a_0
\end{pmatrix}
$$

即 $T_{ij} = a_{j-i}$，由 $2n-1$ 个参数 $\{a_{-(n-1)}, \dots, a_{n-1}\}$ 决定。

循环矩阵是 Toeplitz 矩阵的一个子类（多了一个「循环」条件：$a_k = a_{k-n}$）。

### 3.5 Toeplitz 矩阵乘向量的 O(n log n) 加速

Toeplitz 矩阵乘向量 $T \cdot v$ 可以**嵌入**成循环矩阵问题。

核心技巧：把 $T$ 扩展成 $2n \times 2n$ 的循环矩阵，把 $v$ 补零到 $2n$ 维。

具体做法：

1. 构造长度为 $2n$ 的向量 $c$：
   $$c_i = \begin{cases}
   a_i & 0 \le i < n \\
   0 & i = n \\
   a_{i-2n} & n < i < 2n
   \end{cases}$$

2. 构造 $2n$ 维的循环矩阵 $C$（第一行为 $c$）
3. 构造补零后的向量 $v' = (v_0, \dots, v_{n-1}, 0, \dots, 0)^T$
4. 计算 $w' = C \cdot v'$（用 FFT，$O(n \log n)$）
5. 取 $w'$ 的前 $n$ 个分量就是 $Tv$ 的结果

❓ **这个嵌入为什么正确？**

设 $C$ 是第一行为 $c$ 的 $2n \times 2n$ 循环矩阵。$C_{ij} = c_{(j-i) \bmod 2n}$。

对于 $0 \le i, j < n$，有 $(j-i) \bmod 2n = j-i$（因为 $|j-i| < n$），所以 $C_{ij} = a_{j-i} = T_{ij}$，只要 $c_{j-i} = a_{j-i}$。

对于 $i$ 从 $n$ 到 $2n-1$，$C_{ij}$ 不会影响前 $n$ 个结果分量，因为我们把 $v'$ 的后 $n$ 个分量设成了 0。

这里的关键是 $c$ 的构造：我们把 $a$ 的正负两部分分别放在 $c$ 的前半和后半，长度正好是 $2n$，使得对所有的 $0 \le i < n, 0 \le j < n$ 都有 $c_{(j-i) \bmod 2n} = a_{j-i}$。

**手算例子**：$T = \begin{pmatrix} 1 & 2 \\ 3 & 1 \end{pmatrix}$，$v = (1, 0)^T$。

直接算：$Tv = (1, 3)^T$。

用嵌入法：$n=2$，$2n=4$。

$c = (a_0, a_1, a_{-2}, a_{-1}) = (1, 3, 2, 1)$（这里我们按 $a_0, a_1, a_2, \dots$ 和 $a_{-1}, a_{-2}, \dots$ 的顺序）。

为了验证：构造：

$$C = \begin{pmatrix}
1 & 3 & 2 & 1 \\
1 & 1 & 3 & 2 \\
2 & 1 & 1 & 3 \\
3 & 2 & 1 & 1
\end{pmatrix}$$

$v' = (1, 0, 0, 0)^T$

$Cv' = (1, 1, 2, 3)^T$

取前 2 个分量：$(1, 3)$，和 $Tv$ 一致！

### 3.6 位移秩

Toeplitz 矩阵有一个重要的概念叫**位移秩**（displacement rank）。

定义位移算子 $\Delta(A) = A - Z A Z^T$，其中 $Z$ 是下移移位矩阵：

$$
Z = \begin{pmatrix}
0 & 0 & \cdots & 0 & 0 \\
1 & 0 & \cdots & 0 & 0 \\
0 & 1 & \cdots & 0 & 0 \\
\vdots & \vdots & \ddots & \vdots & \vdots \\
0 & 0 & \cdots & 1 & 0
\end{pmatrix}
$$

对于 Toeplitz 矩阵 $T$，可以证明 $\Delta(T)$ 的秩最多为 2（实际上，它只有两行非零元素）。这就是**位移秩等于 2** 的含义。

位移秩的概念有什么用？**低位移秩的矩阵可以用少量参数表示，并且可以快速做乘法**。Toeplitz 矩阵、Hankel 矩阵（倒序的 Toeplitz）、以及 Vandermonde 矩阵等都有低位移秩性质。

### 3.7 循环矩阵的求逆

循环矩阵的求逆也很简单。由于 $C = F^* \text{diag}(\hat{c}) F$，所以：

$$C^{-1} = F^* \text{diag}(\hat{c}^{-1}) F$$

即 $C^{-1}$ 也是循环矩阵，它的第一行是 $c$ 的 DFT 的逐点倒数再做 IDFT。

当然，这要求所有 $\hat{c}_k \neq 0$（否则 $C$ 不可逆）。

Toeplitz 矩阵的求逆就没有这么简单了，需要用 **Trench 算法** 或 **Gohberg-Semencul 公式** 在 $O(n^2)$ 内完成，不在本文讨论范围内。

---

## 四、代码实现

### 4.1 循环矩阵乘向量

```cpp
#include <bits/stdc++.h>
#include <complex>
using namespace std;
using cd = complex<double>;
const double PI = acos(-1);

void fft(vector<cd> &a, bool invert) {
    int n = a.size();
    for (int i = 1, j = 0; i < n; i++) {
        int bit = n >> 1;
        for (; j & bit; bit >>= 1) j ^= bit;
        j ^= bit;
        if (i < j) swap(a[i], a[j]);
    }
    for (int len = 2; len <= n; len <<= 1) {
        double ang = 2 * PI / len * (invert ? -1 : 1);
        cd wlen(cos(ang), sin(ang));
        for (int i = 0; i < n; i += len) {
            cd w(1);
            for (int j = 0; j < len/2; j++) {
                cd u = a[i+j], v = a[i+j+len/2] * w;
                a[i+j] = u + v;
                a[i+j+len/2] = u - v;
                w *= wlen;
            }
        }
    }
    if (invert) for (auto &x : a) x /= n;
}

// 循环矩阵乘向量：C(c) * v
// c[0..n-1] 是循环矩阵的第一行
vector<double> circulant_multiply(const vector<double>& c, const vector<double>& v) {
    int n = c.size();
    vector<cd> fc(c.begin(), c.end()), fv(v.begin(), v.end());
    fft(fc, false);
    fft(fv, false);
    for (int i = 0; i < n; i++) fc[i] *= fv[i];
    fft(fc, true);
    vector<double> res(n);
    for (int i = 0; i < n; i++) res[i] = fc[i].real();
    return res;
}
```

### 4.2 Toeplitz 矩阵乘向量

```cpp
// Toeplitz 矩阵乘向量：T * v
// a[0..n-1] 是主对角线和下方对角线元素（a[0]=a0, a[1]=a1, ..., a[n-1]=a_{n-1})
// a[-1], a[-2], ..., a[-(n-1)] 通过 a_neg[0..n-2] 传入（a_neg[0]=a_{-1}, ...）
vector<double> toeplitz_multiply(const vector<double>& a_pos,
                                  const vector<double>& a_neg,
                                  const vector<double>& v) {
    int n = a_pos.size();
    // 构造循环矩阵的第一行
    vector<double> c(2 * n, 0);
    for (int i = 0; i < n; i++) c[i] = a_pos[i];
    for (int i = 0; i < n - 1; i++) c[2 * n - 1 - i] = a_neg[i];
    // 补零扩展 v
    vector<double> v_ex(2 * n, 0);
    for (int i = 0; i < n; i++) v_ex[i] = v[i];
    // 用循环矩阵乘法计算
    auto res_ex = circulant_multiply(c, v_ex);
    // 取前 n 个分量
    vector<double> res(n);
    for (int i = 0; i < n; i++) res[i] = res_ex[i];
    return res;
}
```

### 4.3 循环矩阵求逆

```cpp
// 求循环矩阵 C(c) 的逆矩阵的第一行
// 返回第一行 c_inv，满足 C(c_inv) = C(c)^{-1}
vector<double> circulant_inverse(const vector<double>& c) {
    int n = c.size();
    vector<cd> fc(c.begin(), c.end());
    fft(fc, false);
    for (int i = 0; i < n; i++) {
        if (abs(fc[i]) < 1e-10) {
            // 不可逆
            return {};
        }
        fc[i] = 1.0 / fc[i];
    }
    fft(fc, true);
    vector<double> c_inv(n);
    for (int i = 0; i < n; i++) c_inv[i] = fc[i].real();
    return c_inv;
}
```

### 4.4 用 NTT 加速（模意义下）

在模素数 $p$ 下工作时，可以用 NTT 代替 FFT，适用于整系数的情况：

```cpp
// 模意义下的循环矩阵乘向量（需要先写好 NTT）
using ll = long long;
const ll MOD = 998244353, ROOT = 3;

// NTT 函数假设已经实现
void ntt(vector<ll>& a, bool invert);
// ...

vector<ll> circulant_multiply_mod(const vector<ll>& c, const vector<ll>& v) {
    int n = c.size();
    vector<ll> fc = c, fv = v;
    ntt(fc, false);
    ntt(fv, false);
    for (int i = 0; i < n; i++) fc[i] = fc[i] * fv[i] % MOD;
    ntt(fc, true);
    return fc;
}
```

---

## 五、应用场景

### 5.1 环形结构 DP

在环形结构上做 DP，转移只依赖于相对距离时，转移矩阵就是循环矩阵。可以利用循环矩阵快速幂 $O(n \log n \log k)$ 求出 $k$ 步后的状态。

例如：一个 $n$ 个点的环，每步可以从 $i$ 走到 $i\pm 1 \bmod n$（等概率）。求 $k$ 步后每个位置的概率分布。转移矩阵 $P$ 是循环矩阵（第一行为 $(\frac12, \frac12, 0, \dots, 0)$），$P^k$ 也是循环矩阵。

### 5.2 卷积

卷积 $c = a * b$ 的矩阵形式是 Toeplitz 矩阵：

$$
\begin{pmatrix}
b_0 & 0 & 0 & \cdots \\
b_1 & b_0 & 0 & \cdots \\
b_2 & b_1 & b_0 & \cdots \\
\vdots & \vdots & \vdots & \ddots
\end{pmatrix}
\begin{pmatrix}
a_0 \\ a_1 \\ a_2 \\ \vdots
\end{pmatrix}
=
\begin{pmatrix}
c_0 \\ c_1 \\ c_2 \\ \vdots
\end{pmatrix}
$$

所以 FFT 加速卷积就是 Toeplitz 矩阵乘向量的特例。

### 5.3 信号处理与图像处理

- 循环矩阵出现在**离散傅里叶变换对角化任意循环卷积**中
- 图像去模糊（deconvolution）中的 Toeplitz 矩阵
- 线性预测（linear prediction）中的 Toeplitz 矩阵

### 5.4 多项式运算

多项式的乘法和除法都可以写成 Toeplitz 矩阵的形式。利用 Toeplitz 的快速结构，可以做 $O(n \log n)$ 的多项式运算。

**推荐练习题**：

- [洛谷 P5559 失昼城](https://www.luogu.com.cn/problem/P5559) — 结合循环矩阵的图论问题
- [洛谷 P4721 分治 FFT](https://www.luogu.com.cn/problem/P4721) — 可以用 Toeplitz 矩阵加速
- [SPOJ MITH](https://www.spoj.com/problems/MITH/) — 循环矩阵乘法应用

---

## 六、小结

循环矩阵和 Toeplitz 矩阵是竞赛中两类常见的特殊结构矩阵：

| 矩阵类型 | 定义参数 | 乘向量复杂度 | 求逆复杂度 |
|---------|---------|-------------|-----------|
| 循环矩阵 | $n$ 个参数 | $O(n \log n)$ | $O(n \log n)$ |
| Toeplitz 矩阵 | $2n-1$ 个参数 | $O(n \log n)$ | $O(n^2)$（特殊算法） |

它们的核心共同点是**结构化**——不需要存储整个 $n \times n$ 矩阵，用少量参数就能完全描述，并且可以利用 FFT 高效运算。

循环矩阵的核心公式：$C = F^* \text{diag}(\hat{c}) F$。

Toeplitz 矩阵的核心技巧：嵌入到 $2n \times 2n$ 循环矩阵中。

下一篇我们讨论更激进的线性代数话题——**黑盒线性代数（Black Box LA）**，探讨如何在不显式构造矩阵的情况下进行线性代数运算。

---

> **系列索引**：本文是 ACM 竞赛数学系列的第 81 篇。
> 上一篇：[#80 范德蒙德矩阵与拉格朗日插值](80-范德蒙德矩阵与拉格朗日插值.md)
> 下一篇：[#82 黑盒线性代数（Black Box LA）](82-黑盒线性代数（Black Box LA）.md)
