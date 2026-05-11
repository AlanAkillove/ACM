# 期望Min-Max容斥

> Made by Aki.
> 最后更新于 2026.04.30

## 引言

在组合数学中，容斥原理（Inclusion-Exclusion Principle）是我们熟知的工具——通过逐个添加和减去交集来求并集的大小。

但在概率与期望中，有一个**更深刻、更强大**的容斥关系——**Min-Max 容斥**。它揭示了随机变量的最小值与最大值之间的对偶关系：

$$\mathbb{E}[\max(S)] = \sum_{\emptyset \neq T \subseteq S} (-1)^{|T|-1} \cdot \mathbb{E}[\min(T)]$$

这个公式有什么用？试想以下场景：

- 收集 $n$ 种不同的卡片，每次随机获得一种。收集全套所需次数的期望是多少？
- 有 $n$ 个独立的事件，每个事件以某个速率发生，求"所有事件都至少发生一次"的时刻的期望

这两个问题都可以用期望 Min-Max 容斥优雅地解决。经典问题如"优惠券收集问题"的期望公式 $\mathbb{E}[T] = n \cdot H_n$ 是它的一个特例。

更棒的是，Min-Max 容斥还可以推广到求第 $k$ 大的值，以及用 SOS DP / FWT 来加速子集求和——这使得它能处理 $n$ 高达 $20$ 甚至更大的问题。

---

## 1. Min-Max 容斥的基本形式

### 1.1 集合上的 Min-Max 容斥

设 $S$ 是一个实数集合。以下恒等式成立：

$$\max(S) = \sum_{\emptyset \neq T \subseteq S} (-1)^{|T|-1} \cdot \min(T)$$

$$\min(S) = \sum_{\emptyset \neq T \subseteq S} (-1)^{|T|-1} \cdot \max(T)$$

**证明思路**（以第一个公式为例）：

设 $S = \{a_1, a_2, \dots, a_n\}$，将元素从大到小排序 $a_{(1)} \ge a_{(2)} \ge \cdots \ge a_{(n)}$。

考虑 $\min(T) = a_{(k)}$，当 $T$ 中包含 $a_{(1)}, a_{(2)}, \dots, a_{(k-1)}$ 中的任意子集，且包含 $a_{(k)}$，且不包含任何小于 $a_{(k)}$ 的元素。这样的 $T$ 有 $2^{k-1}$ 种。

贡献为 $\sum_{T: \min(T)=a_{(k)}} (-1)^{|T|-1} a_{(k)} = a_{(k)} \sum_{j=1}^{k} \binom{k-1}{j-1} (-1)^{j-1}$。

里面的求和 $\sum_{j=1}^{k} \binom{k-1}{j-1} (-1)^{j-1} = (1-1)^{k-1} = [k=1]$。

所以只有 $a_{(1)}$（最大值）的系数为 1，其余均为 0。因此右边等于 $\max(S)$。

**这个证明本质上就是容斥原理**——最大值可以表示为所有子集最小值的交替和。

### 1.2 期望的 Min-Max 容斥

如果 $S$ 是一个随机变量集合（不一定独立！），则：

$$\mathbb{E}[\max(S)] = \sum_{\emptyset \neq T \subseteq S} (-1)^{|T|-1} \cdot \mathbb{E}[\min(T)]$$

这里不需要独立性假设——Min-Max 容斥是点态成立的恒等式，两边取期望后仍然成立。

> 这是 Min-Max 容斥在概率论中最美妙的地方——即使随机变量之间高度相关，公式仍然成立。因为 $\max(S)$ 和 $\min(T)$ 之间的关系是**确定性的代数恒等式**，和概率分布无关。

### 1.3 特例：优惠券收集问题

设 $X_i$ 为第 $i$ 种券第一次出现的时刻（可能无限）。$\max\{X_1,\dots,X_n\}$ 就是所有 $n$ 种券都至少出现一次的时刻。

令 $\mathbb{E}[\min(T)]$ 表示集合 $T$ 中**任意一种券**首次出现的期望时刻。

如果每次独立均匀地从 $n$ 种券中选一种，那么 $\min(T)$ 服从几何分布，成功概率为 $|T|/n$：

$$\mathbb{E}[\min(T)] = \frac{n}{|T|}$$

代入 Min-Max 容斥：

