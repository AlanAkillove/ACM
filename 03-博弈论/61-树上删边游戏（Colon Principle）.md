# 树上删边游戏（Colon Principle）

> Made by Aki.
> 最后更新于 2026.04.30

## 引言

想象一棵树——不是数据结构中的抽象树，而是一张由节点和边构成的无向图。两个玩家轮流从树上删掉一条边，每次删除都会将树分割成两部分，其中**不包含根节点的部分**会被移除。删掉最后一条边的人获胜。

这就是**树上删边游戏**（Tree Cutting Game），有时也称为**Green Hackenbush**（丛林砍伐游戏）的一种变体——每棵树的枝干就像一条条藤蔓，玩家轮流砍断一根藤蔓，被砍断的枝干（不含根的部分）随之枯萎脱落。

这个游戏有一个非常著名的结论——**Colon Principle**（冒号原理），它告诉我们可以将树上任何分支结构简化为一条路径或一个 Nim 堆。

## 前置知识

- SG 函数与 SG 定理（#56）
- 树的基本概念（根、子树、DFS）
- 异或运算

## 树上删边游戏的基本规则

### 问题定义

给定一棵以 $r$ 为根的树（无向），每次操作可以选择一条边将其删除。删除后，**不包含根的那部分连通分量**会被整体移除（即与根断开的子树全部消失）。最后无法操作的人输（即只剩下根节点时，没有边可删）。

```
     根(r)
    / | \
   A  B  C
  / \    |
 D   E   F
```

如果删除边 $r-A$，则整棵以 $A$ 为根的子树（包括 $A, D, E$）全部被移除，只剩下 $r, B, C, F$。

如果删除边 $A-D$，则节点 $D$ 被移除，剩下的树是 $r-A-E, B, C-F$。

### 问题抽象

这个游戏的特点是：一次操作删除一条边，连带移走一整棵子树。这种「切掉一根枝条，整枝脱落」的形式在很多实际问题中都会出现。

## Colon Principle

### 定理陈述

**Colon Principle（冒号原理）**：
对于树上删边游戏，树中每个节点 $u$ 的 SG 值按下式计算：

$$
SG(u) = \bigoplus_{v \in child(u)} (SG(v) + 1)
$$

其中 $child(u)$ 是 $u$ 的所有子节点。

换句话：**一个节点的 SG 值等于所有子节点「(SG 值 + 1)」的异或**。

特别地，整棵树的 SG 值就是根节点的 SG 值。

### 证明思路

为什么是 $SG(v) + 1$，而不是直接异或 $SG(v)$？

关键原因在于：删除一条连接 $u$ 和 $v$ 的边，会移除以 $v$ 为根的整棵子树。但「删除」本身是一个操作，它等价于：「从以 $v$ 为根的游戏中离开，回到剩余部分游戏」——这个过程类似于 Nim 堆中「取走整堆」的操作。

更深入地，每个子节点 $v$ 对应的实际上是一个**大小为 $SG(v) + 1$ 的 Nim 堆**。之所以 $+1$，是因为从 $u$ 到 $v$ 的这条边本身也是一个「单位」，它和 $v$ 的子树一起构成了一个独立的游戏分支。

让我们通过手算来建立直觉。

### 手算例子

**例子 1：只有一条边**

```
r -- A
```

根 $r$ 有一个子节点 $A$，而 $A$ 没有子节点，$SG(A) = 0$。

根据 Colon Principle：$SG(r) = (SG(A) + 1) = (0 + 1) = 1$。

验证：从根删掉唯一的边 $r-A$，游戏结束，当前玩家获胜。SG 不为 0，与 $SG(r)=1$ 一致。

**例子 2：根连接两个叶子**

```
  r
 / \
A   B
```

$SG(A) = 0$, $SG(B) = 0$

$SG(r) = (0+1) \oplus (0+1) = 1 \oplus 1 = 0$

验证：从根出发，可以删 $r-A$（剩下 $r-B$）或删 $r-B$（剩下 $r-A$）。两种走法都会留下 SG = 1 的局面给对手（因为单独一条边的 SG = 1）。所以所有后继都是必胜态，当前是必败态。$SG(r)=0$ ✓

