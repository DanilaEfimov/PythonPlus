
""" Base Error type for Python+ compiler """

class MyError(Exception):

    def __init__(self,
                 message: str="",
                 line: int | None = None):
        self.message = message
        self.line_num = line
        super().__init__(message)

    def what(self, source: list[str]) -> str:
        """ returns detailed message about error """
        if self.line_num is not None and 0 <= self.line_num < len(source):
            line = source[self.line_num]
            return f"Error at line {self.line_num + 1}: {self.message}\n{line}"
        else:
            return self.message

    def __str__(self):
        return self.message

"""
For multylines, or parameter based directives,
build-time variables declarations
"""
class DirectiveSyntaxError(MyError):

    def __init__(self,
                 message: str = "",
                 line: int | None = None,
                 column: int | None = None):
        super().__init__(message, line)
        self.col_num = column

    @staticmethod
    def direct_mistake_line(mask: list[int],
                            *,
                            space: str=' ',
                            arrow: str='^') -> str:
        return ''.join(
            (arrow * n if i%2 else space * n)
            for i, n in enumerate(mask)
        )

    def what(self, source: list[str], mask: list[int] | None = None) -> str:
        if self.line_num is not None and 0 <= self.line_num < len(source):
            line = source[self.line_num]
            error_string = f"Invalid directive syntax at ({self.line_num + 1},: {self.message}\n>{line}\n"
            pointer_string = self.direct_mistake_line(mask)
            return error_string + pointer_string
        else:
            return self.message


class UndefinedVariableError(MyError):

    def __init__(self,
                 message: str = "",
                 identifier: str = "",
                 line: int | None = None,
                 column: int | None = None):
        super().__init__(message, line)
        self.identifier = identifier
        self.col_num = column

    def what(self, source: list[str]):
        if self.line_num is not None and 0 <= self.line_num < len(source):
            line = source[self.line_num]
            error_string = f"Invalid directive syntax at ({self.line_num + 1},: {self.message}\n>{line}\n"
            if self.col_num is not None:
                mask = [ self.col_num, len(self.identifier) ]
                pointer_string = DirectiveSyntaxError.direct_mistake_line(mask)
                return error_string + pointer_string
            else:
                return error_string
        else:
            return self.message


"""
Base Warning type for Python+ compiler
"""

class MyWarning(Warning):
    pass

class RedefinitionWarning(MyWarning):
    pass