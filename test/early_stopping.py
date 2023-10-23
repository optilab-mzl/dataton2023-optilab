from ortools.sat.python import cp_model

class SolutionPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, model, max_no_improvement):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.model = model
        self.max_no_improvement = max_no_improvement
        self.no_improvement_count = 0
        self.best_solution = None

    def on_solution_callback(self):
        current_solution = self.ObjectiveValue()
        
        # Check if the current solution is better than the best known solution
        if self.best_solution is None or current_solution < self.best_solution:
            self.best_solution = current_solution
            self.no_improvement_count = 0
        else:
            self.no_improvement_count += 1

        if self.no_improvement_count >= self.max_no_improvement:
            print(f"Terminating the solver after {self.no_improvement_count} iterations without improvement.")
            self.StopSearch()

def main():
    model = cp_model.CpModel()

    # Define your variables and constraints here

    solver = cp_model.CpSolver()
    
    max_no_improvement = 100  # Adjust the number of iterations without improvement as needed

    solution_printer = SolutionPrinter(model, max_no_improvement)
    status = solver.SolveWithSolutionCallback(model, solution_printer)

    if status == cp_model.OPTIMAL:
        print("Optimal solution found.")
    elif status == cp_model.FEASIBLE:
        print("Feasible solution found.")
    elif status == cp_model.INFEASIBLE:
        print("No solution exists.")
    elif status == cp_model.MODEL_INVALID:
        print("Invalid model.")
    else:
        print("Solver ran to completion without finding a solution.")

if __name__ == "__main__":
    main()
