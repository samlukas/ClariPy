"""
CSC111 Winter 2023 Project: ClariPy

Classes and Methods:

This module contains code that could be used to represent a various parts that are
commonly found in python program.

This includes classes such as Statements, Expresisons, Num literals, String literals,
Binary operations, and Assignment statements
"""
from __future__ import annotations

from typing import Any


class Statement:
    """An abstract class representing a Python statement.
    """

    def evaluate(self, env: dict[str: Any]) -> Any:
        """Evaluate the statement with the given environment.
        The returned value should be the same as how the python interpreter would evaluate the statement
        """

        raise NotImplementedError


class Expr(Statement):
    """An abstract class representing a Python expression.
    """

    def evaluate(self, env: dict[str: Any]) -> Any:
        """Evaluate the expression with the given environment.

        The returned value should be the same as how the python interpreter would evaluate the expression
        """

        raise NotImplementedError


class Num(Expr):
    """Numeric literal

    Instance Attributes:
        - n: the value of the literal
    """

    n: int | float

    def __init__(self, number: int | float) -> None:
        """Initialize a new numeric literal"""

        self.n = number

    def evaluate(self, env: dict[str: Any]) -> Any:
        """Evaluate the expression with the given environment.

        The returned value should be the same as how the python interpreter would evaluate the expression

        >>> Num(5).evaluate({})
        5
        """

        return self.n

    def __str__(self) -> str:
        """Return the string representation of this expression"""

        return f"Num({self.n})"


class Str(Expr):
    """String literal

    Instance Attributes:
        - s: the value of the literal
    """

    s: str

    def __init__(self, string: str) -> None:
        """Initialize a new string literal"""

        self.s = string

    def evaluate(self, env: dict[str: Any]) -> Any:
        """Evaluate the expression with the given environment.

        The returned value should be the same as how the python interpreter would evaluate the expression.

        >>> Str('hi').evaluate({})
        'hi'
        """

        return self.s

    def __str__(self) -> str:
        """Return the string representation of this expression"""

        return f"Str(\"{self.s}\")"


class Name(Expr):
    """Variable expression

    Instance Attributes:
        - id: the variable name
    """

    id: str

    def __init__(self, id_: str) -> None:
        """Initialize a new variable expression"""

        self.id = id_

    def evaluate(self, env: dict[str: Any]) -> Any:
        """See if the given id is in env, if it is, return associated value, else raise NameError.

        The returned value should be the same as how the python interpreter would evaluate the expression.

        >>> Name('x').evaluate({'x': 5})
        5
        """

        if self.id in env:
            return env[self.id]
        else:
            raise NameError

    def __str__(self) -> str:
        """Return the string representation of this expression"""

        return f"Name({self.id})"


class List(Expr):
    """List literal

    Instance Attributes:
        - lst: the value of the literal
    """

    lst: list

    def __init__(self, lst: list) -> None:
        """Initialize a new list literal"""

        self.lst = lst

    def evaluate(self, env: dict[str: Any]) -> Any:
        """Evaluate the given list literal

        The returned value should be the same as how the python interpreter would evaluate the expression

        >>> List([Num(1), Num(2), Num(3)]).evaluate({})
        [1, 2, 3]
        """

        return [elem.evaluate(env) for elem in self.lst]

    def __getitem__(self, i: int) -> Any:
        """Get the item stored at a specific index in the list

        >>> List([1, 2, 3])[1]
        2
        """

        if i >= len(self.lst):
            raise IndexError
        else:
            return self.lst[i]


class Subscript(Expr):
    """List indexing

    Instance Attributes:
        - lst: the variable that corresponds to a list
        - index: the index used for indexing operations
    """

    lst: Name
    index: Expr

    def __init__(self, lst: Name, index: Expr) -> None:
        """Initialize a new indexing operation"""

        self.lst = lst
        self.index = index

    def evaluate(self, env: dict[str: Any]) -> Any:
        """Evaluate a new indexing operation

        The returned value should be the same as how the python interpreter would evaluate the expression

        >>> Subscript(Name('x'), Num(1)).evaluate({'x': [1, 2, 3]})
        2
        """

        i = self.index.evaluate(env)

        if i >= len(self.lst.evaluate(env)):
            raise IndexError
        else:
            return self.lst.evaluate(env)[i]


class Bool(Expr):
    """Boolean literal

    Instance Attribute:
        - b: the value of the literal
    """

    b: bool

    def __init__(self, b: bool) -> None:
        """Initialize a new string literal"""

        self.b = b

    def evaluate(self, env: dict[str: Any]) -> Any:
        """Evaluate the given bool literal

        The returned value should be the same as how the python interpreter would evaluate the expression

        >>> Bool(True).evaluate({})
        True
        """

        return self.b

    def __str__(self) -> str:
        """Return the string representation of this expression"""

        return f"Bool({self.b})"


class BoolOp(Expr):
    """Represents a bool operation

    Instance Attributes:
        - op: the bool/comparison operator
        - left: the left operand
        - right: the right operand

    Representation Invariants:
        - self.op in {'and', 'or', '<', '<=', '>', '>=', '==', '!='}

    """

    op: str
    right: Expr
    left: Expr

    def __init__(self, op: str, left: Expr, right: Expr) -> None:
        """Initialize a new binary operation

        Preconditions:
        - self.op in {'and', 'or', '<', '<=', '>', '>=', '==', '!='}
        """

        self.op = op
        self.right = right
        self.left = left

    def evaluate(self, env: dict[str: Any]) -> Any:
        """Evaluate the given bool operation

        The returned value should be the same as how the python interpreter would evaluate the expression

        >>> expr = BoolOp('<', Num(3), Num(5))
        >>> expr.evaluate({})
        True
        """

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
        else:  # should never get to this point because of precondition
            raise ValueError(f'Invalid operator {self.op}')


