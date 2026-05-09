# Min-Max 容斥

> Made by Aki.
> 最后更新于 2026.04.30

Min-Max 容斥将「集合的最大值」表示为「子集的最小值」的线性组合——或者说，将极值转化为交集。这一技巧在概率期望题中尤其常见。

---

## 一、核心公式

> 对于有限实数集 $\{x_1, x_2, \dots, x_n\}$：
>
> $$
> \boxed{\max(S) = \sum_{\emptyset \neq T \subseteq S} (-1)^{|T|-1} \min(T)}
> $$
>
> $$
> \boxed{\min(S) = \sum_{\emptyset \neq T \subseteq S} (-1)^{|T|-1} \max(T)}
> $$

两个公式对称——$\max$ 和 $\min$ 互换，符号保持不变。

**推导思路**：将 $x_i$ 升序排列为 $y_1 \le y_2 \le \cdots \le y_n$。$\max(S) = y_n$。右边 $\sum (-1)^{|T|-1} \min(T)$ 的贡献来自包含 $y_n$ 的那些子集。用组合恒等式验证：所有包含 $y_n$ 且最小值为 $y_k$ 的子集，其符号和恰好使 $y_n$ 保留而其余 $y_k$ 消去。

---

## 二、期望版本——竞赛中的主力应用

最强大的推广是它将 $\max$ 和 $\min$ 替换为**随机变量的期望**：

$$
\boxed{\mathbb{E}[\max(S)] = \sum_{\emptyset \neq T \subseteq S} (-1)^{|T|-1} \mathbb{E}[\min(T)]}
$$

**为什么这个版本极其有用？** 在很多概率题中，$\mathbb{E}[\min(T)]$（集合中第一个发生的事件的期望时间）很容易算——如果每个事件 $i$ 独立以概率 $p_i$ 发生，则 $\min(T)$ 的发生时间服从几何分布，期望为 $1 / \sum_{i \in T} p_i$。而 $\mathbb{E}[\max(T)]$（所有事件都发生至少一次的期望时间）非常难直接求。

Min-Max 容斥将「最后一个」转化为「若干个第一个」的线性组合。

---

## 三、例题

**例 3.1**（HAOI2015 按位或）：你每秒随机获得 $0$ 到 $2^n-1$ 之间的一个数（每位独立、以概率 $p_i$ 为 $1$）。求所有位都至少出现过一次 $1$ 的期望时间。

设 $t_i$ 为第 $i$ 位首次出现 $1$ 的时间。所求即 $\mathbb{E}[\max_i t_i]$。

对子集 $T$，$\mathbb{E}[\min_{i \in T} t_i]$ 是 $T$ 中任意位首次出现 $1$ 的期望时间——这是几何分布，期望为 $1 / \sum_{i \in T} p_i$。套用 Min-Max 容斥：

$$
\mathbb{E}[\max_i t_i] = \sum_{\emptyset \neq T} (-1)^{|T|-1} \frac{1}{\sum_{i \in T} p_i}
$$

$p_i$ 可以从输入的 $2^n$ 个概率中用 SOS DP 在 $O(n2^n)$ 内求出。总复杂度 $O(n2^n)$。

---

## 四、扩展：第 $k$ 大

Min-Max 容斥可以推广到第 $k$ 大的元素：

$$
\text{kth}\max(S) = \sum_{\emptyset \neq T \subseteq S} (-1)^{|T|-k} \binom{|T|-1}{k-1} \min(T)
$$

这个版本在 [洛谷 P4707 重返现世](https://www.luogu.com.cn/problem/P4707) 中出现。

---

## 五、推荐练习题

- [洛谷 P3175](https://www.luogu.com.cn/problem/P3175) — [HAOI2015] 按位或。Min-Max 容斥 + 期望 + SOS DP
- [洛谷 P4707](https://www.luogu.com.cn/problem/P4707) — 重返现世。第 $k$ 大 Min-Max 容斥
- [洛谷 P5643](https://www.luogu.com.cn/problem/P5643) — 随机游走。Min-Max + 高斯消元

---

> **系列索引**：本文是 ACM 竞赛数学系列的第 46 篇。
> 上一篇：[#45 子集反演](../02-组合数学/45-子集反演.md)
> 下一篇：[#47 Prufer 序列与 Cayley 定理](../02-组合数学/47-Prufer序列与Cayley定理.md)