$$\mathbb{E}[\max(S)] = \sum_{\emptyset \neq T \subseteq S} (-1)^{|T|-1} \cdot \frac{n}{|T|}$$

按 $|T| = k$ 分组。大小为 $k$ 的子集有 $\binom{n}{k}$ 个：

$$\mathbb{E}[\max(S)] = \sum_{k=1}^n \binom{n}{k} (-1)^{k-1} \cdot \frac{n}{k}$$

这个和等于 $n \cdot H_n$（这是一个已知的组合恒等式）。对于 $n=5$：

$$\begin{aligned}
\mathbb{E}[\max] &= 5\left(1 - \frac{1}{2} + \frac{1}{3} - \frac{1}{4} + \frac{1}{5}\right) \\
&= 5 \cdot \frac{47}{60} \approx 3.917
\end{aligned}$$

而 $5H_5 = 5 \times (1 + \frac{1}{2} + \frac{1}{3} + \frac{1}{4} + \frac{1}{5}) = 5 \times \frac{137}{60} \approx 11.417$。

期望最大（收集全套）比期望最小（收集任意一种）要慢得多——这就是优惠券收集问题"越到后面越难收集"的本质。

❓ **为什么优惠券收集问题的最小值期望是 $n/|T|$？**

> $\min(T)$ 表示 $T$ 中任意一个元素首次出现的时间。每次抽取，抽到 $T$ 中某元素的概率是 $|T|/n$。几何分布告诉我们，首次成功（抽到 $T$ 中元素）的期望次数是 $n/|T|$。注意这里的关键：我们只关心 $T$ 中"任意一个"出现，不是"全部"出现。

---

## 2. k-th Min-Max 容斥

### 2.1 扩展形式

基本 Min-Max 容斥只涉及最大值和最小值。如果我们想要第 $k$ 大的值呢？

设 $S$ 有 $n$ 个元素。记 $\max_k(S)$ 为 $S$ 中第 $k$ 大的元素（$\max_1$ 是最大值，$\max_n$ 是最小值）。则有：

$$\mathbb{E}[\max_k(S)] = \sum_{\emptyset \neq T \subseteq S} (-1)^{|T|-k} \cdot \binom{|T|-1}{k-1} \cdot \mathbb{E}[\min(T)]$$

等价地：

$$\mathbb{E}[\max_k(S)] = \sum_{j=k}^n (-1)^{j-k} \cdot \binom{j-1}{k-1} \cdot \sum_{T: |T|=j} \mathbb{E}[\min(T)]$$

**对称形式**（用最大值表达最小值）：

$$\mathbb{E}[\min_k(S)] = \sum_{\emptyset \neq T \subseteq S} (-1)^{|T|-k} \cdot \binom{|T|-1}{k-1} \cdot \mathbb{E}[\max(T)]$$

### 2.2 手算小例子

**题目**：掷一个公平的六面骰子，每次掷出后记录出现的点数。求所有 6 种点数都至少出现一次时，第 2 大的点数（即第 5 种出现的点数）的期望。

这个例子比较复杂，我们换一个更简单的。

**题目**：有 3 个独立的指数随机变量 $X_1, X_2, X_3$，各自的速率参数为 $\lambda_1, \lambda_2, \lambda_3$。求 $\max_k(S)$ 的期望，其中 $S = \{X_1, X_2, X_3\}$。

**对于指数分布**，$\mathbb{E}[\min(T)] = \frac{1}{\sum_{i \in T} \lambda_i}$（指数分布的最小值仍然是指数分布，速率为参数之和）。

令 $\lambda_1 = 1, \lambda_2 = 2, \lambda_3 = 3$。

求 $\mathbb{E}[\max(S)] = \mathbb{E}[\max_1(S)]$（验证基本公式）：

$$\begin{aligned}
\mathbb{E}[\max(S)] &= \sum_{\emptyset \neq T} (-1)^{|T|-1} \frac{1}{\sum_{i \in T} \lambda_i} \\
&= \left(\frac{1}{1} + \frac{1}{2} + \frac{1}{3}\right) \\
&\quad - \left(\frac{1}{1+2} + \frac{1}{1+3} + \frac{1}{2+3}\right) \\
&\quad + \frac{1}{1+2+3} \\
&= \left(1 + 0.5 + \frac{1}{3}\right) - \left(\frac{1}{3} + \frac{1}{4} + \frac{1}{5}\right) + \frac{1}{6} \\
&= 1.833 - 0.783 + 0.167 = 1.217
\end{aligned}$$

