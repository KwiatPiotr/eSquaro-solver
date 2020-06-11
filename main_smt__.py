from z3 import *

def print_model(model, var):
	for i in range(x_len + 1):
		buff = ''
		for j in range(y_len + 1):
			buff += '1' if model[var[i][j]] == 1 else '0'
		print(buff)

grid = [
	[2, 3, 1]
]

x_len = len(grid)		# -> i
y_len = len(grid[0])	# -> j


var = [[Real('_' + str(j) + '_' + str(i)) for i in range(y_len + 1)] for j in range(x_len + 1)]
s = Solver()

#print(var)

for i in range(x_len + 1):
	for j in range(y_len + 1):
		s.add(Or(var[i][j] == 0, var[i][j] == 1))

# s.add(var[i][j] + var[i+1][j] + var[i][j+1] + var[i+1][j+1] == grid[i][j])

# # 0 0
# s.add(var[0][0] + var[1][0] + var[0][1] + var[1][1] == grid[0][0])

# # 0 1
# s.add(var[0][1] + var[1][1] + var[0][2] + var[1][2] == grid[0][1])

# # 0 2
# s.add(var[0][2] + var[1][2] + var[0][3] + var[1][3] == grid[0][2])

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


