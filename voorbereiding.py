import sympy as sp



I1_in, I1_out, I2_in, I2_out, alpha, eta, D = sp.symbols('I_1^in I_1^out I_2^in I_2^out alpha eta D')

sol = sp.solve([I1_out - I1_in*sp.exp(-alpha*D) - eta/alpha*(1-sp.exp(-alpha*D)),
                I2_out - I2_in*sp.exp(-alpha*D) - eta/alpha*(1-sp.exp(-alpha*D))],
                [alpha, eta])

print("Alpha = " + str(sol[0][0]))
print("Eta = " + str(sol[0][1]))
print(type(sol[0][0]))

alpha = sol[0][0]
eta = sol[0][1]

sI1_in, sI1_out, sI2_in, sI2_out, salpha, seta, sD = sp.symbols('s_I_1^in I_1^out s_I_2^in s_I_2^out s_alpha s_eta s_D')

alpha_err = sp.simplify(sp.sqrt(
                          sp.diff(alpha, I1_in)**2*sI1_in**2
                        + sp.diff(alpha, I1_out)**2*sI1_out**2
                        + sp.diff(alpha, I2_in)**2*sI2_in**2
                        + sp.diff(alpha, I2_out)**2*sI2_out**2
                        + sp.diff(alpha, D)**2*sD**2))

eta_err = sp.simplify(sp.sqrt(
                          sp.diff(eta, I1_in)**2*sI1_in**2
                        + sp.diff(eta, I1_out)**2*sI1_out**2
                        + sp.diff(eta, I2_in)**2*sI2_in**2
                        + sp.diff(eta, I2_out)**2*sI2_out**2
                        + sp.diff(eta, D)**2*sD**2))

print("s_alpha = " + str(alpha_err))
print("s_eta = " + str(eta_err))