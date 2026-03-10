# Basic Propositional Logic Problem Solver


# Importing necessary libraries
import itertools
import random
import string


#Node class for binary tree
class TreeNode:
    #constructor
    def __init__(self, data, right=None, left=None):
        self.data = data
        self.left = left
        self.right = right
    #print tree for testing
    def print_tree(self, level=0):
       if self.data is not None:
            print("  " * level + str(self.data[0]))  # Indentation for levels
            if self.left:
                self.left.print_tree(level + 1)  # Print left subtree
            if self.right:
                self.right.print_tree(level + 1)  # Print right subtree


     #traverse through
    def getLeaves(self):
       if self.left is None and self.right is None:
          return [self.data[0].replace('¬', '')], [self]
       data_list = []
       leaf_list = []
       if self.left:
        left_data, left_nodes = self.left.getLeaves()
        data_list.extend(left_data)
        leaf_list.extend(left_nodes)

       if self.right:
        right_data, right_nodes = self.right.getLeaves()
        data_list.extend(right_data)
        leaf_list.extend(right_nodes)

       return data_list, leaf_list

    #returns true if node is a left leaf in the tree
    def isLeft(self, root):
        data, leafList = root.left.getLeaves()
        if self in leafList:
          return True
        else:
          return False


# Set of operators and variables - supports up to 4 parts
operators = ['→', '∨', '∧']
variables = ['A', 'B', 'C']

# Parser to tokenize and handle logical operators
def parse_expression(expression, vars):
#assume each sentence contains three parts
    #supports AND (∧), OR (∨), NOT (¬), IMPLIES (→) for now
    indices = [0]*10
    count = 1
    parentheses = [0]*4
    p=0
    labels = {'A': ' ', 'B': ' ', 'C': ' '}

    expr = expression.split()
    if expr[0] == "For" and expr[1] == "all" and expr[2] == "x,":
      expr = expr[3:]
      expression = expression.replace("For all x,", "∀x,")
    elif expr[0] == "There" and expr[1] == "exists" and expr[2] == "an" and expr[3] == "x" and expr[4] == "such" and expr[5] == "that":
      expr = expr[6:]
      expression = expression.replace("There exists an x such that", "∃x,")
    #loop through words of expression to convert to variables
    for i, w in enumerate(expr):
        if w == "implies" or w == "or" or w=="and" or i == len(expr)-1:
            indices[count] = i+1
            if i == len(expr)-1:
              ex = ' '.join(expr[indices[count-1]:indices[count]])
            else:
              ex = ' '.join(expr[indices[count-1]:indices[count]-1])
            labels[vars[count-1]] = ex
            if ex.__contains__('not'):
              expression = expression.replace(ex, '¬' + vars[count-1])
            else:
             expression = expression.replace(ex, vars[count-1])
            count = count+1

    exIndex1 = 0
    exIndex2 = 0

    #account for parentheses
    for k, v in labels.items():
        if "(" in v:
            for e in expression:
              if e == k and expression[exIndex1-1] == '¬':
                expression = expression[:exIndex1-1] + "(" + expression[exIndex1-1:]
              elif e == k:
                expression = expression[:exIndex1] + "(" + expression[exIndex1:]
              exIndex1 = exIndex1+1
        if ")" in v:
            for e in expression:
              if e == k:
                expression = expression[:exIndex2+1] + ")" + expression[exIndex2+1:]
              exIndex2 = exIndex2+1

    #replace operator words with symbols
    expression = expression.replace('and', '∧').replace('or', '∨').replace('implies', '→')
    return expression, labels


#creates a binary tree using a parsed expression
def make_tree(parsed_expression, labels):

    #if empty, return
    if not parsed_expression:
      return TreeNode(None)

    parsed_expression = parsed_expression.replace('∃x,', '').replace('∀x,', '')
    #if the whole expression is enclosed by parentheses, return only what's within
    if parsed_expression[0] == '(' and parsed_expression[-1] == ')' and len(parsed_expression)>1:
        return make_tree(parsed_expression[1:-1], labels)


    #if the expression is only a variable, create leaf node
    if len(parsed_expression) <= 2:
      for v in variables:
        if v in parsed_expression:
          if '¬' in parsed_expression:
            vList = ['¬' + v, labels[v]]
            return TreeNode(data=vList)
          else:
           vList = [v,labels[v] ]
           return TreeNode(data=vList)


    #loop which traverses the whole expression by each operator and recusrsively builds the tree
    for o in operators:
      depth = 0
      for p in range(len(parsed_expression) -1, -1, -1):
          c = parsed_expression[p]
          #test for parentheses/precedence
          if c == ')': depth +=1
          elif c == '(': depth -=1
          elif depth == 0 and c == o:
              left = make_tree(parsed_expression[:p-1], labels )
              right = make_tree(parsed_expression[p+2:], labels)
              node1 =TreeNode(c, right, left)
              return node1




