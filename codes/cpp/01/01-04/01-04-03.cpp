// https://www.spoj.com/problems/PON/
#include<bits/stdc++.h>
using namespace std;
typedef long long ll;

// 模快速幂：计算 a^b mod m（利用 __int128 防溢出）
ll qpow(ll a, ll b, ll m) {
    ll res = 1;
    while (b) {
        if (b & 1) res = (__int128)res * a % m;
        a = (__int128)a * a % m;
        b >>= 1;
    }
    return res;
}

// Miller-Rabin 单轮测试（底数 a）
bool millerRabin(ll n, ll a) {
    ll d = n - 1, r = 0;
    while (!(d & 1)) d >>= 1, r++;    // n-1 = d * 2^r, d 为奇数
    ll x = qpow(a, d, n);
    if (x == 1 || x == n - 1) return true;
    for (int i = 0; i < r - 1; i++) {
        x = (__int128)x * x % n;
        if (x == n - 1) return true;   // 在平方链中遇到 -1，通过
    }
    return false;                      // 始终未遇到 -1，不通过
}

// 确定性 Miller-Rabin：覆盖整个 long long 范围
bool isPrime(ll n) {
    if (n <= 1) return false;
    if (n <= 3) return true;  // 2 和 3 是质数
    if (n % 2 == 0 || n % 3 == 0) return false;
    // long long 范围内的确定性底数集合
    const ll bases[] = {2, 325, 9375, 28178, 450775, 9780504, 1795265022};
    for (ll a : bases) {
        if (a >= n || __gcd(a, n) != 1) continue;  // 过滤无效底数
        if (!millerRabin(n, a)) return false;
    }
    return true;
}

int main(){
    int t; cin >> t;
    while(t--){
        ll n; cin >> n;  // 改为 ll
        if (isPrime(n)) cout << "YES" << endl;
        else cout << "NO" << endl;
    }
    return 0;
}