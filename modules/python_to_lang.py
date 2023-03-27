import ast


def str_module(self) -> str:
    """Return the string representation of a ast.Module node
    """

    str_so_far = ''

    for obj in self.body:
        if isinstance(obj, ast.If) or isinstance(obj, ast.While):
            str_so_far += (obj.__str__() + '\n')
        else:
            str_so_far += (obj.__str__() + ';\n')

    return str_so_far


ast.Module.__str__ = str_module


def str_assign(self) -> str:
    """Return the string representation of an ast.Assign node

    Preconditions:
        - the assignment is not parallel
    """
    return f'Define {self.targets[0]} as {self.value}'


ast.Assign.__str__ = str_assign


def str_name(self) -> str:
    """Return the string representation of a ast.Name node
    """

    return f'{self.id}'


ast.Name.__str__ = str_name


def str_constant(self) -> str:
    """Return the string representation of a ast.Constant node
    """

    return f'{self.value}'


ast.Constant.__str__ = str_constant


def str_binop(self) -> str:
    """Return the string representation of a ast.BinOp node
    """

    return f'({self.left} {self.op} {self.right})'


ast.BinOp.__str__ = str_binop


def str_add(self) -> str:
    """Return the string representation of a ast.Add node
    """

    return '+'


ast.Add.__str__ = str_add


def str_mult(self) -> str:
    """Return the string representation of a ast.Mult node
    """

    return '*'


ast.Mult.__str__ = str_mult


def str_div(self) -> str:
    """Return the string representation of a ast.Div node
    """

    return '/'


ast.Div.__str__ = str_div


def str_sub(self) -> str:
    """Return the string representation of a ast.Sub node
    """

    return '-'


ast.Sub.__str__ = str_sub


def str_if(self) -> str:
    """Return the string representation of a ast.If node
    """
    str_so_far = f'If ({self.test}) {{\n'

    for statement in self.body:
        str_so_far += f'\t{statement};\n'

    str_so_far += "}\n"

    if self.orelse:
        if isinstance(self.orelse[0], ast.If):
            str_so_far += f"Else {self.orelse[0]}"
        else:
            str_so_far += 'Else {\n'
            for statement in self.orelse:
                str_so_far += f'\t{statement};\n'
            str_so_far += "}"

    return str_so_far


ast.If.__str__ = str_if


def str_while(self) -> str:
    """Return the string representation of a ast.While node
    """
    str_so_far = f'While ({self.test}) {{\n'

    for statement in self.body:
        str_so_far += f'\t{statement};\n'

    str_so_far += "}\n"

    return str_so_far


ast.While.__str__ = str_while


if __name__ == '__main__':
    with open("test_program.py") as f:
        program = f.read()

    tree = ast.parse(program)
    print(tree)
