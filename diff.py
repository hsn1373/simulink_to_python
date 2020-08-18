import sympy as sp
x = sp.Symbol("x")
# print(sp.diff(sp.sin(sp.tan(x)), x))

# Derivative
print(sp.diff(sp.sin(x), x))


# Integeral
print(sp.integrate(sp.sin(x), x))

#The definite integral
print(sp.integrate(sp.sin(x), (x, 0, sp.pi / 2)))

print(0.05 + (3.5+0.09)*0.0001)