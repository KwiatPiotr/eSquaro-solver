from z3 import *

l = [Real('_' + str(i)) for i in range(10)]

print(l)
s = Solver()

for i in range(10):
    s.add(Or(l[i] == 0, l[i] == 1))

for i in range(10):
    s.add(l[i] + l[(i+1)%10] == 2)

print(s.check())
print(s.model())


