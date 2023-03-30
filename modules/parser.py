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
