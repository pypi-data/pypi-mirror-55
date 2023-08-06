import math

class Arr:
    def __init__(self, cont):
        self.cont = cont
    def __add__(self, other):
        self.new_arr = []
        if len(self.cont) == len(other.cont):
            for i in self.cont:
                self.new_arr.append(i)
            for j in range(len(other.cont)):
                self.new_arr[j] += other.cont[j]
            return self.new_arr
        else:
            return "Yet developing..."


