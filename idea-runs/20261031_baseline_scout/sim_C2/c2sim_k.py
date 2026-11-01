import numpy as np, importlib.util, sys
spec=importlib.util.spec_from_file_location('c',sys.argv[1]); 
src=open(sys.argv[1]).read().split('r=run(8)')[0]; ns={}; exec(src,ns)
rng=ns['rng']
for temp in [0.3,1.0,3.0]:
    kl={'rtn':[],'sr':[],'coup':[]}
    for t in range(60):
        K,V=ns['kv'](); q=rng.normal(0,1,ns['d'])/np.sqrt(ns['d'])
        z0=K@q; scale=(temp*3)/z0.std(); p=ns['softmax'](z0*scale)
        lo,de=ns['grid_perchannel'](K,2)
        for n,fn in [('rtn',ns['q_rtn']),('sr',ns['q_sr']),('coup',ns['q_sr_coupledK'])]:
            ph=ns['softmax']((fn(K,lo,de)@q)*scale); kl[n].append((p*np.log(p/ph)).sum())
    a={n:np.array(v) for n,v in kl.items()}
    win=np.mean(a['coup']<a['sr'])
    print(f"sharpness={temp}: median KL RTN={np.median(a['rtn']):.3f} indepSR={np.median(a['sr']):.3f} coupledSR={np.median(a['coup']):.3f} | mean coupled={a['coup'].mean():.3f} vs indep={a['sr'].mean():.3f} | coupled<indep in {win:.0%} of trials | RTN<coupled in {np.mean(a['rtn']<a['coup']):.0%}")
