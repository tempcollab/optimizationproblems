"""Compute the CHEAP pieces (diff |U-U| and max(U)) for d=140/T=263 and persist
them to d140_diffmax.json. The heavy sumset runs in a separate call."""
import os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "engine"))
from digit_dp import max_U, count_opset
A=[0,2,3,4,5,6,7,8,9,10]; B=21; d=140; T=263
assert B>2*max(A)
t0=time.time()
Nm=count_opset(A,d,T,'-')
M=max_U(A,B,d,T)
json.dump({"Nminus":str(Nm),"maxU":str(M),"d":d,"T":T,"elapsed_s":time.time()-t0},
          open(os.path.join(HERE,"d140_diffmax.json"),"w"),indent=2)
print(f"|U-U|={len(str(Nm))}d max(U)={len(str(M))}d t={time.time()-t0:.1f}s PERSISTED",flush=True)
