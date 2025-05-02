import transfert_vgl as TRANSFER
import matplotlib.pyplot as plt
from lamp import Lamp
"""
This file is the main file that will run the data analysis.
"""

#Afstanden ballonen:
D_lucht = 21.7e-2 # pm 0.3, ballon gevuld met lucht
D_He_zwak = 23.4e-2 # pm 0.3, ballon gevuld met commerciële Helium
D_He_sterk = 23.1e-2 # pm 0.3, ballon gevuld met puur Helium (Danku departement)


#Metingen bij lamp 4 en 5
D_He_zwak_2 = 23.4e-2
D_He_sterk_2 = 25.3e-2
D_lucht_2 = 24.7e-2

d_err = 0.3e-2

#Initialiseren van Lamp objecten (verschillende metingen)
#Niet gebruikte lampen -> geen kwaliteitsvolle metingen
lamp1 = Lamp(1, 10)
lamp2 = Lamp(2, 5)
lamp3 = Lamp(3, 12)

#Gebruikte data
lamp4 = Lamp(4, 6)
lamp5 = Lamp(5, 4)

#Effectieve analyse van de metingen
fig, ax, alpha_nu, alpha_nu_err, eta_nu, eta_nu_err, golf = TRANSFER.calculate_alpha_eta(lamp4, lamp5, D_He_sterk_2, d_err, 
                                                                                         pure_helium=False, rel_bck_calc=True, no_ballon_bck=False)

plt.tight_layout()
plt.show()