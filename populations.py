import matplotlib.pyplot as plt
import numpy as np

# Constants
kb = 8.6173324e-5  # Boltzmann constant (eV*K^-1)
kb_cgs = 1.380649e-16  # erg/K

# Ionization energies
X_Hminus_HI = 0.755  # eV
X_HI_HII = 13.598434599702  # eV

# Partition functions
U_Hminus = 1.0
U_HI = 2.0
U_HII = 1.0


# function to calculate the populations
def calculate_populations(T, Pe):

    # Calculate Ne for each Pe and T
    Ne = Pe / (kb_cgs * T)

    # Ionization populations (Saha equation)
    def saha_ecuation(U_j, U_j_1, X_j):
        return (
            2.07
            * 10 ** (-16)
            * Ne
            * (U_j / U_j_1)
            * T ** (-3 / 2)
            * np.exp(X_j / (kb * T))
        )

    # Calculate the ionization populations N_Hminus/N_HI and N_HI/N_HII:
    A = saha_ecuation(U_Hminus, U_HI, X_Hminus_HI)  # N_Hminus/N_HI
    B = saha_ecuation(U_HI, U_HII, X_HI_HII)  # N_HI/N_HII

    # Solving the system with 3 equations (N_Hminus/N_HI, N_HI/N_HII and
    # charge conservation (Ne + N_Hminus = N_HII)) we obtain the H populations:
    N_Hminus = A * B * Ne / (1 - A * B)
    N_HI = N_Hminus / A
    N_HII = N_Hminus / (A * B)

    # Excitation energies
    XX_ij = [0, 10.206, 12.095]  # levels: n=1, n=2, n=3 (eV)
    # Statistical weights
    gg = [2, 8, 18]  # g(n) = 2n^2

    # Excitation populations (Boltzmann equation)
    def boltzmann_equation(g_ij, U_j, X_ij):
        return (g_ij / U_j) * np.exp(-X_ij / (kb * T)) * N_HI
        # we multiply by N_HI to obtain the population in the excitation level i

    # Calculate the excitation populations:
    N_HI_n1 = boltzmann_equation(gg[0], U_HI, XX_ij[0])
    N_HI_n2 = boltzmann_equation(gg[1], U_HI, XX_ij[1])
    N_HI_n3 = boltzmann_equation(gg[2], U_HI, XX_ij[2])

    # ********* Checks *********

    # Check charge conservation: Ne + N_Hminus = N_HII
    charge_difference = np.abs((Ne + N_Hminus) - N_HII)
    print(
        "Charge conservation check (should be close to 0):", np.max(charge_difference)
    )

    # Check excitation populations are less than N_HI
    assert np.all(N_HI_n1 <= N_HI), "Excitation level n=1 exceeds N_HI"
    assert np.all(N_HI_n2 <= N_HI), "Excitation level n=2 exceeds N_HI"
    assert np.all(N_HI_n3 <= N_HI), "Excitation level n=3 exceeds N_HI"

    # ********* End checks *********

    N_ionization = [N_Hminus, N_HI, N_HII]
    N_excitation = [N_HI_n1, N_HI_n2, N_HI_n3]

    return Ne, N_ionization, N_excitation
