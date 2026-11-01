import numpy as np, sys
src=open(sys.argv[1]).read().split('r=run(8)')[0]; ns={}; exec(src,ns); rng=ns['rng']; d=ns['d']
Hq,_=np.linalg.qr(rng.normal(size=(d,d)))   # random orthogonal rotation (stand-in for Hadamard)
for bits in [2,3]:
  for temp in [0.3,1.0,3.0]:
    kl={'rtn':[],'sr':[],'coup':[]}
    for t in range(60):
        K,V=ns['kv'](); q=rng.normal(0,1,d)/np.sqrt(d)
        z0=K@q; scale=(temp*3)/z0.std(); p=ns['softmax'](z0*scale)
        Kr=K@Hq; qr=q@Hq                  # scores unchanged: Kr@qr == K@q
        lo,de=ns['grid_perchannel'](Kr,bits)
        for n,fn in [('rtn',ns['q_rtn']),('sr',ns['q_sr']),('coup',ns['q_sr_coupledK'])]:
            ph=ns['softmax']((fn(Kr,lo,de)@qr)*scale); kl[n].append((p*np.log(p/ph)).sum())
    a={n:np.array(v) for n,v in kl.items()}
    print(f"K{bits} rotated, sharpness={temp}: median KL RTN={np.median(a['rtn']):.4f} indepSR={np.median(a['sr']):.4f} coupledSR={np.median(a['coup']):.4f} | coupled<indep {np.mean(a['coup']<a['sr']):.0%} | coupled<RTN {np.mean(a['coup']<a['rtn']):.0%}")
