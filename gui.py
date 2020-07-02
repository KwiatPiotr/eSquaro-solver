import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from typing import List
from eSquaroSolver import eSquaroSolverClass


class Application(tk.Frame):
    def __init__(self, master: tk.Tk = None):
        super().__init__(master)
        self.master = master
        
        self.list_name = []
        self.solution_counter = 0
        self.list_img = []

        self.read_file = tk.BooleanVar()
        
        # Input Labels
        tk.Label(self.master, text='File or input (1 file, 0 input):').grid(row=0, column=0, columnspan=1)
        tk.Label(self.master, text='Output name:').grid(row=1, column=0, columnspan=2)
        tk.Label(self.master, text='Filename / Input:').grid(row=3, column=0, columnspan = 2)
        tk.Label(self.master, text='Errors:').grid(row=11, column=0, columnspan = 2)

        # Output Labels
        tk.Label(self.master, text='Path to results').grid(row=0, column=2, columnspan=2)
        tk.Label(self.master, text='Results').grid(row=2, column=2, columnspan=2)

        # Input Entries
        self.file_of_input = tk.Checkbutton(self.master, variable=self.read_file)
        self.file_of_input.grid(row=0, column=1, columnspan=1)
        self.entry_out_name = tk.Entry(self.master, width=40)
        self.entry_out_name.grid(row=2, column=0, columnspan=2) 
        self.entry_puzzle = ScrolledText(self.master, width=40, height=11)
        self.entry_puzzle.grid(row=4, column=0, columnspan=2)
        self.entry_errors = ScrolledText(self.master, width=40, height=11)
        self.entry_errors.grid(row=12, column=0, columnspan=2)
        
        # Output Entries
        self.dump_out_path = tk.Entry(self.master, width=40)
        self.dump_out_path.grid(row=1, column=2, columnspan = 2)
        
        # Button
        tk.Button(self.master, text='Solve', command=self.submit).grid(row=10, column=0, columnspan=2)
        tk.Button(self.master, text='Next', command=self.next).grid(row=3, column=2, columnspan=2)

        # Canvas
        self.canvas = tk.Canvas(self.master, width=1000, height=1000)
        self.canvas.grid(row=4, column=2, rowspan=1000)
        img = tk.PhotoImage(file='hehe-0.png')
        self.image_on_canvas = self.canvas.create_image(0, 0, image=img, anchor="nw")

        # mainloop
        self.master.mainloop()



    def next(self):
        if self.list_name:
            if not self.list_img:
                self.list_img = [tk.PhotoImage(file=name) for name in self.list_name]
            else:
                self.solution_counter += 1
                if self.solution_counter == self.solution_count:
                    self.solution_counter = 0

                self.canvas.itemconfig(self.image_on_canvas, image=self.list_img[self.solution_counter])
                print(self.list_name[self.solution_counter])
        else:
            self.entry_errors.insert(tk.END, 'No solution to show.\n')

    def submit(self):
        out_name = self.entry_out_name.get()
        if not out_name:
            out_name = 'outfiles'
        
        txt = str(self.entry_puzzle.get("1.0", tk.END))
        if self.read_file.get() == tk.TRUE:
            try:
                print('opening file:', txt)
                f = open(txt[:-1], 'r')
                txt = f.read()
                f.close()
            except:
                self.entry_errors.insert(tk.END, 'wrong file or path: ' + txt + '.\n')
                return
        
        puzzle = []
        for row in txt.split('\n'):
            row = row.replace(' ', '')
            if txt:
                try:
                    temp = []
                    for c in row:
                        val = int(c)
                        if 4 < val or val < 0:
                            self.entry_errors.insert(tk.END, 'Number is to large. It should be in <0;4>.\n')
                        else:
                            temp.append(int(c))
                    puzzle.append(temp)

                except ValueError:
                    self.entry_errors.insert(tk.END, 'No letters\n')
            
        while ([] in puzzle):
            puzzle.remove([])
        
        sizes = [len(row) for row in puzzle]
        sizes.append(len(puzzle))
        if len(set(sizes)) > 1:
            self.entry_errors.insert(tk.END, 'Wrong size of puzzle. It should look like square.\n')
            return

        print('puzzle', puzzle)

        self.solve(puzzle, out_name)
    
    def solve(self, puzzle: List[List[int]], filename: str):
        s = eSquaroSolverClass(filename)
        s.get_grid(puzzle)
        if s.solve_SAT():
            self.entry_errors.insert(tk.END, 'Puzzle is unsolveable.')
            return

        self.list_name = s.get_results_name()
        self.solution_count = len(self.list_name)
        print('there are solutions:' + str(self.solution_count))
        self.dump_out_path.delete(0, 'end')
        if len(self.list_name) > 1:
            self.dump_out_path.insert(tk.INSERT, self.list_name[0][:-5] + '*')
        else:
            self.dump_out_path.insert(tk.INSERT, self.list_name[0])

        self.list_img = []
        self.next()
        

root = tk.Tk()
root.title('asldkjk')
app = Application(root)
