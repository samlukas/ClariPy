"""
CSC111 Winter 2023 Project: ClariPy

This module contains code that converts a given file and its contents into tokens that are
easily parsable. This allows us to more easily work with these tokens and the code written
to convert between pseudo code and python code

Also implemented is code that allows us to convert these tokens into their corresponding AST
nodes
"""

import re
import classes

"""
TOKENIZER 
"""

token_format = re.compile(r"[-+]?[0-9]*\.?[0-9]+|\w+|[\"\'][ -~]+[\"\']|!=|[<>]=|[<>+\-*/;{}(),\]\[]|=+")
string_format = re.compile(r"[\"\'][ -~]+[\"\']")
variable_format = re.compile(r"\w+")
int_format = re.compile(r"[-+]?[0-9]+")
float_format = re.compile(r"[-+]?[0-9]*\.[0-9]+")
KEYWORDS = {'Define', 'If', 'Else', 'as', 'and', 'or'}
PRECEDENCES = {'*': 1, '/': 1, '+': 0, '-': 0, '>=': -1, '>': -1, '<=': -1, '<': -1, '==': -1, '!=': -1, 'and': -2,
               'or': -2}
A_OPERATORS = {'*', '/', '+', '-'}
B_OPERATORS = {'and', 'or', '<', '<=', '>', '>=', '!=', '=='}


def tokenize(file_name: str) -> list[str]:
    """Return the tokenized version of the input program
    """
    with open(file_name) as f:
        program = f.read()

    program = program.replace("is equal to", "==")
    program = program.replace("is not equal to", "!=")
    program = program.replace("is greater than", ">")
    program = program.replace("is less than", "<")
    program = program.replace("is greater than or equal to", ">=")
    program = program.replace("is less than or equal to", "<=")

    return token_format.findall(program)


def lexer(tokens: list) -> list:
    """Return the list of tokens, replacing tokens of leaf nodes with appropriate nodes
    """
    tokens_so_far = []
    i = 0

    while i < len(tokens):
        if tokens[i] in KEYWORDS:
            tokens_so_far.append(tokens[i])
        elif re.fullmatch(float_format, tokens[i]):
            tokens_so_far.append(classes.Num(float(tokens[i])))
        elif re.fullmatch(int_format, tokens[i]):
            tokens_so_far.append(classes.Num(int(tokens[i])))
        elif re.fullmatch(string_format, tokens[i]):
            tokens_so_far.append(classes.Str(tokens[i][1:-1]))
        elif re.fullmatch(variable_format, tokens[i]):
            if i < len(tokens) - 1 and tokens[i + 1] == '[':
                end = matching_parenthesis(tokens, i + 1, '[')
                inner = lexer(tokens[i + 2:end])
                subscript = expression_to_ast(inner)  # Subscript must be a single expression
                tokens_so_far.append(classes.Subscript(classes.Name(tokens[i]), subscript))
                i = end
            else:
                tokens_so_far.append(classes.Name(tokens[i]))
        else:
            tokens_so_far.append(tokens[i])

        i += 1

    return tokens_so_far


def expression_to_ast(tokens: list) -> classes.BinOp | classes.BoolOp:
    """Return BinOp/BoolOp AST representation of the given expression
    """
    return polish_to_ast(shunting_yard(tokens))


def shunting_yard(tokens: list) -> list:
    """Return the tokens ordered in Reverse Polish Notation
    """
    operators = '+-*/>=<==!=()andor'  # While technically parentheses are not operators, this simplifies the checks

    operator_stack = []
    output = []

    for i in range(0, len(tokens)):
        if not isinstance(tokens[i], str) or tokens[i] not in operators:
            output.append(tokens[i])
        elif tokens[i] == '(':
            operator_stack.append(tokens[i])
        elif tokens[i] == ')':
            curr = operator_stack.pop()
            while curr != '(':
                output.append(curr)
                curr = operator_stack.pop()
        elif tokens[i] in operators:
            # UNOPTIMIZED VERSION (Restating the rules directly)
            # if not operator_stack or operator_stack[len(operator_stack) - 1] == ')':
            #     operator_stack.append(tokens[i])
            # elif PRECEDENCES[tokens[i]] > PRECEDENCES[operator_stack[len(operator_stack) - 1]]:
            #     operator_stack.append(tokens[i])
            # elif PRECEDENCES[tokens[i]] <= PRECEDENCES[operator_stack[len(operator_stack) - 1]]:
            #     output.append(operator_stack.pop())
            #     while (operator_stack and PRECEDENCES[operator_stack[len(operator_stack) - 1]] >=
            #       PRECEDENCES[tokens[i]]):
            #         output.append(operator_stack.pop())
            #     operator_stack.append(tokens[i])

            # OPTIMIZED VERSION (Might not work as well)
            while (operator_stack and operator_stack[len(operator_stack) - 1] != '(' and
                   PRECEDENCES[tokens[i]] <= PRECEDENCES[operator_stack[len(operator_stack) - 1]]):
                output.append(operator_stack.pop())

            operator_stack.append(tokens[i])

    while operator_stack:
        output.append(operator_stack.pop())
    return output


def polish_to_ast(polish: list) -> classes.BinOp | classes.BoolOp:
    """
    Converts reverse polish notation into ast.BinOp or ast.BoolOp class

    Preconditions:
        - all([(item in A_OPERATORS) or (item in B_OPERATORS) for item in polish if isinstance(item, str)])
    """

    stack = []

    for item in polish:
        if isinstance(item, classes.Expr):
            stack.append(item)
        else:
            val1, val2 = stack.pop(), stack.pop()
            if item in A_OPERATORS:
                stack.append(classes.BinOp(val1, item, val2))
            elif item in B_OPERATORS:
                stack.append(classes.BoolOp(item, val2, val1))

    return stack[0]


def matching_parenthesis(tokens: list, index: int,  p_type: str = '(') -> int:
    """
    Return the index of the matching parenthesis to the parenthesis at the given index
    If the tokens feature unmatched parentheses, raise SyntaxError

    Preconditions:
        - tokens[index] == p_type
    """
    if p_type == '{':
        closing = '}'
    elif p_type == '[':
        closing = ']'
    else:
        closing = ')'

    stack = []

    for i in range(index + 1, len(tokens)):
        if tokens[i] == p_type:
            stack.append(tokens[i])
        elif tokens[i] == closing:
            if not stack:
                return i
            stack.pop()

    raise SyntaxError  # Unmatched parenthesis


def parse_statements(tokens: list) -> list:
    """
    Parse the statments within the given list of tokens.
    Convert the statements into either classes.BoolOp or classes.BinOp
    """

    structure = []
    paren = {'{', '(', '['}
    i = 0

    while i < len(tokens):
        if tokens[i] in paren:
            end = matching_parenthesis(tokens, i, tokens[i])
            rpn = shunting_yard(tokens[i + 1: end])
            structure.append(polish_to_ast(rpn))

            i = end + 1
            
        else:
            structure.append(tokens[i])
            i += 1


    return structure

    