# 黑盒线性代数（Black Box LA）

> Made by Aki.
> 最后更新于 2026.04.30

---

## 一、引言

假设你有一个 $n \times n$ 的稀疏矩阵 $A$（$n = 10^6$），其中非零元素只有 $m = 10^7$ 个。你想计算 $A^k b$，或者判断 $A$ 是否可逆，或者解一个线性方程组 $Ax = b$。

你**不可能**把 $A$ 显式存成 $n \times n$ 的稠密矩阵——内存根本放不下。但你也不需要这么做。你只需要一个**「黑盒」**（black box）：给定一个向量 $x$，能快速返回 $A \cdot x$ 的值就行。

这就是**黑盒线性代数**（Black Box Linear Algebra）的核心思想：**把矩阵当成一个算子来用，通过矩阵-向量乘法的迭代来提取信息**。

这类方法中最著名的是 **Wiedemann 算法**（或称 Wiedemann-Krylov 方法）。它能在 $O(m n + n^2 \log k)$ 的时间内从 $A^k b$ 中提取信息，而不需要显式构造 $A$ 的稠密形式。

---

## 二、前置知识

- 矩阵乘法的基本概念（[第 74 篇](74-矩阵基本运算与快速幂.md)）
- Krylov 子空间的基本概念
- Berlekamp-Massey 算法（[第 78 篇](78-线性递推与Berlekamp-Massey.md)）
- 线性递推与 Kitamasa（[第 79 篇](79-Kitamasa方法与Bostan-Mori算法.md)）
- 最小多项式的概念

---

## 三、核心推导

### 3.1 问题设定

**黑盒模型**：我们有一个实现黑盒的接口：

```
function apply_A(x):
    return A * x    // 只用到了 A 的稀疏结构或特殊结构
```

甚至可以没有原始的 $A$ 矩阵，只要这个接口能返回正确结果即可。例如，某种 DP 转移虽然可以用矩阵表示，但我们从不需要真正建出矩阵。

**黑盒线性代数的目标**：利用黑盒（仅通过 $A \cdot x$ 运算），完成：
1. 计算 $A^k b$（向量迭代）
2. 求解 $Ax = b$
3. 计算最小多项式
4. 计算行列式或特征值

### 3.2 Krylov 子空间与线性递推

给定矩阵 $A$ 和向量 $b$，**Krylov 子空间**定义为：

$$K_r(A, b) = \text{span}\{b, Ab, A^2b, \dots, A^{r-1}b\}$$

现在考虑序列 $s_i = u^T A^i b$，其中 $u$ 是某个随机向量（通常取随机坐标）。

关键观察：**序列 $\{s_i\}_{i \ge 0}$ 满足一个线性递推——即 $A$ 的最小多项式**。

具体来说，设 $m(x)$ 是 $A$ 的最小多项式，$\deg m = d$。那么对任意向量 $b$ 和 $u$，序列 $\{u^T A^i b\}$ 都满足 $m(x)$ 生成的递推。

解释：$m(A) = 0$，所以 $m(A) \cdot b = 0$。于是对任何 $u$，$u^T m(A) A^i b = 0$，这意味着标量序列 $\{u^T A^i b\}$ 满足以 $m(x)$ 为特征多项式的递推。

### 3.3 Wiedemann 算法

Wiedemann 算法的步骤：

1. **随机投影**：随机选取向量 $u$（从有限域中均匀随机选取）
2. **生成序列**：计算 $s_i = u^T A^i b$，$i = 0, 1, \dots, 2d-1$
3. **BM 求递推**：用 Berlekamp-Massey 算法找出 $s_i$ 满足的最小线性递推——这就是 $A$ 的最小多项式在 $b$ 下的投影
4. **利用递推求 $A^k b$**：有了最小多项式（或特征多项式），可以用 Kitamasa / 线性递推快速求出 $A^k b$

其中的关键步骤 2 每次需要进行一次 $A \cdot (A^i b)$ 的运算（黑盒调用），加上一次向量内积 $u^T (\cdot)$，共 $O(m)$ 时间。

总复杂度：
- 生成序列：$O(d \cdot m)$（$d$ 次黑盒调用，每次 $O(m)$）
- BM 算法：$O(d^2)$
- 求 $A^k b$：$O(d^2 \log k)$（Kitamasa）

如果 $d = n$（退化了），那就是 $O(nm + n^2 \log k)$。

❓ **如果 $d$ 比 $n$ 小很多呢？**