求 $\mathbb{E}[\max_2(S)]$（第二大，即中位数）：

$$\begin{aligned}
\mathbb{E}[\max_2(S)] &= \sum_{T} (-1)^{|T|-2} \binom{|T|-1}{1} \mathbb{E}[\min(T)] \\
&= \sum_{T: |T|=2} (-1)^{0} \binom{1}{1} \mathbb{E}[\min(T)] + \sum_{T: |T|=3} (-1)^{1} \binom{2}{1} \mathbb{E}[\min(T)] \\
&= \left(\frac{1}{3} + \frac{1}{4} + \frac{1}{5}\right) - 2 \cdot \frac{1}{6} \\
&= 0.783 - 0.333 = 0.450
\end{aligned}$$

求 $\mathbb{E}[\min(S)] = \mathbb{E}[\max_3(S)]$（最小值，即第三大）：

$$\begin{aligned}
\mathbb{E}[\min(S)] &= \sum_{T} (-1)^{|T|-3} \binom{|T|-1}{2} \mathbb{E}[\min(T)] \\
&= \sum_{T: |T|=3} (-1)^{0} \binom{2}{2} \mathbb{E}[\min(T)] \\
&= \frac{1}{6} \approx 0.167
\end{aligned}$$

**验算**：最小值就是 $\min$ 的期望，直接计算 $\mathbb{E}[\min(S)] = \frac{1}{\lambda_1+\lambda_2+\lambda_3} = \frac{1}{6}$，一致！最大值 1.217、中位数 0.450、最小值 0.167，合理。

❓ **k-th Min-Max 容斥的系数是怎么来的？**

> 这个公式可以通过对基本 Min-Max 容斥反复应用得到，也可以用组合恒等式直接推导。系数的组合意义是：在 $\min(T)$ 对 $\max_k$ 的贡献中，需要计算 $T$ 恰好包含 $\max_k$ 且不包含 $\max_1,\dots,\max_{k-1}$ 的所有子集的总"符号贡献"，这个求和的结果就是 $(-1)^{|T|-k}\binom{|T|-1}{k-1}$。

---

## 3. SOS DP / FWT 优化

### 3.1 子集求和问题

Min-Max 容斥需要对所有非空子集 $T \subseteq S$ 求和。如果 $|S| = n$，直接枚举所有 $2^n$ 个子集，当 $n$ 较大时不可行。

但很多情况下，$\mathbb{E}[\min(T)]$ 只依赖于 $T$ 的某个简单性质（如 $|T|$ 大小、元素和、权值等），这时可以用**子集 DP (SOS DP)** 或**快速沃尔什变换 (FWT)** 来加速计算。

### 3.2 基本 Min-Max 容斥的加速

回顾：

$$\mathbb{E}[\max(S)] = \sum_{\emptyset \neq T \subseteq S} (-1)^{|T|-1} f(T)$$

其中 $f(T) = \mathbb{E}[\min(T)]$。

如果 $f(T)$ 可以写成 $F(T)$ 关于子集信息的函数（如 $f(T) = g(|T|)$），我们可以直接按大小分组——就回到了 $n \cdot H_n$ 这种形式。

如果 $f(T)$ 是更复杂的函数，比如 $f(T) = \frac{1}{\sum_{i \in T} p_i}$（其中 $p_i$ 是元素权值），我们需要对每个可能的和值计算贡献。对于小 $n$（$\le 20$）可以枚举，更大时可能需要其他技巧。

### 3.3 k-th Min-Max 容斥的加速

对于 $\mathbb{E}[\max_k(S)]$，公式为：

$$\mathbb{E}[\max_k(S)] = \sum_{j=k}^n (-1)^{j-k} \cdot \binom{j-1}{k-1} \cdot \sum_{T: |T|=j} \mathbb{E}[\min(T)]$$

如果我们将 $\mathbb{E}[\min(T)]$ 表示成子集函数的形式，那么 $\sum_{T: |T|=j} \mathbb{E}[\min(T)]$ 就是一个**大小为 $j$ 的子集和**问题。

对于某些形式的 $\mathbb{E}[\min(T)]$（如 $T$ 中元素权值的最小值、最大值等），可以用 SOS DP 加速。

