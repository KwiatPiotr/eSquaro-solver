from z3 import *

def print_model(model, var):
    for i in range(x_len + 1):
        buff = ''
        for j in range(y_len + 1):
            buff += '1' if model[var[i][j]] else '0'
        print(buff)
    print('--------------------------------------')

grid = [
	[2, 3, 1, 0, 0],
	[1, 3, 2, 1, 2],
	[2, 3, 2, 2, 3],
	[4, 3, 2, 3, 2],
	[2, 1, 2, 4, 2]
]
# grid = [[1]]


x_len = len(grid)		# -> i
y_len = len(grid[0])	# -> j


var = [[Bool('_' + str(j) + '_' + str(i)) for i in range(x_len + 1)] for j in range(y_len + 1)]
s = Solver()



# print(s.check())
for i in range(x_len):
    for j in range(y_len):
        if grid[i][j] == 0:
            s.add(And(Not(var[i][j]), Not(var[i+1][j]), Not(var[i][j+1]), Not(var[i+1][j+1])))
        elif grid[i][j] == 1:
            s.add(
                Or(
                    And(var[i][j], Not(var[i+1][j]), Not(var[i][j+1]), Not(var[i+1][j+1])),
                    And(Not(var[i][j]), var[i+1][j], Not(var[i][j+1]), Not(var[i+1][j+1])),
                    And(Not(var[i][j]), Not(var[i+1][j]), var[i][j+1], Not(var[i+1][j+1])),
                    And(Not(var[i][j]), Not(var[i+1][j]), Not(var[i][j+1]), var[i+1][j+1])
                )
            )
        elif grid[i][j] == 2:
            s.add(
                Or(
                    And(var[i][j], var[i+1][j], Not(var[i][j+1]), Not(var[i+1][j+1])),
                    And(var[i][j], Not(var[i+1][j]), var[i][j+1], Not(var[i+1][j+1])),
                    And(var[i][j], Not(var[i+1][j]), Not(var[i][j+1]), var[i+1][j+1]),

                    And(Not(var[i][j]), var[i+1][j], var[i][j+1], Not(var[i+1][j+1])),
                    And(Not(var[i][j]), var[i+1][j], Not(var[i][j+1]), var[i+1][j+1]),

                    And(Not(var[i][j]), Not(var[i+1][j]), var[i][j+1], var[i+1][j+1]),
                )
            )
        elif grid[i][j] == 3:
            s.add(
                Or(
                    And(var[i][j], var[i+1][j], var[i][j+1], Not(var[i+1][j+1])),
                    And(var[i][j], var[i+1][j], Not(var[i][j+1]), var[i+1][j+1]),
                    And(var[i][j], Not(var[i+1][j]), var[i][j+1], var[i+1][j+1]),
                    And(Not(var[i][j]), var[i+1][j], var[i][j+1], var[i+1][j+1])
                )
            )
        

# print(s.check())
while s.check() == sat:
    model = s.model()
    term = []
    for i in range(x_len+1):
        for j in range(y_len+1):
            term.append(model[var[i][j]] != var[i][j])
    print(model)
    print(term)
    print(s.sexpr())
    print_model(model, var)
    s.add(Or(term))


