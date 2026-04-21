import numpy as np
import sys
sys.path.insert(0, '.')
from significancia.logic import Logic

L = Logic()

x  = np.array([130, 650, 99, 150, 128, 302, 95, 945, 368, 961], dtype=float)
y1 = np.array([186, 699, 132, 272, 291, 331, 199, 1890, 788, 1601], dtype=float)  # Actual Added/Modified
y1b= np.array([163, 765, 141, 166, 137, 355, 136, 1206, 433, 1130], dtype=float) # Plan Added/Modified
y2 = np.array([15.0, 69.9, 6.5, 22.4, 28.4, 65.9, 19.4, 198.7, 38.8, 138.2])
xk = 386.0


print("=== TEST 1 ===")
r1 = L.full_results(xk, x, y1)
print("rxy   =", round(r1["rxy"], 9), "  exp: 0.954496574")
print("r2    =", round(r1["r2"],  9), "  exp: 0.91106371")
print("tail  =", r1["tail"],          "  exp: 1.77517E-05")
print("beta0 =", round(r1["beta0"],9),"  exp: -22.55253275")
print("beta1 =", round(r1["beta1"],9),"  exp: 1.727932426")
print("yk    =", round(r1["yk"],   9),"  exp: 644.4293838")
print("range =", round(r1["range"],9),"  exp: 230.0017197")
print("UPI   =", round(r1["upi"],  9),"  exp: 874.4311035")
print("LPI   =", round(r1["lpi"],  9),"  exp: 414.427664")

print()
print("=== TEST 2 ===")
r2 = L.full_results(xk, x, y2)
print("rxy   =", round(r2["rxy"], 9), "  exp: 0.933306898")
print("r2    =", round(r2["r2"],  9), "  exp: 0.871061766")
print("tail  =", r2["tail"],          "  exp: 7.98203E-05")
print("beta0 =", round(r2["beta0"],9),"  exp: -4.038881575")
print("beta1 =", round(r2["beta1"],9),"  exp: 0.16812665")
print("yk    =", round(r2["yk"],   9),"  exp: 60.85800528")
print("range =", round(r2["range"],9),"  exp: 27.55764748")
print("UPI   =", round(r2["upi"],  9),"  exp: 88.41565276")
print("LPI   =", round(r2["lpi"],  9),"  exp: 33.3003578")