这常常发生！比如 $A$ 的秩比较低，或者 $A$ 有大量相同的特征值。Wiedemann 算法最大的优势就是：**复杂度依赖于最小多项式的次数 $d$，而不是矩阵的大小 $n$**。如果 $d \ll n$，那 Wiedemann 会比高斯消元快得多。

### 3.4 手算例子

考虑稀疏矩阵：

$$A = \begin{pmatrix}
0 & 1 & 0 \\
0 & 0 & 1 \\
1 & 0 & 0
\end{pmatrix}$$

这是一个置换矩阵（3-循环）。$b = (1, 0, 0)^T$。

**Step 1**：随机选取 $u$，假设 $u = (1, 1, 1)^T$。

**Step 2**：计算序列 $s_i = u^T A^i b$。

$A^0 b = (1, 0, 0)^T$，$s_0 = 1$
$A^1 b = (0, 1, 0)^T$，$s_1 = 1$
$A^2 b = (0, 0, 1)^T$，$s_2 = 1$
$A^3 b = (1, 0, 0)^T$，$s_3 = 1$
$A^4 b = (0, 1, 0)^T$，$s_4 = 1$

序列：$1, 1, 1, 1, 1, 1, \dots$。这显然满足递推 $s_i = s_{i-1}$，所以最小多项式次数 $d=1$，特征多项式是 $x-1$？

等等，这不对。$A$ 的实际最小多项式是 $x^3 - 1$（因为 $A^3 = I$）。为什么投影序列只给了 $x-1$？

问题出在 $u$ 的选择上。如果 $u$ 在所有特征向量上的投影在某些方向上为零，序列的递推式可能「降阶」。这就是为什么 WIedemann 算法需要**随机选择** $u$ 的原因——以高概率避免这种退化。

换一个 $u = (1, 2, 0)^T$。

$s_0 = u^T A^0 b = (1, 2, 0) \cdot (1, 0, 0)^T = 1$
$s_1 = u^T A^1 b = (1, 2, 0) \cdot (0, 1, 0)^T = 2$
$s_2 = u^T A^2 b = (1, 2, 0) \cdot (0, 0, 1)^T = 0$
$s_3 = u^T A^3 b = (1, 2, 0) \cdot (1, 0, 0)^T = 1$
$s_4 = u^T A^4 b = (1, 2, 0) \cdot (0, 1, 0)^T = 2$
$s_5 = u^T A^5 b = (1, 2, 0) \cdot (0, 0, 1)^T = 0$

序列：$1, 2, 0, 1, 2, 0, \dots$

显然满足 $s_i = s_{i-3}$（$s_i - s_{i-3} = 0$），三阶递推。这对应 $x^3 - 1$，就是 $A$ 的最小多项式！

❓ **随机选取的 $u$ 什么时候会失败？**

如果 $u$ 在某个特征子空间上的投影是 0，那么这个特征方向的信息就丢失了。但 $u$ 均匀随机选取时，它以高概率在所有不可约因子对应的子空间上都有非零投影。

在有限域 $\mathbb{F}_q$ 上，失败概率约为 $O(d / q)$。如果 $q$ 是较大的素数（比如 $10^9+7$），失败概率可以忽略不计。

### 3.5 黑盒解线性方程组

Wiedemann 算法也可以用来解 $Ax = b$。

思路：
1. 找到 $A$ 的最小多项式 $m(x) = \sum_{i=0}^d c_i x^i$（$c_d = 1$）
2. 由于 $m(A) = 0$，有 $\sum_{i=0}^d c_i A^i = O$
3. 把两边作用在某个向量上…

但这里需要更精细的分析。更常用的方法是用**块 Wiedemann 算法**或**共轭梯度法**（CG，当 $A$ 对称正定时）。

块 Wiedemann 算法同时使用多个投影向量 $u_1, \dots, u_s$，生成矩阵序列而不是标量序列，然后用矩阵版本的 BM 算法处理。它在处理病态矩阵时更稳定。

### 3.6 黑盒计算 $A^k b$

这是 Wiedemann 系列算法中最直接的应用。

算法步骤：
1. 计算序列 $s_i = u^T A^i b$ 共 $2d$ 项（$d$ 是 $A$ 的最小多项式次数）
2. 用 BM 求递推系数
3. 用 Kitamasa 方法求 $s_k$（需要递推关系求第 $k$ 个标量值，但这给出的是 $u^T A^k b$，不是 $A^k b$）

等一下——我们需要的是 $A^k b$ 这个**向量**，而不是它的投影 $u^T A^k b$。

