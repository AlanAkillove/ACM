# 概率生成函数（PGF）

> Made by Aki.
> 最后更新于 2026.04.30

## 引言

在组合数学中，我们已经接触过普通生成函数（OGF）和指数生成函数（EGF）。这些生成函数将数列编码为幂级数，然后通过代数运算来推导数列的性质。

概率论中有一个类似的强大工具——**概率生成函数 (Probability Generating Function, PGF)**。它将一个取非负整数值的随机变量 $X$ 编码为幂级数：

$$G_X(z) = \mathbb{E}[z^X]$$

PGF 的美妙之处在于：随机变量的**期望、方差、甚至更高阶矩**都可以通过对 PGF 求导得到；两个独立随机变量之和的 PGF 就是它们 PGF 的乘积；而且许多分布（如几何分布、泊松分布）的 PGF 有简洁的封闭形式。

在 ACM 竞赛中，PGF 是解决涉及**整数值随机变量之和**、**随机过程首次到达时间**以及**分布高阶矩**问题的利器。

---

## 1. PGF 的定义与基本性质

### 1.1 定义

设 $X$ 是一个取非负整数值的随机变量（即 $X \in \{0,1,2,\dots\}$），其概率质量函数为 $p_k = P(X = k)$。则 $X$ 的**概率生成函数**定义为：

$$G_X(z) = \mathbb{E}[z^X] = \sum_{k=0}^\infty p_k z^k$$

这是一个以 $z$ 为变量的幂级数。通常在 $|z| \le 1$ 的范围内定义良好（因为 $\sum p_k = 1$，所以 $|G_X(z)| \le \sum p_k |z|^k \le 1$）。

> **PGF 和 OGF 的关系**：如果序列 $\{p_k\}$ 是一个概率分布，那么它的 OGF 就是它的 PGF。PGF 可以看作是一种特殊的 OGF——只不过它的系数有概率解释。

### 1.2 常见分布的 PGF

**1. 伯努利分布**：$X \sim \text{Bern}(p)$

$$G_X(z) = (1-p)z^0 + p z^1 = 1 - p + pz$$

**2. 二项分布**：$X \sim \text{Bin}(n, p)$

$$G_X(z) = \sum_{k=0}^n \binom{n}{k} p^k (1-p)^{n-k} z^k = (1-p + pz)^n$$

就是 $n$ 个独立伯努利变量 PGF 的乘积。

**3. 几何分布**：$X \sim \text{Geom}(p)$（$X$ 表示第一次成功前的失败次数，取值 $0,1,2,\dots$）

$$G_X(z) = \sum_{k=0}^\infty (1-p)^k p \cdot z^k = \frac{p}{1 - (1-p)z}$$

注意这里用的是"失败次数"版本。如果是"第一次成功所需的试验次数"版本（取值 $1,2,\dots$），则 $G_X(z) = \frac{pz}{1 - (1-p)z}$。

**4. 泊松分布**：$X \sim \text{Pois}(\lambda)$

$$G_X(z) = \sum_{k=0}^\infty e^{-\lambda} \frac{\lambda^k}{k!} z^k = e^{\lambda(z-1)}$$

这是一个极其简洁的封闭形式。

❓ **为什么 PGF 不定义在一般的随机变量上，而只定义在整值随机变量上？**

> PGF 的核心是 $z^k$ 这项，它要求随机变量的取值是"幂的指数"。如果 $X$ 取实数值（如正态分布），$\mathbb{E}[z^X]$ 就不是幂级数了。对于一般的随机变量，对应的工具是**矩母函数 (MGF)** $M_X(t) = \mathbb{E}[e^{tX}]$ 和**特征函数 (CF)** $\varphi_X(t) = \mathbb{E}[e^{itX}]$。但竞赛中最常处理的是整值随机变量，所以 PGF 更实用。

---

## 2. 从 PGF 提取矩

PGF 的一个核心用途是快速计算随机变量的各阶矩。

### 2.1 期望：E[X] = G'(1)

