import SATSolver

clauses = [[-1,3], [-2,-3], [2,3], [-1,2,-3], [1,3], [-2,3]]

print('Knowledge base is satisfiable:',SATSolver.testKb(clauses))
print('If we add Amy as a truth teller to the knowledge base: ', SATSolver.testLiteral(1,clauses))
print('If we add Bob as a truth teller to the knowledge base: ', SATSolver.testLiteral(2,clauses))
print('If we add Cal as a truth teller to the knowledge base: ', SATSolver.testLiteral(3,clauses))

clauses = [[-1,3], [-2,-3], [2,3], [-1,2,-3], [1,3], [-2,3], [3], [-2], [-1]]
print('Thus, we have the Cal is a truth-teller, and Amy and Bob are liars. We get the following when adding Cal, not Amy and not Bob to knowledge base: ', SATSolver.testKb(clauses))
