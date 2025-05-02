import data_reader as DATA
import transfert_vgl as TRANSFER
import matplotlib.pyplot as plt
from lamp import Lamp
import tools_experimentele.easystats as STAT



D_He_zwak_2 = 23.4e-2
D_He_sterk_2 = 25.3e-2
D_lucht_2 = 24.7e-2

d_err = 0.3e-2

newLamp1 = Lamp(4, 6)
newLamp2 = Lamp(5, 4)


fig, ax, alpha_nu, alpha_nu_err, eta_nu, eta_nu_err, golf = TRANSFER.calculate_alpha_eta(newLamp1, newLamp2, D_He_sterk_2, d_err, 
                                                                                         pure_helium=True, rel_bck_calc=True, no_ballon_bck=False)

plt.tight_layout()
plt.show()



#Plot de source function (eta_nu / alpha_nu)
BB = []
BB_err = []
for i in range(0, len(alpha_nu)):
    BB.append(eta_nu[i]/alpha_nu[i])
    BB_err.append(STAT.foutpropagatie_product(1, -1, eta_nu_err[i], alpha_nu_err[i], eta_nu[i], alpha_nu[i], BB[i]))

fig, ax = plt.subplots()

ax.errorbar(golf, BB, yerr=BB_err,
                        
                label="Calculations", fmt=" ", marker="o", color="black", ecolor="black", markersize=1, capsize=1.5, capthick=0.5, elinewidth=0.5)

plt.tight_layout()
plt.legend()
plt.show()