对 $G_X(z) = \sum_{k=0}^\infty p_k z^k$ 求导：

$$G'_X(z) = \sum_{k=1}^\infty k p_k z^{k-1}$$

令 $z = 1$：

$$G'_X(1) = \sum_{k=1}^\infty k p_k = \mathbb{E}[X]$$

**简洁！** 随机变量的期望等于 PGF 在 $z=1$ 处的一阶导数。

### 2.2 方差与二阶矩

对 PGF 求二阶导：

$$G''_X(z) = \sum_{k=2}^\infty k(k-1) p_k z^{k-2}$$

$$G''_X(1) = \mathbb{E}[X(X-1)] = \mathbb{E}[X^2] - \mathbb{E}[X]$$

所以：

$$\mathbb{E}[X^2] = G''_X(1) + G'_X(1)$$

$$\text{Var}(X) = \mathbb{E}[X^2] - (\mathbb{E}[X])^2 = G''_X(1) + G'_X(1) - (G'_X(1))^2$$

### 2.3 递降阶乘矩

更一般地，$r$ 阶**递降阶乘矩 (Factorial Moment)** 为：

$$\mathbb{E}[(X)_r] = \mathbb{E}[X(X-1)\cdots(X-r+1)] = G^{(r)}_X(1)$$

其中 $G^{(r)}_X$ 表示 $r$ 阶导数。

**手算例子**：几何分布 $X \sim \text{Geom}(p)$（失败次数版本）

$$G_X(z) = \frac{p}{1-(1-p)z}$$

一阶导数：

$$G'_X(z) = \frac{p(1-p)}{(1-(1-p)z)^2}$$

$$G'_X(1) = \frac{p(1-p)}{(1-(1-p))^2} = \frac{p(1-p)}{p^2} = \frac{1-p}{p}$$

这就是几何分布失败次数版本的期望——$\mathbb{E}[X] = \frac{1-p}{p}$。

二阶导数：

$$G''_X(z) = \frac{2p(1-p)^2}{(1-(1-p)z)^3}$$

$$G''_X(1) = \frac{2p(1-p)^2}{p^3} = \frac{2(1-p)^2}{p^2}$$

$$\text{Var}(X) = G''_X(1) + G'_X(1) - (G'_X(1))^2 = \frac{2(1-p)^2}{p^2} + \frac{1-p}{p} - \frac{(1-p)^2}{p^2} = \frac{1-p}{p^2}$$

和已知的几何分布方差一致。

❓ **G'(1) 一定存在吗？**

> 需要 PGF 在 $z=1$ 处可导。如果 $\mathbb{E}[X] = \infty$（例如某些厚尾分布），那么 $G'(1)$ 会发散。在竞赛中，我们处理的几乎所有分布的期望都是有限的，所以不用太担心这个问题。

---

## 3. PGF 的运算性质

### 3.1 独立随机变量之和

设 $X$ 和 $Y$ 独立，$Z = X + Y$。则：

$$G_Z(z) = \mathbb{E}[z^{X+Y}] = \mathbb{E}[z^X \cdot z^Y] = \mathbb{E}[z^X] \cdot \mathbb{E}[z^Y] = G_X(z) \cdot G_Y(z)$$

**独立随机变量之和的 PGF 等于 PGF 的乘积。**

这个性质非常强大——它把卷积运算（概率质量函数的卷积）转化为简单的乘法。

### 3.2 随机个随机变量之和

设 $X_1, X_2, \dots$ 是独立同分布的随机变量，$N$ 是一个非负整值随机变量（与 $X_i$ 独立）。考虑随机和：

$$S = \sum_{i=1}^N X_i$$

则 $S$ 的 PGF 为（这就是随机变量的**复合分布**）：

$$G_S(z) = G_N(G_X(z))$$

**证明**：

$$G_S(z) = \mathbb{E}[z^S] = \mathbb{E}[\mathbb{E}[z^{\sum_{i=1}^N X_i} \mid N]] = \mathbb{E}[(\mathbb{E}[z^{X_1}])^N] = \mathbb{E}[(G_X(z))^N] = G_N(G_X(z))$$