# Function to generate the truth table for a given expression
def generate_truth_table(expression, variables):
    # Create a list of all possible truth values for the variable
    truth_values = list(itertools.product([False, True], repeat=len(variables)))

    expression = expression.replace('∃x,', '').replace('∀x,', '')
    table = []
    for values in truth_values:
        assignment = dict(zip(variables, values))
        truth_value = evaluate_expression(expression, assignment)
        table.append((assignment, truth_value))

    return table


# Function to evaluate the expression given the truth values of the variables
def evaluate_expression(expression, assignment):
    # Replace the variables in the expression with their corresponding truth values
    expression = expression.replace('∃x,', '').replace('∀x,', '')
    for var, value in assignment.items():
        expression = expression.replace(var, str(value))


    # Evaluate the logical expression using Python's eval (with safety checks)
    try:
        return eval_expression(expression)
    except:
        return "Error in evaluation"


# Evaluate logical expressions
def eval_expression(expression):
    # Implement basic logical operations here
    expression = expression.replace('¬', 'not ')  # NOT
    expression = expression.replace('∧', ' and ')  # AND
    expression = expression.replace('∨', ' or ')   # OR
    expression = expression.replace('→', ' <= ')  # IMPLIES (A → B is equivalent to not A or B)
    return eval(expression)


# Check if a statement is a tautology (always true), contradiction (always false), or contingency (sometimes true)
def check_validity(truth_table):
    all_true = all(truth for _, truth in truth_table)
    all_false = all(not truth for _, truth in truth_table)


    if all_true:
        return "Tautology (Always True)"
    elif all_false:
        return "Contradiction (Always False)"
    else:
        return "Contingency (Sometimes True)"


#negates a logical expression
def negateExpression(pExpr):
  pExpr = pExpr.replace("(", "( ").replace(")", " )")
  ex = pExpr.split()
  negated = ""
  for e in ex:
    if e in variables:
      if '¬' not in e:
        negated += '¬' + e + ' '
      else:
        negated += e.replace('¬', '')
    if e == '(':
      negated += '('
    if e == ')':
      negated += ')'
    if e == '→':
      negated += '∧ '
    if e == '∧':
      negated += '∨ '
    if e == '∨':
      negated += '∧ '
    if e == '∃x,':
      negated += '∀x, '
    if e == '∀x,':
      negated += '∃x, '
  return negated

#uses truth tables to determine validity
def findArgumentValidity(ex_table, prem_table, concl_table):
  matches = False
  valid = False
  for eAssignment, eTruthValue in ex_table:
    for pAssignment, pTruthValue in prem_table:
      for p in pAssignment:
          if pAssignment[p] == eAssignment[p]:
            matches = True
          else:
           matches = False
           break
      if matches == True:
        break
    for cAssignment, cTruthValue in concl_table:
      for c in cAssignment:
         if cAssignment[c] == eAssignment[c]:
            matches = True
         else:
           matches = False
           break
      if matches == True:
        break

    if matches == True and pTruthValue == True and eTruthValue == True and cTruthValue == False:
        return False
  return True


#for extra credit modular arithmetic proofs
def modularProof(a, b, c, d, m):
  if (a-b)%m == 0 and (c-d)%m == 0:
    print(f"Yes, {a} - {b} is divisible by {m} and {c} - {d} is divisble by {m}")
    return ((a+c) - (b+d))%m == 0
  else:
    print(f"Either {a} - {b} is not divisible by {m} or {c} - {d} is not divisble by {m}, or both")
    return False


