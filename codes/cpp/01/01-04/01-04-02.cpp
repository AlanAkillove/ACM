// https://www.luogu.com.cn/problem/B2138
#include <bits/stdc++.h>
using namespace std;

const int MAXN = 5005;
int maxp[MAXN];  

void init() {
    memset(maxp, 0, sizeof(maxp));
    for (int i = 2; i < MAXN; ++i) {
        if (maxp[i] == 0) { 
            maxp[i] = i;
            for (int j = i * 2; j < MAXN; j += i) {
                maxp[j] = i; 
            }
        }
    }
}

int main() {
    init();
    int m, n;
    cin >> m >> n;
    for (int i = m; i <= n; ++i) {
        if (i > m) cout << ",";
        cout << maxp[i];
    }
    return 0;
}