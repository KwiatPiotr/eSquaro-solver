from z3 import *
from typing import List, Union
from PIL import Image, ImageDraw, ImageFont
import puzzles
import time


class eSquaroSolverClass():
    # eSquaroSolverClass constuctor
    #   param: name (str) -> used to name result file
    #   returns: None
    # 
    # Function creates object and assigns name to it
    #
    def __init__(self, name: str) -> None:
        self.name = name

    # eSquaroSolverClass.get_grid(grid)
    #   param: grid (List[List[int]]) -> representation of eSquaro puzzle
    #   returns: None
    #
    # Function add new variables (puzzle's shape and count of variables)
    #
    def get_grid(self, grid: List[List[int]]) -> None:
        self.grid = grid
        self.xlen = len(grid)
        self.ylen = len(grid[0])
        self.xvars = len(grid) + 1
        self.yvars = len(grid[0]) + 1


    # eSquaroSolverClass.solve_arithmetic()
    #   params: None:
    #   return: 0 -> puzzle is solvable (sat problem)
    #   return: 1 -> puzzle is unsolvable (unsat problem)
    #
    # Function triggers solving algorithms (arithmeric) and triggers generating image
    #
    def solve_arithmetic(self) -> int:
        # creating matrix of z3 variables and z3 obj
        self.var = [[Real('_' + str(j) + '_' + str(i)) for i in range(self.xvars)] for j in range(self.yvars)]
        self.s = Solver()
        
        # adding first rule to make Real values acting like Boolean values (be 1 or 0)
        for i in range(self.xvars):
            for j in range(self.yvars):
                self.s.add(Or(self.var[i][j] == 0, self.var[i][j] == 1))
        
        # adding rules to solve puzzle
        # a + b + c + d = X, where:
        # a, b, c, d    -> values in each corner of small square
        # X             -> values in small square
        for i in range(self.xlen):
            for j in range(self.ylen):
                self.s.add(self.var[i][j] + self.var[i+1][j] + self.var[i][j+1] + self.var[i+1][j+1] == self.grid[i][j])
        
        # if problem is unsolvable return 1
        if self.s.check() == unsat:
            return 1
        # else show some results and return 0
        else:
            # container for all models
            self.models = []

            # creating all possible results
            while self.s.check() == sat:
                # creating model's result and adding it to container
                model = self.s.model()
                self.models.append(self.s.model())

                # creating container for current result so they won't appear again
                term = []
                for i in range(self.xvars):
                    for j in range(self.yvars):
                        term.append(model[self.var[i][j]] != self.var[i][j])

                # printing result on stdout
                self.print_model_arithmetic(model, self.var)

                # creating image with solved puzzle
                self.generate_image_arithmetic(self.var)

                # adding current result to solver not to create infinite loop
                self.s.add(Or(term))

        return 0


    # eSquaroSolverClass.solve_SAT()
    #   params: None:
    #   return: 0 -> puzzle is solvable (sat problem)
    #   return: 1 -> puzzle is unsolvable (unsat problem)
    #
    # Function triggers solving algorithms (boolean) and triggers generating image
    #
    def solve_SAT(self) -> int:
        # creating matrix of z3 variables and z3 obj
        self.var = [[Bool('_' + str(j) + '_' + str(i)) for i in range(self.xvars)] for j in range(self.yvars)]
        self.s = Solver()
        self.g = Goal()
        
        # adding rules to solve puzzle
        for i in range(self.xlen):
            for j in range(self.ylen):
                if self.grid[i][j] == 0:
                    self.s.add(
                        And(
                            Not(self.var[i][j]),
                            Not(self.var[i+1][j]),
                            Not(self.var[i][j+1]),
                            Not(self.var[i+1][j+1]))
                    )
                    self.g.add(
                        And(
                            Not(self.var[i][j]),
                            Not(self.var[i+1][j]),
                            Not(self.var[i][j+1]),
                            Not(self.var[i+1][j+1]))
                    )

                elif self.grid[i][j] == 1:
                    self.s.add(
                        Or(
                            And(
                                self.var[i][j],
                                Not(self.var[i+1][j]),
                                Not(self.var[i][j+1]),
                                Not(self.var[i+1][j+1])),
                            And(
                                Not(self.var[i][j]),
                                self.var[i+1][j],
                                Not(self.var[i][j+1]),
                                Not(self.var[i+1][j+1])),
                            And(
                                Not(self.var[i][j]),
                                Not(self.var[i+1][j]),
                                self.var[i][j+1],
                                Not(self.var[i+1][j+1])),
                            And(
                                Not(self.var[i][j]),
                                Not(self.var[i+1][j]),
                                Not(self.var[i][j+1]),
                                self.var[i+1][j+1]),
                        )
                    )
                    self.g.add(
                        Or(
                            And(
                                self.var[i][j],
                                Not(self.var[i+1][j]),
                                Not(self.var[i][j+1]),
                                Not(self.var[i+1][j+1])),
                            And(
                                Not(self.var[i][j]),
                                self.var[i+1][j],
                                Not(self.var[i][j+1]),
                                Not(self.var[i+1][j+1])),
                            And(
                                Not(self.var[i][j]),
                                Not(self.var[i+1][j]),
                                self.var[i][j+1],
                                Not(self.var[i+1][j+1])),
                            And(
                                Not(self.var[i][j]),
                                Not(self.var[i+1][j]),
                                Not(self.var[i][j+1]),
                                self.var[i+1][j+1]),
                        )
                    )
                
                elif self.grid[i][j] == 2:
                    self.s.add(
                        Or(
                            And(
                                self.var[i][j],
                                self.var[i+1][j],
                                Not(self.var[i][j+1]),
                                Not(self.var[i+1][j+1])),
                            And(
                                self.var[i][j],
                                Not(self.var[i+1][j]),
                                self.var[i][j+1],
                                Not(self.var[i+1][j+1])),
                            And(
                                self.var[i][j],
                                Not(self.var[i+1][j]),
                                Not(self.var[i][j+1]),
                                self.var[i+1][j+1]),

                            And(
                                Not(self.var[i][j]),
                                self.var[i+1][j],
                                self.var[i][j+1],
                                Not(self.var[i+1][j+1])),
                            And(
                                Not(self.var[i][j]),
                                self.var[i+1][j],
                                Not(self.var[i][j+1]),
                                self.var[i+1][j+1]),

                            And(
                                Not(self.var[i][j]),
                                Not(self.var[i+1][j]),
                                self.var[i][j+1],
                                self.var[i+1][j+1])
                        )
                    )
                    self.g.add(
                        Or(
                            And(
                                self.var[i][j],
                                self.var[i+1][j],
                                Not(self.var[i][j+1]),
                                Not(self.var[i+1][j+1])),
                            And(
                                self.var[i][j],
                                Not(self.var[i+1][j]),
                                self.var[i][j+1],
                                Not(self.var[i+1][j+1])),
                            And(
                                self.var[i][j],
                                Not(self.var[i+1][j]),
                                Not(self.var[i][j+1]),
                                self.var[i+1][j+1]),

                            And(
                                Not(self.var[i][j]),
                                self.var[i+1][j],
                                self.var[i][j+1],
                                Not(self.var[i+1][j+1])),
                            And(
                                Not(self.var[i][j]),
                                self.var[i+1][j],
                                Not(self.var[i][j+1]),
                                self.var[i+1][j+1]),

                            And(
                                Not(self.var[i][j]),
                                Not(self.var[i+1][j]),
                                self.var[i][j+1],
                                self.var[i+1][j+1])
                        )
                    )
                
                elif self.grid[i][j] == 3:
                    self.s.add(
                        Or(
                            And(
                                self.var[i][j],
                                self.var[i+1][j],
                                self.var[i][j+1],
                                Not(self.var[i+1][j+1])),
                            And(
                                self.var[i][j],
                                self.var[i+1][j],
                                Not(self.var[i][j+1]),
                                self.var[i+1][j+1]),
                            And(
                                self.var[i][j],
                                Not(self.var[i+1][j]),
                                self.var[i][j+1],
                                self.var[i+1][j+1]),
                            And(
                                Not(self.var[i][j]),
                                self.var[i+1][j],
                                self.var[i][j+1],
                                self.var[i+1][j+1]),
                        )
                    )
                    self.g.add(
                        Or(
                            And(
                                self.var[i][j],
                                self.var[i+1][j],
                                self.var[i][j+1],
                                Not(self.var[i+1][j+1])),
                            And(
                                self.var[i][j],
                                self.var[i+1][j],
                                Not(self.var[i][j+1]),
                                self.var[i+1][j+1]),
                            And(
                                self.var[i][j],
                                Not(self.var[i+1][j]),
                                self.var[i][j+1],
                                self.var[i+1][j+1]),
                            And(
                                Not(self.var[i][j]),
                                self.var[i+1][j],
                                self.var[i][j+1],
                                self.var[i+1][j+1]),
                        )
                    )

                elif self.grid[i][j] == 4:
                    self.s.add(
                        And(
                            self.var[i][j],
                            self.var[i+1][j],
                            self.var[i][j+1],
                            self.var[i+1][j+1])
                    )
                    self.g.add(
                        And(
                            self.var[i][j],
                            self.var[i+1][j],
                            self.var[i][j+1],
                            self.var[i+1][j+1])
                    )

        # DIMACS
        t = Then('bit-blast', 'tseitin-cnf')
        subgoal = t(self.g)
        print(type(subgoal[0]))
        print(subgoal[0].dimacs())
        # DIMACS
        
        # if problem is unsolvable return 1
        if self.s.check() == unsat:
            return 1
        # else show some results and return 0
        else:
            # container for all models            
            self.models = []

            # creating all possible results
            while self.s.check() == sat:
                # creating model's result and adding it to container
                model = self.s.model()
                self.models.append(self.s.model())

                # creating container for current result so they won't appear again
                term = []
                for i in range(self.xvars):
                    for j in range(self.yvars):
                        term.append(model[self.var[i][j]] != self.var[i][j])

                # printing result on stdout
                self.print_model_sat(model, self.var)

                # creating image with solved puzzle
                self.generate_image_sat(self.var)

                # adding current result to solver not to create infinite loop
                self.s.add(Or(term))
            return 0
                

    # eSquaroSolverClass.generate_image_arithmetic()
    #   param: var (List[List[z3.Real]]) -> result for puzzle
    #   return: None
    #
    # Function generates image of solved puzzle
    #
    def generate_image_arithmetic(self, var: List[List[z3.Real]]) -> None:
        font = font = ImageFont.truetype('LiberationMono-Regular.ttf', 18)
        name = self.name

        counter = 0
        for model in self.models:
            img = Image.new('1', (40 + (self.xlen - 1) * 30, 40 + (self.ylen - 1) * 30), 1)
            draw = ImageDraw.Draw(img)
            for i in range(self.xlen):
                for j in range(self.ylen):
                    beg = (30 * i + 5, 30 * j + 5)
                    end = (30 * i + 35, 30 * j + 35)
                    text_pnt = (30 * i + 14, 30 * j + 11)
                    draw.rectangle((beg, end))
                    draw.text(text_pnt, str(self.grid[i][j]), fill='black', font=font)

            for i in range(self.xvars):
                for j in range(self.yvars):
                    if model[var[i][j]] == 1:
                        draw.ellipse((i * 30, j * 30, i * 30 + 11, j * 30 + 11), fill='black', outline='black')
                    else:
                        draw.ellipse((i * 30, j * 30, i * 30 + 11, j * 30 + 11), fill='white', outline='black')
                    
            img.save(name + '-' + str(counter) + '.png')
            counter += 1

    
    # eSquaroSolverClass.generate_image_sat()
    #   param: var (List[List[z3.Bool]]) -> result for puzzle
    #   return: None
    #
    # Function generates image of solved puzzle
    #
    def generate_image_sat(self, var: List[List[Bool]]) -> None:
        font = font = ImageFont.truetype('LiberationMono-Regular.ttf', 18)
        name = self.name

        counter = 0
        for model in self.models:
            img = Image.new('1', (40 + (self.xlen - 1) * 30, 40 + (self.ylen - 1) * 30), 1)
            draw = ImageDraw.Draw(img)
            for i in range(self.xlen):
                for j in range(self.ylen):
                    beg = (30 * i + 5, 30 * j + 5)
                    end = (30 * i + 35, 30 * j + 35)
                    text_pnt = (30 * i + 14, 30 * j + 11)
                    draw.rectangle((beg, end))
                    draw.text(text_pnt, str(self.grid[i][j]), fill='black', font=font)

            for i in range(self.xvars):
                for j in range(self.yvars):
                    if model[var[i][j]]:
                        draw.ellipse((i * 30, j * 30, i * 30 + 11, j * 30 + 11), fill='black', outline='black')
                    else:
                        draw.ellipse((i * 30, j * 30, i * 30 + 11, j * 30 + 11), fill='white', outline='black')
            
            
            img.save(name + '-' + str(counter) + '.png')
            counter += 1


    def print_model_arithmetic(self, model, var):
        for i in range(self.xvars):
            buff = ''
            for j in range(self.yvars):
                buff += '1' if model[var[i][j]] == 1 else '0'
            print(buff)


    def print_model_sat(self, model, var):
        for i in range(self.xvars):
            buff = ''
            for j in range(self.yvars):
                buff += '1' if model[var[i][j]] else '0'
            print(buff)


grid = [
    [2]
]

# grid = puzzles.grid_10_10

s = eSquaroSolverClass('xyz_s')
s.get_grid(grid)
if s.solve_SAT():
    print('wrong puzzle')

# print('------------------------------------------------')

# s2 = eSquaroSolverClass('xyz_a')
# s2.get_grid(grid)
# if s2.solve_arithmetic():
#     print('wrong puzzle')
