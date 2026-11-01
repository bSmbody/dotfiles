import numpy as np
rng=np.random.default_rng(0)
d,B,nb=128,128,16; N=B*nb
def kv():
    ch=np.exp(rng.normal(0,1.0,d)); ch[rng.choice(d,4,replace=False)]*=8   # outlier channels in K
    K=rng.normal(0,1,(N,d))*ch + rng.normal(0,0.5,d)*ch
    V=rng.normal(0,1,(N,d))
    return K,V
def grid_perchannel(X,bits):   # KIVI-style: K per-channel within each block
    lo=np.empty_like(X); de=np.empty_like(X)
    for b in range(nb):
        s=slice(b*B,(b+1)*B); mn=X[s].min(0); mx=X[s].max(0)
        lo[s]=mn; de[s]=(mx-mn)/(2**bits-1)+1e-12
    return lo,de
def grid_pertoken(X,bits):     # V per-token
    mn=X.min(1,keepdims=True); mx=X.max(1,keepdims=True)
    return np.broadcast_to(mn,X.shape).copy(), np.broadcast_to((mx-mn)/(2**bits-1)+1e-12,X.shape).copy()
def q_rtn(X,lo,de): return lo+np.round((X-lo)/de)*de
def q_sr(X,lo,de):
    y=(X-lo)/de; f=y-np.floor(y); return lo+(np.floor(y)+(rng.random(X.shape)<f))*de
def q_sr_coupledK(X,lo,de):    # shared U per (block, coordinate)
    y=(X-lo)/de; fl=np.floor(y); f=y-fl; out=np.empty_like(X)
    for b in range(nb):
        s=slice(b*B,(b+1)*B); U=rng.random(d); out[s]=fl[s]+(U[None,:]<f[s])
    return lo+out*de
def q_dep_V(X,lo,de):          # weighted dependent rounding within block, per coordinate (preserves sum of dequantized values)
    y=(X-lo)/de; fl=np.floor(y); x=y-fl
    for b in range(nb):
        for c in range(d):
            idx=list(range(b*B,(b+1)*B)); cur=None
            for j in idx:
                if cur is None: cur=j; continue
                i=cur; Di,Dj=de[i,c],de[j,c]; xi,xj=x[i,c],x[j,c]
                a=min(Di*(1-xi),Dj*xj); bb=min(Di*xi,Dj*(1-xj))
                if a+bb<=0: cur=j; continue
                t=a if rng.random()<bb/(a+bb) else -bb
                x[i,c]=xi+t/Di; x[j,c]=xj-t/Dj
                if abs(x[i,c]-round(x[i,c]))<1e-9: x[i,c]=round(x[i,c]); cur=j
                else: x[j,c]=round(x[j,c])
            if cur is not None and 0<x[cur,c]<1: x[cur,c]=float(rng.random()<x[cur,c])
    return lo+(fl+np.round(x))*de
def softmax(z): z=z-z.max(); e=np.exp(z); return e/e.sum()
def run(trials=20):
    res={}
    for temp in [0.3,1.0,3.0]:            # larger temp -> sharper attention
        acc={k:[] for k in ['K_rtn','K_sr','K_coup','V_rtn','V_sr','V_dep','V1_rtn','V1_sr','V1_dep','ent']}
        for t in range(trials):
            K,V=kv(); q=rng.normal(0,1,d)/np.sqrt(d)
            z=K@q; z=z/z.std()*temp*3; scale=(temp*3)/(K@q).std()
            p=softmax(z)
            acc['ent'].append(-(p*np.log(p+1e-30)).sum())
            lo,de=grid_perchannel(K,2)
            for name,fn in [('K_rtn',q_rtn),('K_sr',q_sr),('K_coup',q_sr_coupledK)]:
                ph=softmax((fn(K,lo,de)@q)*scale); acc[name].append((p*np.log(p/ph)).sum())
            o=p@V
            for bits,pre in [(2,'V'),(1,'V1')]:
                lo2,de2=grid_pertoken(V,bits)
                for name,fn in [('rtn',q_rtn),('sr',q_sr),('dep',q_dep_V)]:
                    e=p@fn(V,lo2,de2)-o; acc[f'{pre}_{name}'].append((e**2).sum()/(o**2).sum())
        res[temp]={k:np.mean(v) for k,v in acc.items()}
    return res
r=run(8)
for temp,v in r.items():
    print(f"attention sharpness={temp}  entropy={v['ent']:.2f} nats (uniform={np.log(N):.2f})")
    print(f"  K2 attention KL     RTN={v['K_rtn']:.4f}  indepSR={v['K_sr']:.4f}  coupledSR={v['K_coup']:.4f}")
    print(f"  V2 rel. readout err RTN={v['V_rtn']:.4f}  indepSR={v['V_sr']:.4f}  depRound={v['V_dep']:.4f}")
    print(f"  V1 rel. readout err RTN={v['V1_rtn']:.4f}  indepSR={v['V1_sr']:.4f}  depRound={v['V1_dep']:.4f}")
