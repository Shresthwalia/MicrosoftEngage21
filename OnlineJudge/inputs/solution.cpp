#include<bits/stdc++.h>
using namespace std;
#define int long long
void binary(int n){
    if(n==0)return;
    binary(n/2);
    cout<<n%2;
}
int32_t main(){
    int t;
    cin>>t;
    while(t--){
        int n,m;
        cin>>n>>m;
        cout<<n+m;
        if(t>0)
        cout<<' ';
    }
}
