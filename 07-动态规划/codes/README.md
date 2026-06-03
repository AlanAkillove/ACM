# 动态规划系列 - 参考代码

本目录包含动态规划系列教程中所有例题和练习题的参考代码。

## 目录结构

```
codes/
├── 01-DP入门与记忆化搜索/
├── 02-线性DP基础/
├── 03-背包问题（一）/
├── 04-背包问题（二）/
├── 05-区间DP/
├── 06-树形DP/
├── 07-数位DP/
├── 08-状压DP/
├── 09-DP优化（一）/
├── 10-概率与期望DP/
└── 11-DP综合应用/
```

## 命名规则

- 每个目录对应教程的一篇
- 文件名格式：`题号-题名.cpp`（如 `70-climbing-stairs.cpp`）
- 如果是洛谷题目，格式为 `P题号-题名.cpp`（如 `P1048-采药.cpp`）

## 代码规范

1. **语言**：C++17
2. **编码**：UTF-8
3. **注释**：关键步骤添加中文注释
4. **头文件**：使用 `#include <bits/stdc++.h>`
5. **命名空间**：使用 `using namespace std;`

## 示例代码

### 01-DP入门与记忆化搜索

- [70-climbing-stairs.cpp](01-DP入门与记忆化搜索/70-climbing-stairs.cpp) - LeetCode 70. 爬楼梯
- [P1216-数字三角形.cpp](01-DP入门与记忆化搜索/P1216-数字三角形.cpp) - 洛谷 P1216 数字三角形

### 02-线性DP基础

- [300-longest-increasing-subsequence.cpp](02-线性DP基础/300-longest-increasing-subsequence.cpp) - LeetCode 300. 最长递增子序列
- [1143-longest-common-subsequence.cpp](02-线性DP基础/1143-longest-common-subsequence.cpp) - LeetCode 1143. 最长公共子序列
- [72-edit-distance.cpp](02-线性DP基础/72-edit-distance.cpp) - LeetCode 72. 编辑距离

### 03-背包问题（一）

- [P1048-采药.cpp](03-背包问题（一）/P1048-采药.cpp) - 洛谷 P1048 采药
- [322-coin-change.cpp](03-背包问题（一）/322-coin-change.cpp) - LeetCode 322. 零钱兑换

### 04-背包问题（二）

- [P1757-通天之分组背包.cpp](04-背包问题（二）/P1757-通天之分组背包.cpp) - 洛谷 P1757 通天之分组背包
- [494-target-sum.cpp](04-背包问题（二）/494-target-sum.cpp) - LeetCode 494. 目标和

### 05-区间DP

- [P1880-石子合并.cpp](05-区间DP/P1880-石子合并.cpp) - 洛谷 P1880 石子合并
- [312-burst-balloons.cpp](05-区间DP/312-burst-balloons.cpp) - LeetCode 312. 戳气球

### 06-树形DP

- [P1352-没有上司的舞会.cpp](06-树形DP/P1352-没有上司的舞会.cpp) - 洛谷 P1352 没有上司的舞会
- [687-longest-univalue-path.cpp](06-树形DP/687-longest-univalue-path.cpp) - LeetCode 687. 最长同值路径

### 07-数位DP

- [P2657-数字游戏.cpp](07-数位DP/P2657-数字游戏.cpp) - 洛谷 P2657 数字游戏
- [233-number-of-digit-one.cpp](07-数位DP/233-number-of-digit-one.cpp) - LeetCode 233. 数字 1 的个数

### 08-状压DP

- [P1896-互不侵犯.cpp](08-状压DP/P1896-互不侵犯.cpp) - 洛谷 P1896 互不侵犯
- [698-partition-to-k-equal-sum-subsets.cpp](08-状压DP/698-partition-to-k-equal-sum-subsets.cpp) - LeetCode 698. 划分为 k 个相等的子集

### 09-DP优化（一）

- [P1886-滑动窗口.cpp](09-DP优化（一）/P1886-滑动窗口.cpp) - 洛谷 P1886 滑动窗口
- [P3195-玩具装箱.cpp](09-DP优化（一）/P3195-玩具装箱.cpp) - 洛谷 P3195 玩具装箱

### 10-概率与期望DP

- [P4316-绿豆蛙的归宿.cpp](10-概率与期望DP/P4316-绿豆蛙的归宿.cpp) - 洛谷 P4316 绿豆蛙的归宿
- [837-new-21-game.cpp](10-概率与期望DP/837-new-21-game.cpp) - LeetCode 837. 新 21 点

### 11-DP综合应用

- [139-word-break.cpp](11-DP综合应用/139-word-break.cpp) - LeetCode 139. 单词拆分
- [115-distinct-subsequences.cpp](11-DP综合应用/115-distinct-subsequences.cpp) - LeetCode 115. 不同的子序列（本文例题）

---

> Made with ❤️ by CQUE-ACMers · 最后更新于 2026.06.03