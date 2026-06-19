"""Heavy sumset via the engine's count_opset (proven-fast path, no logging
overhead). Loads diff/max from d140_diffmax.json, persists beat_d140.json."""
import os, sys, json, time, math
HERE=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,os.path.join(HERE,"..","engine"))
from digit_dp import count_opset
A=[0,2,3,4,5,6,7,8,9,10]; B=21; d=140; T=263
dm=json.load(open(os.path.join(HERE,"d140_diffmax.json")))
Nm=int(dm["Nminus"]); M=int(dm["maxU"])
t0=time.time()
Np=count_opset(A,d,T,'+')
el=time.time()-t0
v=1+math.log(Nm/Np)/math.log(2*M+1)
out={"cell":"d140_T263","A":A,"B":B,"d":d,"T":T,"density":T/d,
     "Nplus":str(Np),"Nminus":str(Nm),"maxU":str(M),
     "value_float":v,"value_record_float":1.1740744476935212,
     "elapsed_s":el,"done":True}
json.dump(out,open(os.path.join(HERE,"beat_d140.json"),"w"),indent=2)
with open(os.path.join(HERE,"run_d140_engine.log"),"w") as f:
    f.write(f"|U+U|={len(str(Np))}d sum_elapsed={el:.1f}s value={v:.13f} PERSISTED\n")
print(f"|U+U|={len(str(Np))}d sum_elapsed={el:.1f}s value={v:.13f} PERSISTED",flush=True)