这个性质在保险精算、排队论中应用广泛，在竞赛中也时有出现。

### 3.3 线性变换

设 $Y = aX + b$，其中 $a, b$ 是常数。一般地，$Y$ 可能不再取整数值（除非 $a$ 是整数），但形式上：

$$G_Y(z) = \mathbb{E}[z^{aX+b}] = z^b \cdot \mathbb{E}[(z^a)^X] = z^b \cdot G_X(z^a)$$

---

## 4. PGF 与 OGF、EGF 的关系

### 4.1 概览

| 类型 | 定义 | 用途 |
|------|------|------|
| OGF | $A(z) = \sum a_n z^n$ | 组合计数，数列通项 |
| EGF | $A(z) = \sum a_n \frac{z^n}{n!}$ | 带标号对象的计数 |
| PGF | $G_X(z) = \sum p_k z^k$ | 概率分布的分析 |

PGF 和 OGF 在形式上完全一致，但解读不同：
- OGF 的系数 $a_n$ 是组合对象的数目
- PGF 的系数 $p_k$ 是概率

### 4.2 概率解释与组合解释的统一

很多组合恒等式同时有概率解释。例如，二项式定理：

$$(1 + z)^n = \sum_{k=0}^n \binom{n}{k} z^k$$

可以看作二项分布 $\text{Bin}(n, \frac{z}{1+z})$ 的 PGF 乘以 $(1+z)^n$。

另一个重要的联系是：如果 $a_n$ 是某个组合对象的计数，且 $\sum a_n$ 有限，那么 $p_n = a_n / \sum a_n$ 就是一个概率分布。此时 PGF 就是归一化后的 OGF。

### 4.3 谱定理

PGF 的一些性质在组合生成函数中没有对应。例如，PGF 的导数在 $z=1$ 处给出矩——生成函数没有这个性质（因为系数不是概率分布时，$A(1)$ 是总数而不是 1）。

❓ **竞赛中什么时候该用 PGF，什么时候该用 OGF？**

> OGF 用于求数列的通项公式或估计渐近行为；PGF 用于分析随机变量的矩和分布。当一个问题既有计数解释又有概率解释时，两者可以互相转化。例如，"
投掷 $n$ 次骰子，总点数为 $s$ 的方案数"可以用 OGF $\left(\sum_{i=1}^6 z^i\right)^n$ 的系数表示——这同时也是离散均匀分布之和的 PGF（乘以 $6^n$）。

---

## 5. 竞赛中的应用

### 5.1 🏆 ARC154F - Dice

**简要题意**：掷一个 $m$ 面的骰子，每次等概率掷出 $1$ 到 $m$ 的点数。求需要掷多少次才能使所有面都至少出现过一次？

这个问题是**优惠券收集问题 (Coupon Collector)**，但用 PGF 的角度能更深刻地理解其结构。

设 $X$ 为收集所有 $m$ 种面所需的次数。$X$ 可以分解为：

$$X = X_1 + X_2 + \cdots + X_m$$

其中 $X_1 = 1$，$X_k$ 是已经收集了 $k-1$ 种面后，收集第 $k$ 种新面所需的次数。

$X_k$ 服从几何分布：$X_k - 1 \sim \text{Geom}(\frac{m-k+1}{m})$（成功概率为 $\frac{m-k+1}{m}$）。

几何分布的 PGF：

$$G_{X_k}(z) = \frac{\frac{m-k+1}{m} \cdot z}{1 - \frac{k-1}{m} \cdot z}$$

由独立随机变量之和的性质：

$$G_X(z) = \prod_{k=1}^m \frac{\frac{m-k+1}{m} \cdot z}{1 - \frac{k-1}{m} \cdot z}$$

从这个 PGF 出发，可以推导 $X$ 的精确分布和矩。例如，期望：

