"""Compare vacancy and surface energy plots."""
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import pandas as pd

plt.switch_backend("agg")

df = pd.read_csv("defects_comparison.csv")
V_DFT = df["V_DFT"].dropna().values
V_TB = df["V_TB"].dropna().values
Gamma_DFT = df["Gamma_DFT"].dropna().values
Gamma_TB = df["Gamma_TB"].dropna().values


print(len(V_TB), len(V_DFT))
print(len(Gamma_TB), len(Gamma_DFT))

the_grid = GridSpec(1, 2)
plt.rcParams.update({"font.size": 18})
plt.figure(figsize=(10, 5))


plt.subplot(the_grid[0])
plt.title("(a)")
plt.plot(V_DFT, V_TB, ".")
plt.plot(V_DFT, V_DFT)
plt.xlabel("DFT V$_f$ (eV)")
plt.ylabel("TB3 V$_f$ (eV)")
plt.xlim([0.1, 4])
plt.ylim([0.1, 4])

plt.subplot(the_grid[1])
plt.title("(b)")
plt.plot(Gamma_DFT, Gamma_TB, ".")
plt.plot(Gamma_DFT, Gamma_DFT)
plt.xlabel("DFT gamma (Jm$^{-2}$)")
plt.ylabel("TB3 gamma (Jm$^{-2}$)")
plt.xlim([0.1, 4])
plt.ylim([0.1, 4])

plt.tight_layout()
plt.savefig("defectcomp.pdf")
plt.close()
