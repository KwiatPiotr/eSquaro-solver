from z3 import *
import z3
from typing import List
from PIL import Image, ImageDraw, ImageFont

import puzzles
import time


class eSquaroSolverClass():
    def __init__(self, name: str):
        self.name = name


    def get_grid(self, grid: List[List[int]]):
        self.grid = grid
        self.xlen = len(grid)
        self.ylen = len(grid[0])
        self.xvars = len(grid) + 1
        self.yvars = len(grid[0]) + 1


    def solve_arithmetic(self):
        self.var = [[Real('_' + str(j) + '_' + str(i)) for i in range(self.xvars)] for j in range(self.yvars)]
        self.s = Solver()
        
        for i in range(self.xvars):
            for j in range(self.yvars):
                self.s.add(Or(self.var[i][j] == 0, self.var[i][j] == 1))
        
        for i in range(self.xlen):
            for j in range(self.ylen):
                self.s.add(self.var[i][j] + self.var[i+1][j] + self.var[i][j+1] + self.var[i+1][j+1] == self.grid[i][j])

        self.models = []
        
        while self.s.check() == sat:
            model = self.s.model()
            self.models.append(self.s.model())
            term = []
            for i in range(self.xlen):
                for j in range(self.ylen):
                    term.append(model[self.var[i][j]] != self.var[i][j])
            self.print_model_arithmetic(model, self.var)
            self.generate_image_arithmetic(self.var)

            self.s.add(Or(term))

    def solve_SAT(self):
        self.var = [[Bool('_' + str(j) + '_' + str(i)) for i in range(self.xvars)] for j in range(self.yvars)]
        self.s = Solver()

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

                elif self.grid[i][j] == 4:
                    self.s.add(
                        And(
                            self.var[i][j],
                            self.var[i+1][j],
                            self.var[i][j+1],
                            self.var[i+1][j+1])
                    )

        self.models = []

        while self.s.check() == sat:
            model = self.s.model()
            self.models.append(self.s.model())
            term = []
            for i in range(self.xlen):
                for j in range(self.ylen):
                    term.append(model[self.var[i][j]] != self.var[i][j])
            self.print_model_sat(model, self.var)
            self.generate_image_sat(self.var)
            self.s.add(Or(term))

                

    def generate_image_arithmetic(self, var):
        font = font = ImageFont.truetype('/usr/share/fonts/liberation/LiberationMono-Regular.ttf', 18)
        name = self.name

        counter = 0
        for model in self.models:
            img = Image.new('1', (31 * self.xlen, 31 * self.ylen), 1)
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
    
    def generate_image_sat(self, var):
        font = font = ImageFont.truetype('/usr/share/fonts/liberation/LiberationMono-Regular.ttf', 18)
        name = self.name

        counter = 0
        for model in self.models:
            img = Image.new('1', (31 * self.xlen, 31 * self.ylen), 1)
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

    def print_model_arithmetic(self, model, var):
        for i in range(self.xlen):
            buff = ''
            for j in range(self.ylen):
                buff += '1' if model[var[i][j]] == 1 else '0'
            print(buff)

    def print_model_sat(self, model, var):
        for i in range(self.xlen):
            buff = ''
            for j in range(self.ylen):
                buff += '1' if model[var[i][j]] else '0'
            print(buff)


s = eSquaroSolverClass('xyz_s')
s.get_grid(puzzles.grid_10_10)
s.solve_SAT()

print('------------------------------------------------')

s2 = eSquaroSolverClass('xyz_a')
s2.get_grid(puzzles.grid_10_10)

s2.solve_arithmetic()
