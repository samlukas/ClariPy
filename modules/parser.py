import re

"""
TOKENIZER 
"""

tokens = re.compile(r"\w+|\"[ -~]+\"|\'[ -~]+\'|!=|[<>]=|[<>+\-*/;{}()]|=+")


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

    return tokens.findall(program)
