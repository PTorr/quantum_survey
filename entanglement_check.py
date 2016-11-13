import numpy as np

def entanglement_checker(psi): # qc = qbits_coefficients
    '''This function is checking if 2 qbits are entangled.
       To do this it calculates the concurrence as documented in:
       https://en.wikipedia.org/wiki/Concurrence_(quantum_computing)
       input: psi - [a00,a01,a10,a11]
       output: evc - eigenvalues subtraction value
               c - return max[0,evc]
               entangled - 1/0 is entangled'''

    from sympy.physics.matrices import msigma  # pauli matrices

    # Computing the density matrix
    psi = np.matrix(psi)
    rho = np.kron(psi,psi.transpose())

    # Computing rho wave for R matrix
    pauli_k = np.kron(msigma(2),msigma(2))
    rho_wave = np.dot(np.dot(pauli_k,np.conjugate(rho)),pauli_k)


    # Computing R
    R_1 = np.dot(np.sqrt(rho),rho_wave)
    R_2 = np.dot(R_1,np.sqrt(rho))
    R_2 = np.float64(R_2)
    R = np.sqrt(R_2)
    # print R

    # Finding the eigenvalues of R
    R[np.isnan(R)] = 0
    # np.nan_to_num(R)
    ev = np.linalg.eigvals(R)

    # Check for entanglement
    evc = ev[0]-sum(ev[1:4])
    c = np.max([0,evc])
    if c>0:
        entangled = 1
    else:
        entangled = 0

    return evc, c, entangled


