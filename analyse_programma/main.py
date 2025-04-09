import data_reader as DATA
import transfert_vgl as TRANSFER
import matplotlib.pyplot as plt
from lamp import Lamp
"""
This file is the main file that will run the data analysis.
"""

#Afstanden ballonen:
D_lucht = 21.7 # pm 0.5, ballon gevuld met lucht
D_He_zwak = 23.4 # pm 0.5, ballon gevuld met commerciële Helium
D_He_sterk = 23.1 # pm 0.5, ballon gevuld met puur Helium (thx departement)

D_He_zwak_2 = 23.4
D_lucht_2 = 24.7

lamp1 = Lamp(1, 10)
lamp2 = Lamp(2, 5)
lamp3 = Lamp(3, 12)
lamp4 = Lamp(4, 6)
lamp5 = Lamp(5, 4)
lamps = [lamp1, lamp2, lamp3, lamp4]

fig, ax = TRANSFER.calculate_alpha_eta(lamp4, lamp5, D_He_zwak_2, pure_helium=False, no_ballon_bck=False)

plt.tight_layout()
plt.show()