$$\mathbb{E}[X] = G'_X(1) = \sum_{k=1}^m \mathbb{E}[X_k] = \sum_{k=1}^m \frac{m}{m-k+1} = m \cdot H_m$$

这就是经典的优惠券收集问题期望。

### 5.2 🏆 CF 891E - Lust

**简要题意**：有一个长度为 $n$ 的数组 $a$，进行 $k$ 次操作。每次操作随机选择一个下标 $i$，将 $ans$ 加上 $\prod_{j \neq i} a_j$，然后将 $a_i$ 减 1。求 $k$ 次操作后 $ans$ 的期望。

**思路分析**：

这个问题看似复杂，但用 PGF 可以优雅地解决。

关键观察：$\prod_{j \neq i} a_j$ 就是 $\frac{\prod a_j}{a_i}$。如果我们记 $b_i$ 为操作结束后 $a_i$ 被减去的次数（$\sum b_i = k$），那么总贡献为：

$$\prod_{i=1}^n a_i - \prod_{i=1}^n (a_i - b_i)$$

这是常用的"telescoping"技巧——每次操作相当于从乘积中"拿走"一个因子。

所以期望：

$$\mathbb{E}[ans] = \prod a_i - \mathbb{E}\left[\prod (a_i - b_i)\right]$$

现在问题转化为：求 $\mathbb{E}\left[\prod (a_i - b_i)\right]$，其中 $(b_1,\dots,b_n)$ 是 $k$ 步均匀随机选择的多项分布。

记 $f(x) = \prod_{i=1}^n (a_i - x_i)$，我们可以用 PGF 来求 $b_i$ 的联合分布。

每个 $b_i$ 的边缘分布是 $\text{Bin}(k, 1/n)$，但 $b_i$ 之间不独立（$\sum b_i = k$）。联合 PGF 为：

$$G(z_1,\dots,z_n) = \left(\frac{z_1 + \cdots + z_n}{n}\right)^k$$

那么：

$$\mathbb{E}\left[\prod (a_i - b_i)\right] = \prod a_i \cdot \mathbb{E}\left[\prod \left(1 - \frac{b_i}{a_i}\right)\right]$$

这里需要将 $b_i$ 的分布代入。可以利用 PGF 的一个技巧：

$$\mathbb{E}\left[\prod (1 - \frac{b_i}{a_i})\right]$$

可以通过积分变换或生成函数操作得到。最终的简洁结果是：

$$\mathbb{E}[ans] = \prod a_i - \left[\prod (a_i - \frac{\partial}{\partial t_i})\right] \left(\frac{\sum e^{t_i}}{n}\right)^k \Big|_{t=0}$$

虽然需要一定的高级技巧，但 PGF 的思路清晰地将"随机挑选"编码为多项式运算。

---

## 6. 代码实现：从 PGF 求矩的模板

下面的代码演示了如何利用 PGF 的导数来快速计算期望和方差。

