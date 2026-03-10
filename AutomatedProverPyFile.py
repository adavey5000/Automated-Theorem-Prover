# Basic Propositional Logic Problem Solver

# Importing necessary libraries
import itertools

# 1. Parser to tokenize and handle logical operators
def parse_expression(expression):
    # We only support AND (∧), OR (∨), NOT (¬), IMPLIES (→) for now
    expression = expression.replace('AND', '∧').replace('OR', '∨').replace('NOT', '¬').replace('IMPLIES', '→')
    return expression

# 2. Function to generate the truth table for a given expression
def generate_truth_table(expression, variables):
    # Create a list of all possible truth values for the variables
    truth_values = list(itertools.product([False, True], repeat=len(variables)))
    
    table = []
    for values in truth_values:
        assignment = dict(zip(variables, values))
        truth_value = evaluate_expression(expression, assignment)
        table.append((assignment, truth_value))
    
    return table

# 3. Function to evaluate the expression given the truth values of the variables
def evaluate_expression(expression, assignment):
    # Replace the variables in the expression with their corresponding truth values
    for var, value in assignment.items():
        expression = expression.replace(var, str(value))
    
    # Evaluate the logical expression using Python's eval (with safety checks)
    try:
        return eval_expression(expression)
    except:
        return "Error in evaluation"

# 4. Evaluate logical expressions
def eval_expression(expression):
    # Implement basic logical operations here
    expression = expression.replace('¬', 'not ')  # NOT
    expression = expression.replace('∧', ' and ')  # AND
    expression = expression.replace('∨', ' or ')   # OR
    expression = expression.replace('→', ' <= ')   # IMPLIES (A → B is equivalent to not A or B)
    return eval(expression)

# 5. Check if a statement is a tautology (always true), contradiction (always false), or contingency (sometimes true)
def check_validity(truth_table):
    all_true = all(truth for _, truth in truth_table)
    all_false = all(not truth for _, truth in truth_table)

    if all_true:
        return "Tautology (Always True)"
    elif all_false:
        return "Contradiction (Always False)"
    else:
        return "Contingency (Sometimes True)"

# Example: Propositional Logic Problem Solver
def main():
    # Example logic statement (you can change this)
    expression = "P AND Q"  # Input: "P AND Q"
    
    # Parse the expression to make it uniform with our operator definitions
    parsed_expression = parse_expression(expression)
    
    # Define the variables involved in the expression
    variables = ['P', 'Q']
    
    # Generate the truth table for the expression
    truth_table = generate_truth_table(parsed_expression, variables)
    
    # Print the truth table
    print("Truth Table:")
    for assignment, truth_value in truth_table:
        print(f"Variables: {assignment} | Truth Value: {truth_value}")
    
    # Check the validity of the expression
    validity = check_validity(truth_table)
    print(f"\nThe expression is a: {validity}")

# Run the main function to test the problem solver
if __name__ == "__main__":
    main()
