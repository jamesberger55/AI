import SATSolver

clauses = [[-1,3], [-2,-3], [2,3], [-1,2,-3], [1,3], [-2,3]]

print('Is the Knowledge Base satisfiable? (True/False):',SATSolver.testKb(clauses))
print('If we assume that Amy is a truth teller and add her to the knowledge base: ', SATSolver.testLiteral(1,clauses))
print('If we assume that Bob is a truth teller and add him to the knowledge base: ', SATSolver.testLiteral(2,clauses))
print('If we assume that Cal is a truth teller and add him to the knowledge base: ', SATSolver.testLiteral(3,clauses))

clauses = [[-1,3], [-2,-3], [2,3], [-1,2,-3], [1,3], [-2,3], [3], [-2], [-1]]
print('Therefore, we have shown that Cal is a truth-teller, and Amy and Bob are liars. We got to this conclusion when we added Cal as a truth teller, and not Amy, and not Bob to knowledge base: ', SATSolver.testKb(clauses))
