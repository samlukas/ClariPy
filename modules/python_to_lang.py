import ast


def str_module(self) -> str:
    """Return the string representation of a ast.Module node
    """

    str_so_far = ''

    for obj in self.body:
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

if __name__ == '__main__':
    with open("test_program.py") as f:
        program = f.read()

    tree = ast.parse(program)
    print(tree)
