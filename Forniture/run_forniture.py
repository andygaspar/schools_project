from Forniture.forniture import PaniniSolver

p_solver = PaniniSolver()
print('Unita\' minime rimaste', p_solver.get_obj_val())
print('Assegnazione alle scuole: ')
p_solver.get_solution()


#csv_file_name='Forniture/sol_template.csv'

#print('quantità avanzata', p_solver.evaluate_csv(csv_file_name))