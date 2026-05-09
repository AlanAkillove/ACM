# 有向无环图（DAG）上的博弈

> Made by Aki.
> 最后更新于 2026.04.30

## 引言

回想一下我们在本系列第一篇（#52）中给出的博弈分析通用框架：定义状态、确定转移、标记胜败。这个框架的本质，就是在一张**有向图**上分析每个节点的胜负属性。

但在很多实际问题中，状态转移图并不是一棵树，而是一张更一般的**有向无环图（DAG）**。一个状态可以到达多个状态，而且多个不同的状态可能到达同一个后继状态（共享子状态）。

为什么不直接使用 SG 函数呢？因为 DAG 博弈在竞赛中往往有两类考法：

1. **静态 DAG**：图的结构固定，直接计算每个节点的 SG 值——这就是 SG 函数的直接应用
2. **DAG 上的多棋子博弈**：多个棋子在 DAG 上移动，每个回合必须移动一个棋子——这等于多个子游戏的 SG 值异或
3. **有环图**：如果图中存在环，游戏可能无限进行下去——这时需要引入「平局」（Draw）状态

前两种情况我们已经在前面的文章中覆盖了。本文将重点放在**有环图的处理**——这是竞赛中容易失分的知识点。

## 前置知识

- 必胜态与必败态（#52）
- SG 函数与 SG 定理（#56）
- 有向图、拓扑排序的基本概念
- 队列 BFS

## DAG 上的必胜/必败判定

### 问题定义

**DAG 博弈**：给定一张有向无环图，一个棋子初始在某个节点上。两名玩家轮流沿有向边移动棋子，不能移动者输。

### 判定方法

在 DAG 上，由于没有环，我们可以通过**反向拓扑排序**递推每个节点的胜负状态。

设 $win[u]$ 表示节点 $u$ 的胜负状态（true 为必胜，false 为必败）。

从出度为 0 的节点（终止节点）开始：
- 终止节点：$win[u] = false$（无路可走，必败）
- 其他节点：$win[u] = true$ 当且仅当存在一个后继 $v$ 使得 $win[v] = false$

这就是我们之前反复使用的递推公式，在 DAG 上可以直接用拓扑序计算。

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MAXN = 100005;
vector<int> g[MAXN];    // 原图
vector<int> rg[MAXN];   // 反向图
int outdeg[MAXN];
bool win[MAXN];

void solve(int n) {
    queue<int> q;
    // 初始化
    for (int i = 1; i <= n; i++) {
        outdeg[i] = g[i].size();
        if (outdeg[i] == 0) {
            win[i] = false;  // 终止节点必败
            q.push(i);
        }
    }

    while (!q.empty()) {
        int u = q.front(); q.pop();
        for (int v : rg[u]) {
            if (!win[u] && !win[v]) {
                // 后继 u 是必败态 → 当前 v 是必胜态
                win[v] = true;
                q.push(v);
            } else {
                // 否则减少 v 的出度计数
                outdeg[v]--;
                if (outdeg[v] == 0) {
                    // 所有后继都是必胜态 → 当前是必败态
                    win[v] = false;
                    q.push(v);
                }
            }
        }
    }
}
```

这个算法的本质就是一个**反向 BFS**，从终止状态逆向标记。

### 手算例子

考虑一个简单的 DAG：

```
A → B → C
↓   ↓
D → E
```

其中 $C$ 和 $E$ 是终止节点（出度为 0）。

- $C$：必败
- $B$：后继只有 $C$（必败）→ 必胜
- $E$：必败
- $D$：后继只有 $E$（必败）→ 必胜
- $A$：后继有 $B$（必胜）和 $D$（必胜）→ 所有后继都是必胜，所以 $A$ 是必败

验证：从 $A$ 出发，先手可以走到 $B$ 或 $D$——都是必胜态（轮到对手必胜），所以先手怎么走都是输。确实必败。

### 多个棋子的情况

如果有 $k$ 个棋子分布在 DAG 的不同节点上，每次只能移动一个棋子，不能移动者输——这就是 **DAG 上的 Nim**。

直接使用 SG 定理：计算每个节点的 SG 值，然后所有棋子所在节点 SG 值的异或和为 0 则先手必败，否则先手必胜。

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MAXN = 100005;
vector<int> g[MAXN];
int sg[MAXN];

void compute_sg(int n) {
    // 按拓扑序逆序计算 SG 值
    vector<int> order;  // 拓扑序
    vector<int> indeg(n + 1, 0);
    for (int i = 1; i <= n; i++)
        for (int v : g[i]) indeg[v]++;

    queue<int> q;
    for (int i = 1; i <= n; i++)
        if (indeg[i] == 0) q.push(i);
    while (!q.empty()) {
        int u = q.front(); q.pop();
        order.push_back(u);
        for (int v : g[u])
            if (--indeg[v] == 0) q.push(v);
    }

    // 逆拓扑序计算 SG
    reverse(order.begin(), order.end());
    for (int u : order) {
        set<int> s;
        for (int v : g[u])
            s.insert(sg[v]);
        int mex = 0;
        while (s.count(mex)) mex++;
        sg[u] = mex;
    }
}
```