为了得到向量 $A^k b$，我们需要多运行几次 Wiedemann，或者使用更复杂的技术。一种方法是对每个标准基向量 $e_j$ 运行一次 Wiedemann 来得到 $(A^k b)_j$，但那样太慢了。

更好的做法：**在 BM 找到递推式后，直接对向量序列用递推关系**。

如果 $A$ 的最小多项式是 $m(x) = x^d - c_1 x^{d-1} - \cdots - c_d$，那么对任何向量 $v$，有 $A^d v = c_1 A^{d-1} v + \cdots + c_d v$。

现在，要计算 $A^k b$：
1. 先暴力算出 $b, Ab, A^2b, \dots, A^{d-1}b$（$d$ 次黑盒调用）
2. 然后用递推关系在 $O(d^2 \log k)$ 内（或用 Kitamasa 的 $O(d^2 \log k)$）求出 $A^k b$ 在基底 $\{b, Ab, \dots, A^{d-1}b\}$ 下的组合系数
3. 把基底向量按系数组合

```python
# 伪代码
# 输入：黑盒函数 mul_A(v) = A*v，向量 b，整数 k
# 输出：A^k * b

# 第 1 步：生成序列
d = ... # 最小多项式次数的上界（通常取 n）
seq = []
v = b
for i in range(2*d):
    seq.append(inner_prod(u, v))
    v = mul_A(v)

# 第 2 步：BM 求最小多项式
C = berlekamp_massey(seq)  # C[0]=1, 递推系数

# 第 3 步：暴力计算基向量
basis = [b]
for i in range(1, d):
    basis.append(mul_A(basis[-1]))
# 现在 basis[i] = A^i * b

# 第 4 步：用 Kitamasa 或递推求 A^k b 的系数
coeff = get_coefficients(C, k, d)  # 返回 coeff[0..d-1]，使得 A^k b = sum coeff[i] * basis[i]

# 第 5 步：组合
result = zero_vector(n)
for i in range(d):
    result = result + coeff[i] * basis[i]
return result
```

### 3.7 黑盒的应用范围

Wiedemann 算法不仅限于求 $A^k b$，还可以：

1. **求最小多项式**：序列的 BM 结果就是最小多项式
2. **求特征多项式**：可以用更复杂的 Wiedemann 变体
3. **求行列式**：从特征多项式提取常数项
4. **解线性方程组**：
   - 先求最小多项式 $m(x)$
   - 令 $m(x) = x \cdot q(x) + m(0)$
   - 如果 $A$ 可逆（$m(0) \neq 0$），则 $A^{-1} = -\frac{1}{m(0)} q(A)$
   - 那么 $x = A^{-1}b = -\frac{1}{m(0)} q(A) b$

这比直接高斯消元更通用，尤其适合**超大稀疏问题**。

---

## 四、代码实现

### 4.1 Wiedemann 算法：求 $A^k b$

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
using poly = vector<ll>;
using matrix = vector<vector<ll>>;

const ll MOD = 1'000'000'007;

// 黑盒接口：计算 A * x
// 实际使用时根据问题实现
vector<ll> mul_A(const vector<ll>& x) {
    // 示例：3-cycle 置换矩阵
    int n = x.size();
    vector<ll> res(n);
    for (int i = 0; i < n; i++)
        res[(i + 1) % n] = x[i];
    return res;
}

ll inner_prod(const vector<ll>& a, const vector<ll>& b) {
    ll s = 0;
    for (int i = 0; i < (int)a.size(); i++)
        s = (s + a[i] * b[i]) % MOD;
    return s;
}

// Berlekamp-Massey
poly berlekamp_massey(const vector<ll>& s) {
    poly C(1, 1), B(1, 1);
    ll b = 1;
    int L = 0, m = 1;

    auto mod_pow = [](ll a, ll e) {
        ll r = 1; while (e) { if (e & 1) r = r * a % MOD;
            a = a * a % MOD; e >>= 1; } return r; };

    for (int i = 0; i < (int)s.size(); i++) {
        ll d = s[i];
        for (int j = 1; j <= L; j++)
            d = (d + C[j] * s[i - j]) % MOD;
        if (d == 0) { m++; continue; }
        poly T = C;
        ll coef = d * mod_pow(b, MOD - 2) % MOD;
        if (C.size() < B.size() + m) C.resize(B.size() + m, 0);
        for (int j = 0; j < (int)B.size(); j++)
            C[j + m] = (C[j + m] - coef * B[j] % MOD + MOD) % MOD;
        if (2 * L <= i) {
            L = i + 1 - L;
            B = T;
            b = d;
            m = 1;
        } else m++;
    }
    return C;
}

