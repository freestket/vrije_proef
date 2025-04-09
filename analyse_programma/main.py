import data_reader as DATA
import transfert_vgl as TRANSFER
import matplotlib.pyplot as plt
from lamp import Lamp
import tools_experimentele.easystats as STAT
"""
This file is the main file that will run the data analysis.
"""

#Afstanden ballonen:
D_lucht = 21.7e-2 # pm 0.5, ballon gevuld met lucht
D_He_zwak = 23.4e-2 # pm 0.5, ballon gevuld met commerciële Helium
D_He_sterk = 23.1e-2 # pm 0.5, ballon gevuld met puur Helium (thx departement)

D_He_zwak_2 = 23.4e-2
D_He_sterk_2 = 25.3e-2
D_lucht_2 = 24.7e-2

D_dubbel = 56.8e-2
D_dubbel_ballonnen = 51.5e-2

lamp1 = Lamp(1, 10)
lamp2 = Lamp(2, 5)
lamp3 = Lamp(3, 12)
lamp4 = Lamp(4, 6)
lamp5 = Lamp(5, 4)
lamps = [lamp1, lamp2, lamp3, lamp4]

fig, ax, alpha_nu, alpha_nu_err, eta_nu, eta_nu_err, golf = TRANSFER.calculate_alpha_eta(lamp4, lamp5, D_He_sterk_2, pure_helium=True, no_ballon_bck=False)

plt.tight_layout()
plt.show()

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