#runs program
def runProgram(expression, premise, conclusion, num, num2):
  #print expressions
  print("\nConditional statement/premise 1: " + expression.replace("(", "").replace(")", ""))
  print("Premise 2: " + premise)
  print("Conclusion 2: " + conclusion)

  print("\nWe parse the expression and create a tree and truth tables:")

  parsed_expression, labels = parse_expression(expression, variables)
  node= make_tree(parsed_expression, labels)

  print(f"The first premise parsed is {parsed_expression}")
  print("The tree for the expression is:")
  node.print_tree()
  i = 0
  for e in parsed_expression:
      if e == '→':
        left = parsed_expression[:i]
        right = parsed_expression[i+1:]
      i= i+1


  if num == 1:
    leftVars, leftLeaf = node.left.getLeaves()
    rightVars, rightLeaf = node.right.getLeaves()
    truth_table_left = generate_truth_table(left, leftVars)
    truth_table_right = generate_truth_table(right, rightVars)
  if num == 2:
    leftVars, leftLeaf = node.right.getLeaves()
    rightVars, rightLeaf = node.left.getLeaves()
    truth_table_left = generate_truth_table(right, leftVars)
    truth_table_right = generate_truth_table(left, rightVars)

  prem_pe, prem_labels = parse_expression(premise, leftVars)
  concl_pe, concl_labels = parse_expression(conclusion, rightVars)
  prem_tree = make_tree(prem_pe, prem_labels)
  concl_tree = make_tree(concl_pe, concl_labels)
  pVars, pLeaf = prem_tree.getLeaves()
  cVars, cLeaf = concl_tree.getLeaves()


  #make truth tables
  vars, leaf = node.getLeaves()

  truth_table = generate_truth_table(parsed_expression, vars)
  prem_table = generate_truth_table(prem_pe, pVars)
  concl_table = generate_truth_table(concl_pe, cVars)

   # Print the truth table
  print("\nTruth Table for Premise 1:")
  left_truth_values = []
  right_truth_values = []
  i = 0
  leftTemp = ""
  rightTemp = ""
    #traverse main table
  for assignment1, truth_value1 in truth_table:
        #traverse left table and get values
      if num ==1:
       for assignment2, truth_value2 in truth_table_left:
        if len(left.replace(" ", "")) <=2:
          left_truth_values.append(' ')
          leftTemp = ""
        elif len(left) <= 6:
         left_truth_values.append(truth_value2)
         left_truth_values.append(truth_value2)
         left_truth_values.append(truth_value2)
         left_truth_values.append(truth_value2)
         leftTemp = left + ":"
        else:
          left_truth_values.append(truth_value2)
          left_truth_values.append(truth_value2)
          leftTemp = left + ":"


        #traverse right table and get values
       for assignment3, truth_value3 in truth_table_right:
        if len(right.replace(" ", "")) <=2:
          right_truth_values.append(' ')
          rightTemp = ""
        else:
          right_truth_values.append(truth_value3)
          rightTemp = right + ":"

      elif num == 2:
        for assignment2, truth_value2 in truth_table_right:
         if len(left.replace(" ", "")) <=2:
          left_truth_values.append(' ')
          leftTemp = ""
         elif len(left) <= 6:
           left_truth_values.append(truth_value2)
           left_truth_values.append(truth_value2)
           left_truth_values.append(truth_value2)
           left_truth_values.append(truth_value2)
           leftTemp = left +":"
         else:
           left_truth_values.append(truth_value2)
           left_truth_values.append(truth_value2)
           leftTemp = left + ":"


        #traverse right table and get values
        for assignment3, truth_value3 in truth_table_left:
         if len(right.replace(" ", "")) <=2:
          right_truth_values.append(' ')
          rightTemp = ""
         else:
          right_truth_values.append(truth_value3)
          rightTemp = right + ":"


       #print table
      print(f"Expression: {parsed_expression} | Variables: {assignment1} |{leftTemp} {left_truth_values[i]}|{rightTemp} {right_truth_values[i]}| Truth Value: {truth_value1}")
      i=i+1

  print("\nTruth Table for Premise 2:")
  for assignment, truth_value in prem_table:
        print(f"Expression: {prem_pe} | Variables: {assignment} | Truth Value: {truth_value}")

  print("\nTruth Table for Conclusion:")
  for assignment, truth_value in concl_table:
          print(f"Expression:  {concl_pe} | Variables: {assignment} | Truth Value: {truth_value}")


    # Check the validity of the expression
  validity = check_validity(truth_table)
  print(f"\nThe expression is a: {validity}")

  option = False
  print("Using the tables, we can deduce the validity of the entire argument - it is invalid only if both premises are \ntrue and the conclusion is false")
  valid = findArgumentValidity(truth_table, prem_table, concl_table)
  if valid == True:
    if prem_pe in negateExpression(right):
      print("Argument is valid by modus tollens")
      option = True
    elif prem_pe in left:
      if num2 ==1:
        print("Argument is valid by modus ponens")
        option = True
      elif num2==2:
         print("Argument is valid by universal modus ponens / instantiation")
         option = True
  elif valid == False:
    if prem_pe in negateExpression(left):
      print("Argument is invalid by inverse error")
      option = True
    elif prem_pe in right:
      print("Argument is invalid by converse error")
      option = True
  if option == False:
    print("Argument is invalid")