// 多项式乘法与模幂（Kitamasa 的一部分）
poly poly_mul(const poly& a, const poly& b) {
    poly res(a.size() + b.size() - 1, 0);
    for (int i = 0; i < (int)a.size(); i++)
        for (int j = 0; j < (int)b.size(); j++)
            res[i + j] = (res[i + j] + a[i] * b[j]) % MOD;
    return res;
}

poly poly_mod(poly a, const poly& p) {
    int k = p.size() - 1;
    for (int i = (int)a.size() - 1; i >= k; i--) {
        if (a[i] == 0) continue;
        for (int j = 0; j <= k; j++)
            a[i - k + j] = (a[i - k + j] - a[i] * p[j]) % MOD;
    }
    a.resize(k);
    for (auto& x : a) if (x < 0) x += MOD;
    return a;
}

// Wiedemann 算法核心：求 A^k * b
vector<ll> wiedemann(const vector<ll>& b, ll k, int n) {
    // Step 1: 随机选取 u
    vector<ll> u(n);
    mt19937 rng(chrono::steady_clock::now().time_since_epoch().count());
    for (int i = 0; i < n; i++)
        u[i] = uniform_int_distribution<ll>(1, MOD-1)(rng);

    // Step 2: 生成标量序列
    int d_est = min(n, 50); // 实际中应该根据问题调整，或者自适应
    vector<ll> seq(2 * d_est);
    vector<ll> v = b;
    for (int i = 0; i < 2 * d_est; i++) {
        seq[i] = inner_prod(u, v);
        v = mul_A(v);
    }

    // Step 3: BM 求最小多项式
    poly C = berlekamp_massey(seq);
    int d = (int)C.size() - 1;
    if (d <= 0) d = 1;

    // 如果估计的阶数不够，需要重新计算更多项
    // （这里简化处理，实际需要自适应）

    // Step 4: 暴力计算基向量 A^i * b, i=0..d-1
    vector<vector<ll>> basis(d);
    basis[0] = b;
    for (int i = 1; i < d; i++)
        basis[i] = mul_A(basis[i - 1]);

    // Step 5: 用 Kitamasa 求系数（多项式模幂）
    // 特征多项式: P(x) = x^d - C[1]x^{d-1} - ... - C[d]
    poly p(d + 1, 0);
    p[0] = 1;
    for (int i = 1; i <= d; i++)
        p[i] = (-C[i] % MOD + MOD) % MOD;

    // 计算 x^k mod p(x)
    poly res = {1}, base = {0, 1};
    ll exp = k;
    while (exp) {
        if (exp & 1) {
            res = poly_mul(res, base);
            res = poly_mod(res, p);
        }
        base = poly_mul(base, base);
        base = poly_mod(base, p);
        exp >>= 1;
    }

    // Step 6: 组合基向量
    vector<ll> ans(n, 0);
    for (int i = 0; i < d; i++) {
        for (int j = 0; j < n; j++)
            ans[j] = (ans[j] + res[i] * basis[i][j]) % MOD;
    }
    return ans;
}

