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


def str_compare(self) -> str:
    """Return the string representation of an ast.Compare node
    """

    return f'{self.left.__str__()} {self.ops[0].__str__()} {self.comparators[0].__str__()}'


ast.Compare.__str__ = str_compare


def str_expr(self) -> str:
    """Return the string representation of an ast.Expr node
    """

    return self.value.__str__()


ast.Expr.__str__ = str_expr


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
    if isinstance(self.value, str):
        return f'\"{self.value}\"'

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



def str_eq(self) -> str:
    """Return the string representation of a ast.Eq node
    """

    return 'is equal to'


ast.Eq.__str__ = str_eq


def str_neq(self) -> str:
    """Return the string representation of the ast.NotEq node
    """

    return 'is not equal to'


ast.NotEq.__str__ = str_neq


def str_lt(self) -> str:
    """Return the string representation of the ast.Lt node
    """

    return 'is less than'


ast.Lt.__str__ = str_lt


def str_lte(self) -> str:
    """Return the string representation of the ast.LtE node
    """

    return 'is less than or equal to'


ast.LtE.__str__ = str_lte


def str_gt(self) -> str:
    """Return the string representation of the ast.Gt node
    """

    return 'is greater than'


ast.Gt.__str__ = str_gt


def str_gte(self) -> str:
    """Return the string representation  of the ast.GtE node
    """

    return 'is greater than or equal to'


ast.GtE.__str__ = str_gte


def str_list(self) -> str:
    """Return the string representation of a ast.List
    """

    str_so_far = "["

    for elem in self.elts:
        str_so_far += f'{elem}, '

    str_so_far = str_so_far[0:-2] + "]"

    return str_so_far


ast.List.__str__ = str_list

if __name__ == '__main__':
    with open("test_program.py") as f:
        program = f.read()

    tree = ast.parse(program)
    print(tree)
