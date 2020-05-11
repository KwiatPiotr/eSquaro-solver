from z3 import *


def print_model(model, var):
	for i in range(x_len + 1):
		buff = ''
		for j in range(y_len + 1):
			buff += '1' if model[var[i][j]] == 1 else '0'
		print(buff)
	print('-' * (x_len + 1) )


grid = [
	[2, 3, 1, 0, 0, 1, 2, 3, 2, 1],
	[1, 3, 2, 1, 2, 2, 3, 4, 3, 2],
	[2, 3, 2, 2, 3, 2, 2, 2, 3, 3],
	[4, 3, 2, 3, 2, 0, 0, 0, 2, 3],
	[2, 1, 2, 4, 2, 1, 1, 1, 3, 2],
	[1, 1, 3, 4, 2, 2, 2, 2, 4, 3],
	[2, 2, 2, 3, 3, 2, 1, 1, 2, 2],
	[3, 2, 0, 1, 2, 2, 1, 0, 1, 1],
	[4, 3, 2, 1, 1, 3, 3, 2, 2, 2],
	[2, 3, 3, 2, 2, 2, 3, 3, 2, 3]
]

grid = [
	[2, 2],
	[2, 2]
]

x_len = len(grid)		# -> i
y_len = len(grid[0])	# -> j


var = [[Real('_' + str(j) + '_' + str(i)) for i in range(x_len + 1)] for j in range(y_len + 1)]
s = Solver()

#print(var)

for i in range(x_len + 1):
	for j in range(y_len + 1):
		s.add(Or(var[i][j] == 0, var[i][j] == 1))

#print(s.check())
for i in range(x_len):
	for j in range(y_len):
		s.add(var[i][j] + var[i+1][j] + var[i][j+1] + var[i+1][j+1] == grid[i][j])

#print(s.check())
while s.check() == sat:
	model = s.model()
	term = []
	for i in range(x_len):
		for j in range(y_len):
			term.append(model[var[i][j]] != var[i][j])
	print_model(model, var)
	s.add(Or(term))