**例子 3：一条长度为 2 的链**

```
r -- A -- B
```

$B$ 是叶子，$SG(B) = 0$
$A$ 的子节点是 $B$，$SG(A) = (SG(B) + 1) = 1$
$r$ 的子节点是 $A$，$SG(r) = (SG(A) + 1) = 1 + 1 = 2$

验证一下：长度为 2 的链（3 个节点，2 条边），有哪些操作？
- 删 $A-B$：移除 $B$，剩下 $r-A$（一条边，SG=1）
- 删 $r-A$：移除 $A$ 和 $B$，剩下只有 $r$（没有边，SG=0）

后继 SG 值集合 $\{1, 0\}$，$mex(\{0,1\}) = 2$。$SG(r)=2$ ✓

> ❓ Colon Principle 说 $SG(u) = XOR(SG(v)+1)$，这跟直接算 mex 等价吗？
>
> 完全等价！Colon Principle 是树上删边游戏 SG 值的递推公式，它可以从 mex 定义推导出来。它之所以有用，是因为你不需要为每个节点枚举所有可能的删边操作（那太多了），而是直接用子树的 SG 值递推。

**例子 4：更复杂的树**

```
    r
   /|\
  A B C
 /|   |
D E   F
```

先算所有叶子的 SG = 0：
- $D: SG=0, E: SG=0, F: SG=0$

然后向上递推：
- $A: SG = (0+1) \oplus (0+1) = 1 \oplus 1 = 0$
- $B: SG = 0$（叶子）
- $C: SG = (0+1) = 1$

最后 $r$：
- $SG(r) = (0+1) \oplus (0+1) \oplus (1+1) = 1 \oplus 1 \oplus 2 = 0 \oplus 2 = 2$

$SG(r) = 2 \ne 0$，所以先手必胜。

### Colon Principle 的本质：简化到 Nim

Colon Principle 告诉我们，树上的每个分支都可以等效为一个 Nim 堆。

具体地，一棵以 $u$ 为根的子树等效于一个大小为 $SG(u)$ 的 Nim 堆。而 $u$ 的每个子节点 $v$ 对应的分支（包括边 $u-v$ 和以 $v$ 为根的整棵子树）等效于一个大小为 $SG(v) + 1$ 的 Nim 堆。

因此，整个游戏可以化简为一堆 Nim 石子：**根节点有若干子节点，每个子分支是一个独立 Nim 堆，大小为 $SG(v) + 1$，根节点的 SG 值即所有这些 Nim 堆大小的异或**。

### 代码实现

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MAXN = 100005;
vector<int> g[MAXN];

int dfs(int u, int parent) {
    int sg = 0;
    for (int v : g[u]) {
        if (v == parent) continue;
        // SG(u) = XOR of (SG(child) + 1)
        sg ^= (dfs(v, u) + 1);
    }
    return sg;
}

int main() {
    int n;  // 节点数
    cin >> n;
    for (int i = 0; i < n - 1; i++) {
        int u, v;
        cin >> u >> v;
        g[u].push_back(v);
        g[v].push_back(u);
    }
    int root_sg = dfs(1, 0);  // 假设 1 是根
    cout << (root_sg ? "First" : "Second") << " wins!" << endl;
    return 0;
}
```

复杂度：$O(n)$，DFS 一次即可。

## Fusion Principle（融合原理）

### 问题：如果树中有环？

Colon Principle 适用于树（无环图）。但如果树中有环（即图是基环树或更一般的图）呢？

这时就需要 **Fusion Principle**（融合原理）。

**Fusion Principle 定理**：
在一个无向连通图中，如果存在环，可以将环按照以下规则化简而不改变游戏的 SG 值：

- **奇环（奇数长度的环）**：化简为一条边（即环上的所有节点合并为一个节点，并保留一条自环边的效果，等效为一条边连接该节点）
- **偶环（偶数长度的环）**：化简为一个点（即环上所有节点合并为一个节点）

更通俗地说，Fusion Principle 允许我们「收缩」环上的节点：
1. 对于奇环：收缩后的节点形成一个带自环的节点，等效于有一条伸出的边
2. 对于偶环：收缩后的节点就是一个普通节点

### 为什么？

给出完整的证明需要用到图的 SG 值计算方法，这里提供一个直觉：

在树上删边游戏中，环相当于提供了「额外的路径」——如果你删掉环上的一条边，其他环上的边仍然保持连通，不会导致任何子树脱落。只有当环上的边被删到只剩一棵树的连通性时，再删一条边才会产生真正的「脱落」。

经过分析可以证明，偶环上的博弈行为等价于一个节点，奇环上的博弈行为等价于一条边。这个结论被称为 Fusion Principle。

### 使用 Fusion Principle 简化图

```
   A --- B
   |     |
   |     |
   D --- C
    \
     E