```cpp
#include <bits/stdc++.h>
using ll = long long;
using Poly = std::vector<double>;

// 计算多项式在 z=1 处的导数
// poly 的系数是 p_0, p_1, ..., p_n
// 假设共有 n+1 项

// 计算 G(1) = sum(p_k)
double eval_at_one(const Poly& p) {
    double sum = 0;
    for (double pk : p) sum += pk;
    return sum;  // 应该为 1
}

// 计算 G'(1) = sum(k * p_k)
double first_deriv_at_one(const Poly& p) {
    double sum = 0;
    for (size_t k = 1; k < p.size(); ++k) {
        sum += (double)k * p[k];
    }
    return sum;  // 期望 E[X]
}

// 计算 G''(1) = sum(k * (k-1) * p_k)
double second_deriv_at_one(const Poly& p) {
    double sum = 0;
    for (size_t k = 2; k < p.size(); ++k) {
        sum += (double)k * (k - 1) * p[k];
    }
    return sum;
}

// 从概率分布计算期望和方差
std::pair<double, double> mean_and_variance(const Poly& p) {
    double E_X = first_deriv_at_one(p);
    double E_XX1 = second_deriv_at_one(p);
    double E_X2 = E_XX1 + E_X;
    double Var_X = E_X2 - E_X * E_X;
    return {E_X, Var_X};
}

// 验证：二项分布 Bin(n, p) 的 PGF 是 (1-p+pz)^n
// 展开系数即为 P(X=k) = C(n,k) * p^k * (1-p)^(n-k)
Poly binomial_pmf(int n, double p) {
    Poly res(n + 1, 0.0);
    double q = 1.0 - p;
    for (int k = 0; k <= n; ++k) {
        double comb = 1.0;
        for (int i = 1; i <= k; ++i) {
            comb = comb * (n - i + 1) / i;
        }
        res[k] = comb * std::pow(p, k) * std::pow(q, n - k);
    }
    return res;
}

int main() {
    // 验证二项分布 Bin(10, 0.3)
    auto binom = binomial_pmf(10, 0.3);
    auto [E, Var] = mean_and_variance(binom);
    
    std::cout << "二项分布 Bin(10, 0.3):" << std::endl;
    std::cout << "  计算期望: " << E << " (理论值: " << 10 * 0.3 << ")" << std::endl;
    std::cout << "  计算方差: " << Var << " (理论值: " << 10 * 0.3 * 0.7 << ")" << std::endl;
    
    // 验证泊松分布 Pois(lambda)
    double lambda = 5.0;
    // 泊松分布理论上有无穷多项，截断到 k=20
    Poly poisson(21, 0.0);
    for (int k = 0; k <= 20; ++k) {
        poisson[k] = std::exp(-lambda) * std::pow(lambda, k);
        for (int i = 1; i <= k; ++i) poisson[k] /= i;
    }
    
    auto [E2, Var2] = mean_and_variance(poisson);
    std::cout << "\n泊松分布 Pois(5.0) (截断到 k=20):" << std::endl;
    std::cout << "  计算期望: " << E2 << " (理论值: " << lambda << ")" << std::endl;
    std::cout << "  计算方差: " << Var2 << " (理论值: " << lambda << ")" << std::endl;
    
    return 0;
}
```

---

## 7. 推荐练习题

1. **AtCoder ARC154F - Dice**：利用 PGF 分析优惠券收集问题的分布。
   - 链接：https://atcoder.jp/contests/arc154/tasks/arc154_f

2. **Codeforces 891E - Lust**：经典 PGF 应用题，期望与生成函数的结合。
   - 链接：https://codeforces.com/problemset/problem/891/E

3. **Project Euler 323 - Bitwise-AND operations**：可以用 PGF 分析二进制随机过程。

---

## 8. 小结

概率生成函数（PGF）是连接生成函数和概率论的桥梁：

- **定义**：$G_X(z) = \mathbb{E}[z^X] = \sum p_k z^k$
- **求矩**：$\mathbb{E}[X] = G'(1)$，$\mathbb{E}[X(X-1)] = G''(1)$，一般地 $\mathbb{E}[(X)_r] = G^{(r)}(1)$
- **独立和**：$G_{X+Y}(z) = G_X(z) \cdot G_Y(z)$（独立时）
- **随机和**：$G_{\sum_{i=1}^N X_i}(z) = G_N(G_X(z))$（复合分布）

PGF 在分析以下问题时特别有优势：
1. 独立整值随机变量之和的分布
2. 分布的矩（尤其是高阶矩）计算
3. 随机过程首次到达时间的分布分析
4. 带随机个随机变量的复合分布

下一篇文章我们将回到马尔可夫链的话题——但不是吸收链，而是**一般马尔可夫链**，并探讨如何用**高斯消元**求解带环的期望和概率问题。

---

> **系列索引**：本文是 ACM 竞赛数学系列的第 70 篇。
> 上一篇：[#69 吸收马尔可夫链](./69-吸收马尔可夫链.md)
> 下一篇：[#71 马尔可夫链与高斯消元](./71-马尔可夫链与高斯消元.md)