# Example: Propositional Logic Problem Solver
def main():

    print("This program is called ValidityProver and acts as a theorem parser and validity checker.\nIt evaluates different types of arguments and assesses both their validity and \nthe type of argument or error that might be present. It does this by logically parsing \nthe expressions, creating a binary tree to represent them, and providing a truth table for each one.")
    print("Each statement is written using the word 'implies' but the statement can also be expressed in if-then form.")
    # Modus ponens example - include paretheses to indicate priority
    print("\nExample 1:")
    modusPonensP1 = "Giving a mouse a cookie implies (he will ask for milk and get sick)"
    modusPonensP2 = "I gave the mouse a cookie"
    modusPonensConcl = "He will ask for milk and get sick"
    runProgram(modusPonensP1, modusPonensP2, modusPonensConcl, 1, 1)

    #modus tollens example
    print("\nExample 2:")
    modusTollensP1 = "(Sarah laying in the sun and getting tan) implies she is happy"
    modusTollensP2 = "She is not happy"
    modusTollensConcl = "Sarah does not lay in the sun or does not get tan"
    runProgram(modusTollensP1, modusTollensP2, modusTollensConcl, 2, 1)

    #inverse error example
    print("\nExample 3:")
    converseP1 = "Riding the train implies (you have a car or you do not have a bike)"
    converseP2 = "You have a car"
    converseConcl = "You ride the train"
    runProgram(converseP1, converseP2, converseConcl, 2, 1)


    #converse error example
    print("\nExample 4:")
    inverseP1 = "The student being in the library implies (they are not doing well in class and need a tutor)"
    inverseP2 = "The student is not in the library"
    inverseConcl = "They are doing well in class and do not need a tutor"
    runProgram(inverseP1, inverseP2, inverseConcl, 1, 1)


    #Quantified statement example
    print("\nExample 5:")
    quantifyP1 = "For all x, x being > 0 implies that it is a natural number"
    quantifyP2 = "7 is > 0"
    quantifyConcl = "7 is a natural number"
    runProgram(quantifyP1, quantifyP2, quantifyConcl, 1, 2)


    #Modular arithmetic proofs example
    print("\nExample 6:")
    modularP1 = "a ≡ b mod m and c ≡ d mod m implies a + c ≡ b + d mod m"
    modularP2 = "6 ≡ 2 mod 4 and 3 ≡ 7 mod 4"
    modularConcl = "4 + 3 ≡ 2 + 7 (mod 4)"
    print("The statement below means that if (a-b) % m is equal to zero and if (c-d) % m is equal to 0, then ((a+c)-(b+d)) % m equals 0")
    print("That is, they are divisible by m")
    runProgram(modularP1, modularP2, modularConcl, 1, 2)
    print("\nBut we must check if it is true for the given values: ")
    isValid = modularProof(6, 2, 3, 7, 4)


    #negation demonstration
    print("\nExample 7: ")
    print("Demonstration of negation of conditional quantified statement: ")
    statement = "There exists an x such that multiplying by 10 implies (x will equal 120 and be divisible by 3)"
    parsed_statement, sLabels = parse_expression(statement, variables)
    print("Statement: " + statement.replace("(", "").replace(")", ""))
    print("Parsed, this statement is " + parsed_statement)
    negated_statement = negateExpression(parsed_statement)
    print("Negated, the statement becomes " +negated_statement)

    #tautology example
    print("\nExample 8: ")
    print("Demonstration of a tautology:")
    tautology = "I go to the store or I do not go to the store"
    parsed_tautology, tLabels = parse_expression(tautology, ['A', 'A'])
    print("Statement: " + tautology.replace("(", "").replace(")", ""))
    print("Parsed, this statement is " + parsed_tautology)
    tautology_table = generate_truth_table(parsed_tautology, ['A', 'A'])
    print("Truth table:")
    for assignment, truth_value in tautology_table:
        print(f"Variables: {assignment} | Truth Value: {truth_value}")
    print("This statement is a " + check_validity(tautology_table))

    #contradiction example
    print("\nExample 9: ")
    print("Demonstration of a contradiction:")
    contradiction = "Tonight I ate dinner and I did not eat dinner"
    parsed_contradiction, cLabels = parse_expression(contradiction, ['A', 'A'])
    print("Statement: " + contradiction.replace("(", "").replace(")", ""))
    print("Parsed, this statement is " + parsed_contradiction)
    contradiction_table = generate_truth_table(parsed_contradiction, ['A', 'A'])
    print("Truth table:")
    for assignment, truth_value in contradiction_table:
        print(f"Variables: {assignment} | Truth Value: {truth_value}")
    print("This statement is a " + check_validity(contradiction_table))


# Run the main function to test the problem solver
if __name__ == "__main__":
    main()