```

这是一个外挂了一棵树的四元环（偶环，4 个节点）。

Fusion Principle：偶环 → 一个点。将 $A, B, C, D$ 合并为一个节点 $X$。

```
   X
    \
     E
```

现在图被简化为一棵树（$X-E$），一条边。SG 值 = 1。

验证：原图中，如果从 $A$ 删到 $E$ 的边，会移除 $E$，剩下四元环 $A-B-C-D-A$。偶环等效于一个点，所以删 $A-E$ 后剩下的 SG = 0（一个点没有边可删）。

如果删 $A-B$：剩下路径 $A-D-C-B$，可以继续操作。但偶环 $A-B-C-D$ 实际上确保游戏一定会进行到某个点……

详细验证有点复杂，但结论正确：$SG=1$，先手必胜。

再考虑一个奇环的例子：

```
   A --- B
   |   / |
   | /   |
   C --- D
```

三角形 $A-B-C-A$ 是奇环（3 个节点），$D$ 连接 $C$ 和 $B$ 形成另一个环——可以先处理外部环。

实际上，对于复杂图，反复应用 Fusion Principle 直到图变成树，然后再用 Colon Principle 计算。

> ❓ 如果图中有多个环交织在一起呢？
>
> 你可以反复应用 Fusion Principle：先找到一个环，收缩它；再找下一个环，再收缩……直到图变成树。注意收缩后的图可能产生新的环，继续收缩即可。最终得到的树的 SG 值就是原图的 SG 值。

## 竞赛应用

### 案例 1：AGC 017D

**问题**（AGC017D - Game on Tree）：给定一棵树，两个玩家轮流操作，每次可以选择一个节点 $u$，删除以 $u$ 为根的子树（即删除 $u$ 和它的所有后代——不是删边，而是以节点为单位删子树）。

这与我们讨论的删边游戏不同。但注意：删节点 $u$ 相当于删除了从 $u$ 的父节点到 $u$ 的边，以及 $u$ 的所有后代——这比删边更强（相当于一次删除多条边）。

实际上这个问题可以直接用 SG 分析：对于这种「删除子树」的操作，SG 值的计算方式与 Colon Principle 正好相反——是 $(SG(v) + 1)$ 按位异或？不。

AGC017D 的结论是：$SG(u) = \bigoplus_{v \in child(u)} (SG(v) + 1)$——和 Colon Principle 一模一样！所以原问题直接套用 Colon Principle 的 DFS 计算即可。

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MAXN = 100005;
vector<int> g[MAXN];

int dfs(int u, int p) {
    int sg = 0;
    for (int v : g[u]) {
        if (v == p) continue;
        sg ^= (dfs(v, u) + 1);
    }
    return sg;
}

int main() {
    int n;
    cin >> n;
    for (int i = 0; i < n - 1; i++) {
        int u, v;
        cin >> u >> v;
        g[u].push_back(v);
        g[v].push_back(u);
    }
    cout << (dfs(1, 0) ? "Alice" : "Bob") << endl;
    return 0;
}
```

复杂度 $O(n)$。

### 案例 2：POJ 3710

**问题**（POJ 3710 - "Christmas Game"）：给定若干棵树（可能带环），在树上玩删边游戏。多棵树意味着多个子游戏——整体 SG 值为各棵树 SG 值的异或。

