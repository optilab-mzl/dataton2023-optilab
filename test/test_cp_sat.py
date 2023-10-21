from ortools.sat.python import cp_model

model = cp_model.CpModel()
x = model.NewIntVar(0, 10, "")
two_to_the_x = model.NewIntVar(1, 2 ** 10, "")

precalculated = [2 ** i for i in range(11)]
model.AddElement(x, precalculated, two_to_the_x)

# test
model.Add(x == 3)

solver = cp_model.CpSolver()
solver.Solve(model)

print("x", solver.Value(x))
print("2**x", solver.Value(two_to_the_x))