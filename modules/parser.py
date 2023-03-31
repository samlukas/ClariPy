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

token_format = re.compile(r"[-+]?[0-9]*\.?[0-9]+|\w+|[\"\'][ -~]+[\"\']|!=|[<>]=|[<>+\-*/;{}()]|=+")
string_format = re.compile(r"[\"\'][ -~]+[\"\']")
variable_format = re.compile(r"\w+")
int_format = re.compile(r"[-+]?[0-9]+")
float_format = re.compile(r"[-+]?[0-9]*\.[0-9]+")
KEYWORDS = {'Define', 'If', 'Else', 'as'}
PRECEDENCES = {'*': 1, '/': 1, '+': 0, '-': 0}
OPERATORS = {'*', '/', '+', '-'}


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


def lexer(tokens: list) -> None:
    """Mutate the list of tokens to replace tokens of leaf nodes with appropriate nodes
    """

    for i in range(0, len(tokens)):
        if tokens[i] in KEYWORDS:
            continue
        if re.fullmatch(float_format, tokens[i]):
            tokens[i] = classes.Num(float(tokens[i]))
        elif re.fullmatch(int_format, tokens[i]):
            tokens[i] = classes.Num(int(tokens[i]))
        elif re.fullmatch(string_format, tokens[i]):
            tokens[i] = classes.Str(tokens[i][1:-1])
        elif re.fullmatch(variable_format, tokens[i]):
            tokens[i] = classes.Name(tokens[i])


def shunting_yard(tokens: list) -> list:
    """Return the tokens ordered in Reverse Polish Notation
    """
    operators = '+-*/()'  # While technically parentheses are not operators, this simplifies the checks

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


def polish_to_ast(polish: list) -> classes.BinOp:
    """
    Converts reverse polish notation into ast.BinOp class

    Preconditions:
        - all(item in OPERATORS for item in polish if isinstance(item, str))
    """

    stack = []

    for item in polish:
        if isinstance(item, classes.Expr):
            stack.append(item)
        else:
            val1, val2 = stack.pop(), stack.pop()
            if item in OPERATORS:
                stack.append(classes.BinOp(val1, item, val2))

    return stack[0]