// 使用示例
int main() {
    int n = 3;
    vector<ll> b = {1, 0, 0};
    ll k = 10;
    vector<ll> res = wiedemann(b, k, n);
    // 3-cycle: A^10 = A^(10 mod 3) = A^1
    // A^1 * (1,0,0) = (0,1,0)
    cout << "A^10 * b = (" << res[0] << ", " << res[1] << ", " << res[2] << ")\n";
    return 0;
}
```

### 4.2 黑盒解线性方程组

```cpp
// 用 Wiedemann 解 Ax = b（假设 A 可逆）
vector<ll> wiedemann_solve(const vector<ll>& b, int n) {
    // 1. 求 A 的最小多项式
    vector<ll> u(n);
    mt19937 rng(chrono::steady_clock::now().time_since_epoch().count());
    for (int i = 0; i < n; i++)
        u[i] = uniform_int_distribution<ll>(1, MOD-1)(rng);

    int d_est = min(n, 100);
    vector<ll> seq(2 * d_est);
    vector<ll> v = b;
    for (int i = 0; i < 2 * d_est; i++) {
        seq[i] = inner_prod(u, v);
        v = mul_A(v);
    }

    poly C = berlekamp_massey(seq);
    int d = C.size() - 1;

    // m(x) = x^d - c1 x^{d-1} - ... - cd = 0
    // A^(-1) = (1/cd) * (A^{d-1} - c1 A^{d-2} - ... - c_{d-1} I)
    // x = A^(-1) * b = (1/cd) * (A^{d-1}b - c1 A^{d-2}b - ... - c_{d-1} b)

    ll cd = (-C[d] % MOD + MOD) % MOD; // m(x) 的常数项
    if (cd == 0) {
        // A 不可逆
        return {};
    }

    // 计算 A^i * b, i=0..d-1
    vector<vector<ll>> Ab(d);
    Ab[0] = b;
    for (int i = 1; i < d; i++)
        Ab[i] = mul_A(Ab[i-1]);

    // x = (1/cd) * (A^{d-1}b - c1*A^{d-2}b - ... - c_{d-1}*b)
    vector<ll> x(n, 0);
    for (int i = 1; i <= d; i++) {
        ll coeff = (-C[i] % MOD + MOD) % MOD;
        if (i == d) coeff = 1; // 最高次项系数是 1
        for (int j = 0; j < n; j++)
            x[j] = (x[j] + coeff * Ab[d - i][j]) % MOD;
    }

    ll inv_cd = 1;
    // 计算 cd 的逆元
    {
        ll a = cd, e = MOD - 2, r = 1;
        while (e) { if (e & 1) r = r * a % MOD; a = a * a % MOD; e >>= 1; }
        inv_cd = r;
    }
    for (int j = 0; j < n; j++)
        x[j] = x[j] * inv_cd % MOD;

    return x;
}
```

---

## 五、复杂度分析

### 5.1 Wiedemann 算法

| 步骤 | 复杂度 | 说明 |
|------|-------|------|
| 生成序列 | $O(d \cdot m)$ | $d$ 次黑盒调用 + 向量内积 |
| BM 求递推 | $O(d^2)$ | $d$ 是递推阶数 |
| Kitamasa 求系数 | $O(d^2 \log k)$ | 多项式模幂 |
| 组合基向量 | $O(d \cdot n)$ | $d$ 个 $n$ 维向量的线性组合 |
| **总计** | $O(m d + d^2 \log k + d n)$ | 通常 $d \le n$ |

### 5.2 与高斯消元的对比

| 方法 | 复杂度 | 内存 | 适用场景 |
|------|-------|------|---------|
| 高斯消元 | $O(n^3)$ | $O(n^2)$ | $n \le 2000$ 稠密矩阵 |
| Wiedemann | $O(m n + n^2 \log k)$ | $O(m)$ | 大型稀疏矩阵 |
| 共轭梯度（CG） | $O(m \cdot \kappa \cdot \log(1/\epsilon))$ | $O(m)$ | 对称正定矩阵 |

$\kappa$ 是条件数，$m$ 是稀疏矩阵的非零元素个数。

---

## 六、应用场景

1. **超大稀疏矩阵的幂**：图上的随机游走 $A^k e_i$，适合 Wiedemann
2. **不需要显式构造矩阵**：直接提供黑盒函数即可
3. **最小多项式与特征值**：稀疏矩阵的谱信息提取
4. **配合概率方法**：随机化算法的高概率正确性

**推荐练习题**：

- [Codeforces 1096G Lucky Tickets](https://codeforces.com/problemset/problem/1096/G) — NTT 优化多项式幂运算，黑盒迭代思想
- [洛谷 P4719 【模板】矩阵树定理](https://www.luogu.com.cn/problem/P4719) — 可以用稀疏矩阵技术求解

---

## 七、小结

黑盒线性代数的核心思想很简单：**不存储矩阵，只提供矩阵-向量乘法接口**。

Wiedemann 算法通过将问题投影到标量序列上，利用 Krylov 子空间中序列满足线性递推的性质，结合 BM 算法和 Kitamasa，实现了高效的 $A^k b$ 计算和方程组求解。

| 概念 | 用途 |
|------|------|
| Krylov 子空间 | 由 $b, Ab, A^2b, \dots$ 张成 |
| 最小多项式 | 序列满足的线性递推 |
| 随机投影 | 避免退化的高概率方法 |
| BM 算法 | 从投影序列恢复递推 |

下一篇我们将对**线性代数综合应用**做一个全景式的总结，涉及邻接矩阵幂、图上随机游走和线性规划等内容。

---

> **系列索引**：本文是 ACM 竞赛数学系列的第 82 篇。
> 上一篇：[#81 循环矩阵与Toeplitz矩阵](81-循环矩阵与Toeplitz矩阵.md)
> 下一篇：[#83 线性代数综合应用](83-线性代数综合应用.md)
