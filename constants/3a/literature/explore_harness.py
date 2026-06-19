from fractions import Fraction
from math import log
import itertools

def counts(A, base, d, T):
    A=sorted(set(A))
    # max(U): greedy fill highest digits with largest a<=rem
    rem=T; m=0
    for i in range(d-1,-1,-1):
        a=max(x for x in A if x<=rem); m+=a*(base**i); rem-=a
    # sum count via bitset DP
    Y=sorted({a+b for a in A for b in A})
    P={y:tuple(a for a in A if y-a in A) for y in Y}
    mask=(1<<(T+1))-1
    cache={}
    def shift(bitset,y):
        k=(bitset,y)
        if k in cache: return cache[k]
        out=0
        for p in P[y]: out|=bitset<<p
        out&=mask; cache[k]=out; return out
    states={0:{1:1}}
    for _ in range(d):
        ns={}
        for ty,bs in states.items():
            for bitset,cnt in bs.items():
                for y in Y:
                    nty=ty+y
                    if nty<=2*T:
                        nb=shift(bitset,y)
                        if nb:
                            b=ns.setdefault(nty,{}); b[nb]=b.get(nb,0)+cnt
        states=ns
    full=(1<<(T+1))-1; S=0
    for ty,bs in states.items():
        lower=max(0,ty-T)
        feas=full^((1<<lower)-1) if lower else full
        for bitset,cnt in bs.items():
            if bitset&feas: S+=cnt
    # diff count via (left,right) DP
    Delta=sorted({a-b for a in A for b in A})
    feats=[]
    for delta in Delta:
        q=min(b for b in A if b+delta in A); feats.append((q,q+delta))
    st={(0,0):1}
    for _ in range(d):
        ns={}
        for (l,r),cnt in st.items():
            for x,y in feats:
                nl=l+x; nr=r+y
                if nl<=T and nr<=T:
                    k=(nl,nr); ns[k]=ns.get(k,0)+cnt
        st=ns
    D=sum(st.values())
    theta=1+log(D/S)/log(2*m+1)
    return S,D,m,theta

if __name__=="__main__":
    import sys
    # record reproduce baseline with small d for speed sanity
    A=[0,2,3,4,5,6,7,8,9,10]
    # small test
    S,D,m,th=counts(A,21,12,22)
    print("test d=12 T=22:",th)