需要用到 Fusion Principle 处理环，再用 Colon Principle 计算每棵树的 SG 值。

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MAXN = 105;
vector<int> g[MAXN];
int vis[MAXN], depth[MAXN];
int sg[MAXN];

// 使用 DFS 处理环（Fusion Principle）
int dfs(int u, int p, int d) {
    vis[u] = 1;
    depth[u] = d;
    int res = 0;
    for (int v : g[u]) {
        if (v == p) continue;
        if (!vis[v]) {
            res ^= (dfs(v, u, d + 1) + 1);
        } else if (depth[v] < depth[u]) {
            // 发现环：v 是 u 的祖先
            int len = depth[u] - depth[v] + 1;
            if (len % 2 == 1) {
                // 奇环 → 等效为一条边
                // 奇环化简为边意味着返回 1
                // 在 Colon Principle 中，(sg+1) 中 sg=0 时得 1
                // 这就是奇环被化简为一条边的效果
                // 但需要合并到异或结果中
                // 由于奇环化简为边后 SG=1（一条边）
                // 与异或运算的交互方式是对环内节点做处理
                // 对于奇环，环等效于一条边：但这条边已经被计入 depth 关系
                res ^= 1;  // 奇环贡献
            }
            // 偶环 → 等效为一个点（无贡献）
        }
    }
    return sg[u] = res;
}
```

> ❓ 代码中的奇环处理为什么是 `res ^= 1`？
>
> 这是将 Fusion Principle 与 Colon Principle 结合的实现。对于奇环，化简为一条边，SG 值为 1。当 DFS 遍历到环时，我们将这个 1 异或到结果中。
>
> 但注意，这个实现是简化版。完整的 POJ 3710 还需要处理多个环重叠等复杂情况，需要更细致的标记和递归处理。建议在理解原理的基础上参考网上完整的题解实现。

### 空间优化与模板

树上删边游戏的 SG 计算只需要一次 DFS，代码非常简洁。最需要注意的点反而是环的处理。建议记住以下模板：

**树版（无环）**：
```cpp
int dfs(int u, int p) {
    int sg = 0;
    for (int v : g[u])
        if (v != p)
            sg ^= (dfs(v, u) + 1);
    return sg;
}
```

**基环树版（有环）**：可借助 Fusion Principle 先化简环为树，再用树版计算。

## 推荐练习题

1. **AGC 017 D - Game on Tree**（树删边 + Colon Principle 直译，必做）
   https://atcoder.jp/contests/agc017/tasks/agc017_d

2. **AGC 017 D - Game on Tree**（树删边 + Colon Principle 直译，必做）
   https://atcoder.jp/contests/agc017/tasks/agc017_d

3. **AGC 017 D - Game on Tree**（树删边的简单应用，Colon Principle 直译）
   https://atcoder.jp/contests/agc017/tasks/agc017_d

4. **Codeforces 1382B - Sequential Nim**（虽然不是树，但与 Colon Principle 的递推思想相通）
   https://codeforces.com/problemset/problem/1382/B

## 小结

树上删边游戏及其 Colon Principle 是博弈论在树形结构上的经典应用：

- **Colon Principle**：$SG(u) = \bigoplus_{v \in child(u)} (SG(v) + 1)$，将树上删边游戏化简为 Nim
- **直觉理解**：每个子分支（边 + 子树）相当于一个大小为 $SG(v)+1$ 的 Nim 堆
- **Fusion Principle**：偶环 → 点，奇环 → 边，用于化简有环图
- **竞赛应用**：AGC017D 是 Colon Principle 的直接运用；POJ3710 是 Fusion Principle 的经典题

这两条原理将复杂的树/图删边问题归约到我们熟悉的 Nim 框架，是组合博弈论中极为优美的一部分内容。

---
> **系列索引**：本文是 ACM 竞赛数学系列的第 61 篇。
> 上一篇：[#60 有向无环图（DAG）上的博弈](./60-有向无环图（DAG）上的博弈.md)
> 下一篇：[#62 Every-SG、Multi-SG与Moore's Nim](./62-Every-SG、Multi-SG与Moore's-Nim.md)
