def f(a, L=[]):

    print(hex(id(L)))

    L.append(a)

    return L

print(f(1))

print(f(2))

print(f(3))