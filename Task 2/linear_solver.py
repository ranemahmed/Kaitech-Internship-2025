import numpy as np

class linear_Equation_Solver:
    def __init__(self, coefficients, constants):
        self._A = np.array(coefficients) 
        self._B = np.array(constants)     

    def solve(self):
        raise NotImplementedError

class Numpy_Linear_Equation_Solver(linear_Equation_Solver):
    def solve(self):
        try:
            solution = np.linalg.solve(self._A, self._B)
            return solution
        except np.linalg.LinAlgError as e:
            return f"Error! Equations doesn't have a solution: {e}"

class EquationSystem:
    def __init__(self):
        # 2x + 3y + z = 1
        # 4x + y + 2z = 2
        # 3x + 2y + 3z = 3
        self.coefficients = [
            [2, 3, 1],
            [4, 1, 2],
            [3, 2, 3]
        ]
        self.constants = [1, 2, 3]
        self.solver = Numpy_Linear_Equation_Solver(self.coefficients, self.constants)

    def display_solution(self):
        solution = self.solver.solve()
        
        print("The solution is: ")
        if isinstance(solution, str):
            print(solution)
        else:
            print(f"x = {solution[0]:.4f}")
            print(f"y = {solution[1]:.4f}")
            print(f"z = {solution[2]:.4f}")

if __name__ == "__main__":
    system = EquationSystem()
    system.display_solution()