## 有环图的博弈：Draw 状态的处理

### 问题：环导致无限游戏

当状态转移图中存在环时，游戏可能永远不会结束。例如：

```
A → B → C → A  (形成一个环)
```

两个玩家都在环上移动，谁都不想输——游戏可能无限循环下去。

在竞赛中，通常有三种结果：**先手胜**、**先手负**、**平局**（Draw，即双方都采用最优策略时游戏无限进行）。

### 三值逻辑

我们需要用三个值来表示每个节点的状态：
- `WIN`：当前节点必胜（当前玩家有策略获胜）
- `LOSE`：当前节点必败（无论当前玩家怎么走，对手有策略获胜）
- `DRAW`：平局（双方最优策略下游戏无限进行）

### 判定算法：degree 计数法

**算法思路**：

1. 初始时，所有节点的状态未知
2. 如果一个节点**没有后继**（出度为 0），它是 `LOSE`
3. 如果一个节点**存在一个状态为 `LOSE` 的后继**，它是 `WIN`
4. 如果一个节点的**所有后继都是 `WIN`**，它是 `LOSE`
5. 剩余的状态就是 `DRAW`

这个逻辑跟 DAG 博弈一样，但关键区别在于：有环时可能有些节点永远无法被判定为 WIN 或 LOSE——这些就是 DRAW。

**实现技巧——度计数法**：

对每个节点维护一个 `outdeg` 表示「未被判定为 WIN 的后继数量」。当这个数减到 0 时，说明所有后继都是 WIN，当前节点就是 LOSE。

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MAXN = 100005;
vector<int> g[MAXN];    // 原图
vector<int> rg[MAXN];   // 反向图
int outdeg[MAXN];       // 未判定为 WIN 的后继数
int state[MAXN];        // 0: 未知, 1: WIN, -1: LOSE, 2: DRAW