### 3.4 SOS DP 模板

```cpp
#include <bits/stdc++.h>
using ll = long long;

// SOS DP (Sum Over Subsets)
// f[mask] 是原始定义的函数值
// 计算后 g[mask] = sum_{sub ⊆ mask} f[sub]
template<typename T>
void sos_dp(std::vector<T>& f, int n) {
    int size = 1 << n;
    std::vector<T> g = f;
    for (int i = 0; i < n; ++i) {
        for (int mask = 0; mask < size; ++mask) {
            if (mask & (1 << i)) {
                g[mask] += g[mask ^ (1 << i)];
            }
        }
    }
    // 现在 g[mask] = sum_{sub ⊆ mask} f[sub]
    // 复制回 f
    f = g;
}

// 另一种形式：对超集求和
// g[mask] = sum_{sup ⊇ mask} f[sup]
template<typename T>
void sos_superset_dp(std::vector<T>& f, int n) {
    int size = 1 << n;
    std::vector<T> g = f;
    for (int i = 0; i < n; ++i) {
        for (int mask = 0; mask < size; ++mask) {
            if (!(mask & (1 << i))) {
                g[mask] += g[mask | (1 << i)];
            }
        }
    }
    f = g;
}

// 对 Min-Max 容斥的应用示例
// 假设有 n 个元素，求期望最大值
// f[mask] = E[min(T)] for T = mask
// 返回 E[max(S)]
double min_max_exclusion(const std::vector<double>& f, int n) {
    int size = 1 << n;
    std::vector<double> g = f;
    // 先做子集和 DP
    sos_dp(g, n);
    // 但现在 g[mask] = sum_{sub ⊆ mask} f[sub]
    // 我们想要的是 sum_{∅≠T⊆S} (-1)^{|T|-1} f[T]
    // 可以用容斥逐项计算
    double result = 0.0;
    for (int mask = 1; mask < size; ++mask) {
        int bits = __builtin_popcount(mask);
        if (bits % 2 == 1) {
            result += f[mask];
        } else {
            result -= f[mask];
        }
    }
    return result;
}
```

> **注意**：SOS DP 并不能直接给出带符号的 Min-Max 容斥和，但可以高效计算 $\sum_{sub \subseteq mask} f[sub]$ 或 $\sum_{sup \supseteq mask} f[sub]$，这在很多期望问题中非常有用。

---

## 4. 🏆 洛谷 P3175 (HAOI2015 按位或)

### 4.1 题目描述

初始时有一个数字 $x = 0$。每秒以概率 $p_i$ 获得数字 $i$（$0 \le i < 2^n$），并将 $x$ 更新为 $x \mid i$（按位或）。求 $x$ 第一次变为 $2^n - 1$（所有 $n$ 位都是 1）的期望秒数。

### 4.2 思路分析

令 $S = \{0, 1, 2, \dots, n-1\}$ 为 $n$ 个二进制位。设 $X_k$ 为第 $k$ 位第一次变成 1 的时刻。

我们要求的是 $\mathbb{E}[\max_{k \in S} X_k]$——所有位都变成 1 的时刻。

由 Min-Max 容斥：

$$\mathbb{E}[\max(S)] = \sum_{\emptyset \neq T \subseteq S} (-1)^{|T|-1} \cdot \mathbb{E}[\min(T)]$$

$\min(T)$ 表示 $T$ 中**任意一位**第一次变成 1 的时刻。每次操作，$T$ 中某一位变成 1 的概率，等于抽到的数字 $i$ 满足 $i \land T \neq 0$ 的概率。

所以 $\mathbb{E}[\min(T)] = \frac{1}{P(T)}$，其中 $P(T) = \sum_{i \land T \neq 0} p_i = 1 - \sum_{i \land T = 0} p_i$。

于是：

$$\mathbb{E}[\max(S)] = \sum_{\emptyset \neq T \subseteq S} (-1)^{|T|-1} \frac{1}{1 - \sum_{i \land T = 0} p_i}$$

问题转化为对每个 $T$ 计算 $\sum_{i \land T = 0} p_i$——即所有与 $T$ 无交的 $i$ 的概率和。

这恰好可以用**SOS DP 的超集和**来高效计算：$g[mask] = \sum_{i \supseteq mask} p_i$。那么对于 $T$，与 $T$ 无交的集合就是 $mask \subseteq \overline{T}$（$T$ 的补集的子集）。

