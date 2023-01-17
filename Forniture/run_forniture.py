from Forniture.forniture import PaniniSolver

p_solver = PaniniSolver()
print('Optimal Solution value', p_solver.get_obj_val())
print('Optimal Solution configuration')
p_solver.get_solution()


#print(evaluate_csv(csv_file_name))