"""
CSC111 Winter 2023 Project: ClariPy

Parsing and Tokenizing:

This module contains code that converts a given file and its contents into tokens that are
easily parsable. This allows us to more easily work with these tokens and the code written
to convert between pseudo code and python code

Also implemented is code that allows us to convert these tokens into their corresponding AST
nodes
"""
import re
import classes


KEYWORDS = {'Define', 'While', 'If', 'Else', 'as', 'and', 'or', 'Print'}
PRECEDENCES = {'*': 1, '/': 1, '%': 1, '+': 0, '-': 0, '>=': -1, '>': -1, '<=': -1, '<': -1, '==': -1, '!=': -1,
               'and': -2, 'or': -2}
A_OPERATORS = {'*', '/', '+', '-', '%'}
B_OPERATORS = {'and', 'or', '<', '<=', '>', '>=', '!=', '=='}


def parse_module(file_name: str) -> classes.Module:
    """Return the AST conversion of the given module
    """

    tokens = lexer(tokenize(file_name))
    statements = parse_statements(tokens)

    return classes.Module(statements)


def tokenize(file_name: str) -> list[str]:
    """Return the tokenized version of the input program
    """
    TOKEN_FORMAT = re.compile(r"-?[0-9]*\.?[0-9]+|\w+|[\"\'][ -~]+[\"\']|!=|[<>]=|[<>+\-*/;{}(),%\]\[]|=+")

    with open(file_name) as f:
        program = f.read()

    program = program.replace("is equal to", "==")
    program = program.replace("is not equal to", "!=")
    program = program.replace("is greater than or equal to", ">=")
    program = program.replace("is less than or equal to", "<=")
    program = program.replace("is greater than", ">")
    program = program.replace("is less than", "<")

    return TOKEN_FORMAT.findall(program)


def lexer(tokens: list) -> list:
    """Return the list of tokens, replacing tokens of leaf nodes with appropriate nodes
    """
    STRING_FORMAT = re.compile(r"[\"\'][ -~]+[\"\']")
    VARIABLE_FORMAT = re.compile(r"\w+")
    INT_FORMAT = re.compile(r"-?[0-9]+")
    FLOAT_FORMAT = re.compile(r"-?[0-9]*\.[0-9]+")
    tokens_so_far = []
    i = 0

    while i < len(tokens):
        if tokens[i] in KEYWORDS:
            tokens_so_far.append(tokens[i])
        elif re.fullmatch(FLOAT_FORMAT, tokens[i]):
            tokens_so_far.append(classes.Num(float(tokens[i])))
        elif re.fullmatch(INT_FORMAT, tokens[i]):
            tokens_so_far.append(classes.Num(int(tokens[i])))
        elif re.fullmatch(STRING_FORMAT, tokens[i]):
            tokens_so_far.append(classes.Str(tokens[i][1:-1]))
        elif re.fullmatch(VARIABLE_FORMAT, tokens[i]):
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
    operators = '+-*/%>=<==!=()andor'  # While technically parentheses are not operators, this simplifies the checks

    operator_stack = []
    output = []

    for token in tokens:
        if not isinstance(token, str) or token not in operators:
            output.append(token)
        elif token == '(':
            operator_stack.append(token)
        elif token == ')':
            curr = operator_stack.pop()
            while curr != '(':
                output.append(curr)
                curr = operator_stack.pop()
        elif token in operators:
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
            while (operator_stack and operator_stack[len(operator_stack) - 1] != '('
                    and PRECEDENCES[token] <= PRECEDENCES[operator_stack[len(operator_stack) - 1]]):
                output.append(operator_stack.pop())

            operator_stack.append(token)

    while operator_stack:
        output.append(operator_stack.pop())
    return output


def polish_to_ast(polish: list) -> classes.Expr:
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
                stack.append(classes.BinOp(val2, item, val1))
            elif item in B_OPERATORS:
                stack.append(classes.BoolOp(item, val2, val1))

    return stack[0]


def matching_parenthesis(tokens: list, index: int, p_type: str = '(') -> int:
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


def parse_if_statement(tokens: list, offset: int) -> tuple[classes.If, int]:
    """
    Return the If statement at the beginning of the list of tokens and index of the token after it
    """
    i = 0

    while i < len(tokens):
        i += 1
        if tokens[i] == '(':
            end = matching_parenthesis(tokens, i)
            condition = expression_to_ast(tokens[i + 1:end])
            i = end + 1
            if tokens[i] == '{':
                end = matching_parenthesis(tokens, i, '{')
                body = parse_statements(tokens[i + 1:end])
                i = end + 1
                if i < len(tokens) and tokens[i] == "Else":
                    i += 1
                    if tokens[i] == '{':
                        end = matching_parenthesis(tokens, i, '{')
                        orelse = parse_statements(tokens[i + 1:end])
                        return (classes.If(condition, body, orelse), end + 1 + offset)
                    else:
                        orelse, i = parse_if_statement(tokens[i:], i)
                        return (classes.If(condition, body, [orelse]), i + offset)
                else:
                    return (classes.If(condition, body), i + offset)
            else:
                raise SyntaxError
        else:
            raise SyntaxError


def parse_list(tokens: list, offset: int) -> tuple[classes.List, int]:
    """
    Return the AST representation of a list and the index of the token after it
    """
    list_so_far = []
    end = matching_parenthesis(tokens, 0, '[')
    i = 1

    expression = []

    while i <= end:
        if tokens[i] != ',' and tokens[i] != ']':
            if tokens[i] == '[':
                element, i = parse_list(tokens[i:], i)
                expression.append(element)
            else:
                expression.append(tokens[i])
                i += 1
        else:
            list_so_far.append(expression_to_ast(expression))
            expression = []
            i += 1

    return classes.List(list_so_far), offset + (end + 1)


def parse_statements(tokens: list) -> list:
    """
    Parse the statments within the given list of tokens.
    Convert the statements into either classes.BoolOp or classes.BinOp
    """

    statements = []
    i = 0

    while i < len(tokens):
        if tokens[i] == "While":
            i += 1
            if tokens[i] == '(':
                end = matching_parenthesis(tokens, i)
                condition = expression_to_ast(tokens[i + 1:end])
                i = end + 1
                if tokens[i] == '{':
                    end = matching_parenthesis(tokens, i, '{')
                    body = parse_statements(tokens[i + 1:end])
                    statements.append(classes.While(condition, body))
                    i = end + 1
                else:
                    raise SyntaxError
            else:
                raise SyntaxError

        elif tokens[i] == "If":
            statement, i = parse_if_statement(tokens[i:], i)
            statements.append(statement)

        elif tokens[i] == 'Define':
            i += 1
            if isinstance(tokens[i], (classes.Name, classes.Subscript)):
                target = tokens[i]
                i += 1
                if tokens[i] == 'as':
                    i += 1
                    if tokens[i] == '[':
                        expression, i = parse_list(tokens[i:], i)
                        if tokens[i] != ';':
                            raise SyntaxError
                        i += 1
                    else:
                        start = i
                        while tokens[i] != ';':
                            i += 1
                        expression = expression_to_ast(tokens[start:i])
                        i += 1
                    statements.append(classes.Assign(target, expression))
                else:
                    raise SyntaxError
            else:
                raise SyntaxError

        elif tokens[i] == 'Print':
            i += 1
            start = i
            while tokens[i] != ';':
                i += 1
            statements.append(classes.Print(expression_to_ast(tokens[start:i])))
            i += 1

    return statements


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'allowed-io': ['Print.evaluate', 'tokenize'],
        'extra-imports': ['classes', 're'],
        'disable': ['abstract-method', 'syntax-error']
    })
