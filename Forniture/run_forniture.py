from Forniture.forniture import PaniniSolver

p_solver = PaniniSolver()
print('Optimal Solution value', p_solver.get_obj_val())
print('Optimal Solution configuration')
p_solver.get_solution()


#csv_file_name='Forniture/sol_template.csv'

#print('quantità avanzata', p_solver.evaluate_csv(csv_file_name))