void solve(int n) {
    queue<int> q;
    for (int i = 1; i <= n; i++) {
        outdeg[i] = g[i].size();
        if (outdeg[i] == 0) {
            state[i] = -1;  // 终止节点 → LOSE
            q.push(i);
        }
    }

    while (!q.empty()) {
        int u = q.front(); q.pop();
        for (int v : rg[u]) {
            if (state[v] != 0) continue;  // 已判定

            if (state[u] == -1) {
                // 后继 u 是 LOSE → 当前 v 是 WIN
                state[v] = 1;
                q.push(v);
            } else {
                // 后继 u 是 WIN → 减少计数
                outdeg[v]--;
                if (outdeg[v] == 0) {
                    // 所有后继都是 WIN → 当前是 LOSE
                    state[v] = -1;
                    q.push(v);
                }
            }
        }
    }

    // 剩余的未知状态都是 DRAW
    for (int i = 1; i <= n; i++) {
        if (state[i] == 0) state[i] = 2;
    }
}
```

### 手算例子：有环图

考虑图：

```
A → B → C
↑   ↓
└─── D
```

边的方向：$A \to B$, $B \to C$, $B \to D$, $D \to A$。

分析：
- $C$：出度为 0 → LOSE
- $B$：后继 $C$（LOSE）→ WIN
- $D$：后继 $A$（未知）→ 暂时无法判断
- $A$：后继 $B$（WIN）→ 但不能马上判断

继续递推：$B$ 被判定为 WIN 后，反向边 $D \to B$ 处理：$D$ 的后继 $B$ 是 WIN，减少 $D$ 的 outdeg。$D$ 的出度只有 1（只连向 $A$），outdeg 现在是 0？不对——$D$ 只连向 $A$，$D$ 的后继是 $A$，不是 $B$。$B$ 被判定为 WIN 不影响 $D$。

等等，让我重新整理。反向边是：
- $C \to B$，$D \to B$
- $A \to D$
- $B \to A$

流程：
1. $C$（LOSE）入队
2. 处理 $C \to B$（反向边）：$B$ 的后继 $C$ 是 LOSE → $B$ 是 WIN，$B$ 入队
3. 处理 $B \to A$（反向边）：$A$ 的后继 $B$ 是 WIN → outdeg[$A$]--。$A$ 的出度为 1，outdeg 变为 0 → 所有后继都是 WIN → $A$ 是 LOSE，$A$ 入队
4. 处理 $B \to D$（反向边）：$D$ 的后继 $B$ 是 WIN → outdeg[$D$]--。$D$ 的出度为 1，outdeg 变为 0 → 所有后继都是 WIN → $D$ 是 LOSE，$D$ 入队

最终：$A$ LOSE, $B$ WIN, $C$ LOSE, $D$ LOSE。没有 DRAW 状态。

验证：从 $A$ 出发，只能到 $B$（WIN），$A$ 的所有后继都是 WIN，所以 $A$ 是 LOSE ✓

> ❓ 这个例子没有 DRAW，那什么情况下会出现 DRAW？
>
> 当图中存在一个环，环上所有节点都无法被判定为 WIN 或 LOSE 时。比如一个简单环 $A \to B \to C \to A$：
> - 所有节点的出度都是 1
> - 没有出度为 0 的节点，队列初始为空
> - 所有节点的 outdeg[.] 初始 = 1，但永远不会有节点入队
> - 最终所有节点都是 DRAW

### 更复杂的 DRAW 例子

```
A → B → C → D
↑   ↓
└─── E
```

设 $D$ 是终止节点（LOSE）。

分析：
- $D$：LOSE
- $C$：后继 $D$（LOSE）→ WIN
- $B$：后继 $E$（未知）和 $C$（WIN）→ outdeg[$B$] 减到 1吗？等等，$B$ 的后继是 $C$（WIN）所以 outdeg[ $B$ ] 减 1（outdeg 初始是 2，现在是 1）。还不能判断。
- $E$：后继 $A$（未知）→ 不能判断
- $A$：后继 $B$（未知）→ 不能判断

此时 $B$ 还有 outdeg = 1（连向 $E$，$E$ 状态未知），$E$ 所有后继未知，$A$ 所有后继未知。

剩下 $A \to B \to E \to A$ 这个环上的节点都无法判定 → 全部 DRAW。

验证：从 $A$ 出发，先手如果走向 $B$（DRAW），游戏可能无限循环；但先手有更好的选择吗？没有其他出边了。所以 $A$ 确实是 DRAW。

从 $E$ 出发，只能到 $A$（DRAW），所以也是 DRAW。

从 $B$ 出发，可以到 $C$（WIN）——先手走到 $C$，则轮到对手在必胜态……所以先手不会这么走！先手会走向 $E$（DRAW），游戏平局。所以 $B$ 也是 DRAW。

> ❓ 但先手走到 $C$ 不是输了吗？为什么要这么走？
>
> 在平局判定中，「最优策略」的意思是：所有玩家**优先争取获胜**，其次争取平局，最差接受失败。所以如果某个节点有到 LOSE 的边，就是 WIN；没有到 LOSE 的边但有到 DRAW 的边，就是 DRAW；只有到 WIN 的边，才是 LOSE。
>
> 在 $B$ 的例子中，$B$ 有两条出边：到 $C$（WIN，即走到那一步就会输）和到 $E$（DRAW，可能平局）。先手选择平局而不是输，所以 $B$ 是 DRAW。

## 有环图博弈的优先级规则

更系统地，我们可以为节点判定定义优先级：

1. 如果存在后继是 LOSE → 当前是 WIN
2. 如果所有后继都是 WIN → 当前是 LOSE
3. 如果存在后继是 DRAW 且没有后继是 LOSE → 当前是 DRAW

这个优先级正是 degree 计数法的核心逻辑。

### 变种：出度为 0 也可能不是 LOSE

有些博弈问题中，如果游戏陷入循环，判定先手输而非平局。这时环上的所有节点都是 WIN（因为先手可以通过拖入循环让对方输）。

这种情况下，算法反而更简单——没有 DRAW 状态，可以直接用拓扑排序递推，剩余的环上节点全部标记为 WIN。

但竞赛中大多数情况会允许 DRAW，所以 degree 计数法是最常用的。

## 案例：Codeforces 917B

**问题**（CF 917B - MADMAX）：两个人在 DAG 上玩一个游戏。有 $n$ 个节点，$m$ 条有向边，每条边上有一个字母（小写）。两个人轮流沿边移动棋子，但**每次移动所用的边的字母不能小于上一次移动的字母**。不能移动者输。

**分析**：
这个游戏跟普通的 DAG 博弈不同，因为每个节点的状态不仅取决于位置，还取决于「上一次移动的字母」。所以状态需要定义为 $(u, last\_char)$，其中 $last\_char$ 是上一步移动的字母，初始时没有上一步（可以视为 $last\_char = 'a' - 1$）。

状态总数 $O(26n)$，可以接受。这是一个 DAG 吗？注意每次字母只能增大或不变，所以边上的字母是递增的——这意味着状态图中不可能有环！所以这是一个 DAG 博弈。

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MAXN = 105;
vector<pair<int, char>> g[MAXN];
int win[MAXN][26];  // -1: 未计算, 0: LOSE, 1: WIN
// win[u][c] 表示当前在 u，上一步字母为 c（0='a'）时的胜负

int dfs(int u, int c) {
    if (win[u][c] != -1) return win[u][c];
    for (auto [v, ch] : g[u]) {
        if (ch - 'a' >= c) {
            if (dfs(v, ch - 'a') == 0) {
                return win[u][c] = 1;
            }
        }
    }
    return win[u][c] = 0;
}

int main() {
    int n, m;
    cin >> n >> m;
    for (int i = 0; i < m; i++) {
        int u, v; char ch;
        cin >> u >> v >> ch;
        g[u].push_back({v, ch});
    }
    memset(win, -1, sizeof(win));

    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++) {
            // 从 i 出发，面对对手在 j（初始没有上一步字符，设为 0）
            // 实际上是：棋子初始在 i，轮到当前玩家走
            // 状态为 (i, 0) 表示在 i，可以走任意边
            cout << (dfs(i, 0) ? 'A' : 'B');
        }
        cout << endl;
    }
    return 0;
}
```

