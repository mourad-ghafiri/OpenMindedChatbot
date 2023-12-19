import re
import math

def is_balanced(expression):
    stack = []
    for char in expression:
        if char == '(':
            stack.append(char)
        elif char == ')':
            if not stack or stack[-1] != '(':
                return False
            stack.pop()
    return len(stack) == 0


def format_math_expression(expression):
    if expression.lower() == "none":
        return ""
    # Regular expression pattern for valid characters and math functions
    pattern = r"[0-9\+\-\*\/\(\) ]|%|sin|cos|tan|log|sqrt|exp|abs|round"
    
    # Find all valid parts of the expression including math functions
    valid_parts = re.findall(pattern, expression, re.IGNORECASE)
    formatted_expression = ''.join(valid_parts)

    # Replace math function names with their equivalents in the math module
    math_functions = {
        'sin': 'math.sin', 'cos': 'math.cos', 'tan': 'math.tan', 
        'log': 'math.log', 'sqrt': 'math.sqrt', 'exp': 'math.exp', 
        'abs': 'abs', 'round': 'round'
    }
    for func in math_functions:
        formatted_expression = re.sub(r'\b' + func + r'\b', math_functions[func], formatted_expression)

    # Check for balanced parentheses
    if not is_balanced(formatted_expression):
        open_parentheses = formatted_expression.count('(')
        close_parentheses = formatted_expression.count(')')

        while open_parentheses > close_parentheses:
            formatted_expression += ')'
            close_parentheses += 1
        while close_parentheses > open_parentheses:
            formatted_expression = formatted_expression.replace(')', '', 1)
            close_parentheses -= 1

    return formatted_expression


def evaluate_math_expression(expression):
    if expression.lower() == "none":
        return ""
    print(f"the result of the expression : {expression} is {eval(format_math_expression(expression))}")
    return f"the result of the expression : {expression} is {eval(format_math_expression(expression))}"
