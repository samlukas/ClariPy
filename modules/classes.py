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


class Assign(Expr):
    """Assign a variable to a target
    """

    target = str
    value = Expr

    def __init__(self, target: str, value: Expr) -> None:
        """Initialize a new assignment statement"""

        self.target = target
        self.value = value

    def evaluate(self, env: dict[str: Any]) -> Any:
        """Create a new variable in the given environment"""

        env[self.target] = self.value.evaluate(env)


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
