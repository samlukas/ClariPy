"""
CSC111 Winter 2023 Project: ClariPy

This module contains code that could be used to represent a various parts that are
commonly found in python program.

This includes classes such as Statements, Expresisons, Num literals, String literals,
Binary operations, and Assignment statements
"""


from typing import Any

class Statement:
    def evaluate(self, env: dict[str: Any]) -> Any:
        """Evaluate the statement with the given environment"""

        raise NotImplementedError


class Expr(Statement):
    def evaluate(self, env: dict[str: Any]) -> Any:
        """Evaluate the statement with the given environment"""

        raise NotImplementedError


class Num(Expr):
    """Numeric literal
    """

    n: int | float

    def __init__(self, number: int | float) -> None:
        """Initialize a new numeric literal"""

        self.n = number

    def evaluate(self, env: dict[str: Any]) -> Any:
        """Evaluate the given numeric literal"""

        return self.n

    def __str__(self) -> str:

        return f"Num({self.n})"


class Str(Expr):
    """String literal
    """

    s: str

    def __init__(self, string: str) -> None:
        """Initialize a new string literal"""

        self.s = string

    def evaluate(self, env: dict[str: Any]) -> Any:
        """Evaluate the given string literal"""

        return self.s

    def __str__(self) -> str:
        return f"Str(\"{self.s}\")"


class Name(Expr):
    """Variable expression
    """

    id: str

    def __init__(self, id_: str) -> None:
        """Initialize a new variable expression"""

        self.id = id_

    def evaluate(self, env: dict[str: Any]) -> Any:
        """See if the given id is in env, if it is, return associated value, else raise NameError"""

        if self.id in env:
            return env[self.id]
        else:
            raise NameError

    def __str__(self) -> str:
        return f"Name({self.id})"


class List(Expr):
    """List literal
    """

    lst: list

    def __init__(self, lst: list) -> None:
        """Initialize a new list litereal"""

        self.lst = lst

    def evaluate(self, env: dict[str: Any]) -> Any:
        """Evaluate the given list literal"""

        return self.lst

    def __getitem__(self, i: int) -> Any:
        """Get the item stored at a specific index in the list"""

        if i >= len(self.lst):
            raise IndexError
        else:
            return self.lst[i]


class Subscript(Expr):
    """List indexing
    """

    lst: Name
    index: Expr

    def __init__(self, lst: Name, index: Expr) -> None:
        """Initialize a new indexing operation"""

        self.lst = lst
        self.index = index

    def evaluate(self, env: dict[str: Any]) -> Any:
        """Evaluate a new indexing operation"""

        i = self.index.evaluate(env)

        if i >= len(self.lst.evaluate(env)):
            raise IndexError
        else:
            return self.lst.evaluate(env)[i].evaluate(env)


class Bool(Expr):
    """Boolean literal
    """

    b: bool

    def __init__(self, b: bool) -> None:
        """Initialize a new string literal"""

        self.b = b

    def evaluate(self, env: dict[str: Any]) -> Any:
        """Evaluate the given bool literal"""

        return self.b

    def __str__(self) -> str:
        return f"Bool(\"{self.b}\)"


class BoolOp(Expr):
    """Represents a bool operation
    """

    op: str
    right: Expr
    left: Expr

    def __init__(self, op: str, left: Expr, right: Expr) -> None:
        """Initialize a new binary operation"""

        self.op = op
        self.right = right
        self.left = left

    def evaluate(self, env: dict[str: Any]) -> Any:
        """Evaluate the given bool operation"""

        right_val = self.right.evaluate(env)
        left_val = self.left.evaluate(env)

        if self.op == 'and':
            return right_val and left_val
        elif self.op == 'or':
            return right_val or left_val
        elif self.op == '<':
            return left_val < right_val
        elif self.op == '<=':
            return left_val <= right_val
        elif self.op == '>':
            return left_val > right_val
        elif self.op == '<=':
            return left_val <= right_val
        elif self.op == '==':
            return left_val == right_val
        elif self.op == '!=':
            return left_val != right_val
        else:
            raise ValueError(f'Invalid operator {self.op}')


class BinOp(Expr):
    """Represents a binary operation
    """

    left: Expr
    op: str
    right: Expr

    def __init__(self, left: Expr, op: str, right: Expr) -> None:
        """Initialize a new binary operation"""

        self.left = left
        self.op = op
        self.right = right

    def evaluate(self, env: dict[str: Any]) -> Any:
        """Evaluate the given binary operation"""

        left_val = self.left.evaluate(env)
        right_val = self.right.evaluate(env)

        if self.op == '+' and ((isinstance(left_val, str) and isinstance(right_val, str)) or
                               (isinstance(left_val, int | float) and isinstance(right_val, int | float))):
            return left_val + right_val
        elif self.op == '*' and not (isinstance(left_val, str) and isinstance(right_val, str)):
            return left_val * right_val
        elif self.op == '-' and (isinstance(left_val, int | float) and isinstance(right_val, int | float)):
            return left_val - right_val
        elif self.op == '/' and (isinstance(left_val, int | float) and isinstance(right_val, int | float)):
            return left_val / right_val
        elif self.op == '//' and (isinstance(left_val, int | float) and isinstance(right_val, int | float)):
            return left_val // right_val
        elif self.op == '%' and (isinstance(left_val, int | float) and isinstance(right_val, int | float)):
            return left_val % right_val
        else:
            raise ValueError(f'Invalid operator {self.op}')

class Assign(Expr):
    """Assign a variable to a target
    """

    target = Name | Subscript
    value = Expr

    def __init__(self, target: Name | Subscript, value: Expr) -> None:
        """Initialize a new assignment statement"""

        self.target = target
        self.value = value

    def evaluate(self, env: dict[str: Any]) -> Any:
        """Create a new variable in the given environment"""
        if isinstance(self.target, Name):
            env[self.target.id] = self.value.evaluate(env)
        else:
            env[self.target.lst.id][self.target.index.evaluate(env)] = self.value.evaluate(env)


class Print(Statement):
    """Takes in an Expression, evaluates it, and prints it"""

    arg = Expr

    def __init__(self, arg: Expr) -> None:
        """Initialize a new print node"""
        self.arg = arg

    def evaluate(self, env: dict[str: Any]) -> Any:
        """Evaluate the given argument and print it"""
        print(self.arg.evaluate(env))


class While(Statement):
    """While loop statement"""

    test: Expr
    body: list[Statement]

    def __init__(self, test: Expr, body: list[Statement]) -> None:
        """Initiate a While Node"""
        self.test = test
        self.body = body

    def evaluate(self, env: dict[str: Any]) -> Any:
        """Evalute the While node
        """
        while self.test.evaluate(env):
            for statement in self.body:
                statement.evaluate(env)

class If(Statement):
    """If statement"""

    test: Expr
    body: list[Statement]
    orelse: list[Statement]

    def __init__(self, test: Expr, body: list[Statement], orelse: list = []) -> None:
        """Initiate an If Node"""
        self.test = test
        self.body = body
        self.orelse = orelse

    def evaluate(self, env: dict[str: Any]) -> Any:
        """Evalute the If node
        """
        if self.test.evaluate(env):
            for statement in self.body:
                statement.evaluate(env)
        else:
            for statement in self.orelse:
                statement.evaluate(env)

class Module:
    """Class representing python program with various statements
    """

    body = list[Statement]

    def __init__(self, body: list[Statement]) -> None:
        """Initialize a module object"""

        self.body = body

    def evaluate(self) -> None:
        """Evaluate all the statements within the given module"""

        env = {}
        for statement in self.body:
            statement.evaluate(env)