### 4.3 代码实现

```cpp
#include <bits/stdc++.h>
using ll = long long;

// SOS DP 计算超集和
// 输入 f[mask]，输出 g[mask] = sum_{sup ⊇ mask} f[sup]
void superset_sum(std::vector<double>& f, int n) {
    int size = 1 << n;
    for (int i = 0; i < n; ++i) {
        for (int mask = 0; mask < size; ++mask) {
            if (!(mask & (1 << i))) {
                f[mask] += f[mask | (1 << i)];
            }
        }
    }
}

int main() {
    int n;
    std::cin >> n;
    int size = 1 << n;
    
    std::vector<double> p(size, 0.0);
    for (int i = 0; i < size; ++i) {
        std::cin >> p[i];
    }
    
    // SOS DP 求超集和
    // sum_over_sup[mask] = sum_{i ⊇ mask} p[i]
    std::vector<double> sum_over_sup = p;
    superset_sum(sum_over_sup, n);
    
    // 应用 Min-Max 容斥
    double ans = 0.0;
    for (int mask = 1; mask < size; ++mask) {
        // complement = (~mask) & (size-1)
        int complement = (~mask) & (size - 1);
        // 与 mask 无交的集合的概率和 = sum_over_sup[complement]
        double prob_T = 1.0 - sum_over_sup[complement];
        
        if (prob_T < 1e-12) {
            // 如果某位永远无法变为 1，则不可能达到全 1
            std::cout << "INF" << std::endl;
            return 0;
        }
        
        double E_min_T = 1.0 / prob_T;
        int bits = __builtin_popcount(mask);
        if (bits % 2 == 1) {
            ans += E_min_T;
        } else {
            ans -= E_min_T;
        }
    }
    
    std::cout << std::fixed << std::setprecision(10) << ans << std::endl;
    
    return 0;
}
```

---

## 5. 🏆 洛谷 P4707 (重返现世)

### 5.1 题目描述

有 $n$ 种物品，每次随机获得一种，获得第 $i$ 种的概率为 $\frac{p_i}{m}$（$m = \sum p_i$）。求获得**恰好 $k$ 种不同物品**的期望次数。

### 5.2 思路分析

这是一个 k-th Min-Max 容斥的经典应用。

设 $X_i$ 为第 $i$ 种物品首次出现的时刻。我们要求的是第 $(n-k+1)$ 大的 $X_i$——即所有 $n$ 种物品中，第 $n-k+1$ 个出现的物品的时刻（因为"收集到 $k$ 种不同物品"等价于第 $n-k+1$ 个物品出现）。

利用 k-th Min-Max 容斥：

$$\mathbb{E}[\max_{n-k+1}(S)] = \sum_{\emptyset \neq T \subseteq S} (-1)^{|T|-(n-k+1)} \cdot \binom{|T|-1}{n-k} \cdot \mathbb{E}[\min(T)]$$

其中 $\mathbb{E}[\min(T)] = \frac{m}{\sum_{i \in T} p_i}$（几何分布，成功概率为 $\frac{\sum p_i}{m}$）。

令 $K = n - k + 1$（要求的第 $K$ 大）：

$$\mathbb{E}[\max_K(S)] = \sum_{\emptyset \neq T} (-1)^{|T|-K} \binom{|T|-1}{K-1} \cdot \frac{m}{\sum_{i \in T} p_i}$$

当 $n$ 较大（如 $n=1000$）且 $k$ 较小（如 $k=10000$）时，不能直接枚举子集。需要使用 DP 来统计每个 $\sum p_i$ 对应的系数之和。

设计 DP：$dp[j][s]$ 表示考虑了前 $i$ 个物品，选了 $j$ 个，总 $p$ 和为 $s$ 的方案数（带符号）。

由于 $k$ 可能较大（$k \le 10000$），但 $p_i \le 10^4$，总 $m$ 可能达到 $10^4 \times 1000 = 10^7$，不能直接开数组。

P4707 的核心技巧是利用生成函数和容斥系数的组合意义，将 DP 维度压缩到 $O(nk)$。具体实现较为复杂，这里给出简化的代码框架。

### 5.3 代码框架

