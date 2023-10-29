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


class TimeoutCallback(cp_model.CpSolverSolutionCallback):
    def __init__(self, time_limit_seconds):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.time_limit_seconds = time_limit_seconds
        self.start_time = 0

    def on_solution_callback(self):
        if self.ObjectiveValue() == self.best_objective_value:
            # No improvement in the best solution.
            elapsed_time = time.time() - self.start_time
            if elapsed_time >= self.time_limit_seconds:
                self.StopSearch()
        else:
            # Update the best objective value and reset the timer.
            self.best_objective_value = self.ObjectiveValue()
            self.start_time = time.time()