## 推荐练习题

1. **Codeforces 917B - MADMAX**（DAG 博弈 + 带附加状态，必做）
   https://codeforces.com/problemset/problem/917/B

2. **洛谷 P2575 - 高手过招**（DAG 上的多棋子 SG 函数，思路相通）
   https://www.luogu.com.cn/problem/P2575

3. **Codeforces 917B - MADMAX**（DAG 博弈 + 带附加状态，可替代 POJ 2599）
   https://codeforces.com/problemset/problem/917/B

4. **AtCoder ABC 255 G - Constrained Nim**（DAG 上 SG 的优化计算）
   https://atcoder.jp/contests/abc255/tasks/abc255_g

## 小结

DAG 博弈是 SG 函数理论最自然的应用场景，但有环图博弈的处理需要额外的技巧：

- **DAG 博弈**：反向拓扑排序递推，或直接计算 SG 值
- **多棋子 DAG**：每个棋子独立，异或所有棋子所在节点的 SG 值
- **有环图博弈**：需要三值逻辑（WIN/LOSE/DRAW），degree 计数法是标准解法
- **DRAW 的产生条件**：环上的节点无法被判定为 WIN 或 LOSE，且没有通往 LOSE 的路径
- **记忆化搜索**：如果图中有环但环上节点不会影响结果（或者环上节点可以提前处理），记忆化搜索 + 访问标记也可以处理

掌握这些技巧后，大多数竞赛中的图博弈问题都能迎刃而解。

---
> **系列索引**：本文是 ACM 竞赛数学系列的第 60 篇。
> 上一篇：[#59 反Nim与Misère规则](./59-反Nim与Misère规则.md)
> 下一篇：[#61 树上删边游戏（Colon Principle）](./61-树上删边游戏（Colon Principle）.md)