class BinOp(Expr):
    """Represents a binary operation

    Instance Attributes:
        - left: the left operand
        - op: the arithmetic operator
        - right: the right operand

    Representation Invariants:
        - self.op in {'+', '*', '-', '/', '//', '%'}
    """

    left: Expr
    op: str
    right: Expr

    def __init__(self, left: Expr, op: str, right: Expr) -> None:
        """Initialize a new binary operation

        Preconditions:
            - self.op in {'+', '*', '-', '/', '//', '%'}
        """

        self.left = left
        self.op = op
        self.right = right

    def evaluate(self, env: dict[str: Any]) -> Any:
        """Evaluate the given binary operation

        The returned value should be the same as how the python interpreter would evaluate the expression

        >>> expr = BinOp(Num(5), '+', Num(-3))
        >>> expr.evaluate({})
        2
        """

        left_val = self.left.evaluate(env)
        right_val = self.right.evaluate(env)

        if self.op == '+' and ((isinstance(left_val, str) and isinstance(right_val, str))
                               or (isinstance(left_val, int | float) and isinstance(right_val, int | float))):
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

    Instance Attributes:
        - target: the variable name on the left-hand side of the equals sign
        - value: the expression on the right-hand side of the equals sign
    """

    target: Name | Subscript
    value: Expr

    def __init__(self, target: Name | Subscript, value: Expr) -> None:
        """Initialize a new assignment statement"""

        self.target = target
        self.value = value

    def evaluate(self, env: dict[str: Any]) -> Any:
        """Create a new variable in the given environment.
        The returned value should be the same as how the python interpreter would evaluate the expression.
        Evaluates the right hand side and then updates env to store the corresponding value with the target.
        >>> expr = Assign(Name('x'), Num(10))
        >>> env = {}
        >>> expr.evaluate(env)
        >>> env['x']
        10
        """
        if isinstance(self.target, Name):
            env[self.target.id] = self.value.evaluate(env)
        else:
            env[self.target.lst.id][self.target.index.evaluate(env)] = self.value.evaluate(env)


class Print(Statement):
    """Takes in an Expression, evaluates it, and prints it
    Instance Attributes:
        - arg: the expression to be evaluated and printed out
    """

    arg: Expr

    def __init__(self, arg: Expr) -> None:
        """Initialize a new print node"""

        self.arg = arg

    def evaluate(self, env: dict[str: Any]) -> Any:
        """Evaluate the given argument and print it

        The returned value should be the same as how the python interpreter would evaluate the expression.

        >>> env = {}
        >>> Print(Num(5)).evaluate(env)
        5
        """
        print(self.arg.evaluate(env))


class While(Statement):
    """While loop statement

    Instance Attributes:
        - test: the conditional part of the while loop
        - body: the list of statements to evaluate when test is True
    """

    test: Expr
    body: list[Statement]

    def __init__(self, test: Expr, body: list[Statement]) -> None:
        """Initiate a While Node"""

        self.test = test
        self.body = body

    def evaluate(self, env: dict[str: Any]) -> Any:
        """Evalute the While node

        The returned value should be the same as how the python interpreter would evaluate the expression.

        >>> env = {'x': 0}
        >>> body = [Assign(Name('x'), BinOp(Name('x'), '+', Num(1)))]
        >>> test = BoolOp('<', Name('x'), Num(5))
        >>> loop = While(test, body).evaluate(env)
        >>> Name('x').evaluate(env)
        5
        """

        while self.test.evaluate(env):
            for statement in self.body:
                statement.evaluate(env)


class If(Statement):
    """If statement

    Instance Attributes:
        - test: the conditional part of the if statement
        - body: the list of statements to evaluate when test is True
        - orelse: the list of statement to evaluate when test is False
    """

    test: Expr
    body: list[Statement]
    orelse: list[Statement]

    def __init__(self, test: Expr, body: list[Statement], orelse: list = None) -> None:
        """Initiate an If Node"""

        self.test = test
        self.body = body
        self.orelse = orelse

    def evaluate(self, env: dict[str: Any]) -> Any:
        """Evalute the If node

        The returned value should be the same as how the python interpreter would evaluate the expression.

        >>> stmt = If(Bool(True), [Assign(Name('x'), Num(1))], [Assign(Name('y'), Num(0))])
        >>> env = {}
        >>> stmt.evaluate(env)
        >>> env
        {'x': 1}
        """
        if self.test.evaluate(env):
            for statement in self.body:
                statement.evaluate(env)
        elif self.orelse is not None:
            for statement in self.orelse:
                statement.evaluate(env)


class Module:
    """Class representing python program with various statements

    Instance Attributes:
        - body: a list of statements to be evaluated
    """

    body: list[Statement]

    def __init__(self, body: list[Statement]) -> None:
        """Initialize a module object"""

        self.body = body

    def evaluate(self) -> None:
        """Evaluate all the statements within the given module

        >>> Module([Print(Num(5))]).evaluate()
        5
        """

        env = {}
        for statement in self.body:
            statement.evaluate(env)


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'allowed-io': ['Print.evaluate'],
        'disable': ['abstract-method', 'syntax-error']
    })