```cpp
#include <bits/stdc++.h>
using ll = long long;
const int MOD = 998244353;

// P4707 核心 DP（简化版，仅展示思路）
// 完整实现需要模意义下的组合数和细致的状态转移

ll mod_pow(ll a, ll b, ll mod) {
    ll res = 1;
    while (b) {
        if (b & 1) res = res * a % mod;
        a = a * a % mod;
        b >>= 1;
    }
    return res;
}

// 主函数框架
int main() {
    int n, k, m;
    std::cin >> n >> k >> m;
    
    std::vector<int> p(n);
    for (int i = 0; i < n; ++i) {
        std::cin >> p[i];
    }
    
    // k-th Min-Max 容斥
    // 目标是求第 (n-k+1) 大的期望
    // 公式: E[max_K] = sum_{T} (-1)^{|T|-K} * C(|T|-1, K-1) * m / sum(p in T)
    int K = n - k + 1;
    
    // DP: dp[cnt][sum] = sum of (-1)^{cnt} 对所有大小为 cnt 且 p 和为 sum 的子集
    // 用于后续计算
    // 注意这里仅为框架，P4707 需要用更精妙的 DP 来降维
    
    // 完整实现需要结合组合数和模逆元
    // 这里省略了具体的 DP 降维实现
    
    std::cout << "实现细节请参考洛谷 P4707 题解" << std::endl;
    
    return 0;
}
```

---

## 6. Min-Max 容斥的应用模式

### 6.1 何时使用 Min-Max 容斥？

遇到以下特征的问题时，优先考虑 Min-Max 容斥：

1. 求"所有事件都发生"的期望时刻——对应 $\max$
2. 每个"子事件"的首次发生时刻有简单的期望——对应 $\min$
3. 求第 $k$ 个事件发生的期望时刻——对应 k-th 扩展
4. 问题涉及"覆盖"、"收集"、"激活"等概念

### 6.2 常见公式速查

| 场景 | 最大值公式 | 第 k 大公式 |
|------|-----------|-------------|
| 一般形式 | $\sum (-1)^{|T|-1} \mathbb{E}[\min(T)]$ | $\sum (-1)^{|T|-k} \binom{|T|-1}{k-1} \mathbb{E}[\min(T)]$ |
| 优惠券收集 | $n \sum_{k=1}^n \frac{(-1)^{k-1}}{k} \binom{n}{k}$ | $n \sum_{j=k}^n \frac{(-1)^{j-k}}{j} \binom{j-1}{k-1} \binom{n}{j}$ |
| 通用几何分布 | $\sum (-1)^{|T|-1} \frac{1}{P_T}$ | $\sum (-1)^{|T|-k} \binom{|T|-1}{k-1} \frac{1}{P_T}$ |

其中 $P_T$ 是每次试验"命中 $T$ 中至少一个元素"的概率。

---

## 7. 推荐练习题

1. **洛谷 P3175 - [HAOI2015] 按位或**：Min-Max 容斥 + SOS DP 的经典题。
   - 链接：https://www.luogu.com.cn/problem/P3175

2. **洛谷 P4707 - 重返现世**：k-th Min-Max 容斥 + DP 优化的综合题。
   - 链接：https://www.luogu.com.cn/problem/P4707

---

## 8. 小结

期望 Min-Max 容斥是解决"所有事件都发生"类期望问题的终极武器：

- **基本公式**：$\mathbb{E}[\max(S)] = \sum (-1)^{|T|-1} \mathbb{E}[\min(T)]$
- **k-th 扩展**：$\mathbb{E}[\max_k(S)] = \sum (-1)^{|T|-k} \binom{|T|-1}{k-1} \mathbb{E}[\min(T)]$
- **无需独立性假设**：公式是点态成立的恒等式
- **加速手段**：SOS DP、FWT 用于子集求和；DP 用于按大小或权值分组

Min-Max 容斥的美在于"将难求的最大值的期望转化为易求的最小值的期望之和"。在优惠券收集问题、随机覆盖问题、概率图模型中都有广泛应用。

下一篇文章我们将进入概率与期望板块的最后一篇——**综合应用**，涵盖一些更高阶的视角，如鞅与停时定理。

---

> **系列索引**：本文是 ACM 竞赛数学系列的第 72 篇。
> 上一篇：[#71 马尔可夫链与高斯消元](./71-马尔可夫链与高斯消元.md)
> 下一篇：[#73 概率与期望综合应用](./73-概率与期望综合应用.md)
