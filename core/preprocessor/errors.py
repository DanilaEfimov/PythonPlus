"""
In this file, the hierarchy of exception and warning
classes for the Python+ compiler preprocessor is defined.
"""
from typing import List, Callable


""" Base Preprocessor Error type for Python+ compiler """
class PreprocessorError(Exception):

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

""" Base Preprocessor Warning type for Python+ compiler """
class PreprocessorWarning(Warning):

    def __init__(self, message: str):
        self.message = message

    def what(self):
        return f"Preprocessor::Warning: {self.message}"

    def __str__(self):
        return self.what()


class EmptyInputWarning(PreprocessorWarning):

    def __init__(self,
                 message: str = ""):
        super().__init__(message)

    def what(self):
        return f"Was given empty file: {self.message}"

    def __str__(self):
        return self.what()


class SelfReferenceError(PreprocessorError):

    def __init__(self,
                 message: str,
                 filename: str,
                 line: int | None = None,
                 column: int | None = None):
        super().__init__(message)
        self.filename = filename
        self.line_num = line
        self.col_num = column

    def what(self, source: list[str]):
        if self.line_num is not None and 0 <= self.line_num < len(source):
            line = source[self.line_num]
            error_string = f"Circular include error at '{self.filename}' line {self.line_num + 1}: {self.message}\n>{line}\n"

            if self.col_num is not None and 0 <= self.col_num < len(line):
                mask = [self.col_num, 1]  # spaces ~ + 1 arrow ^
                pointer_string = DirectiveSyntaxError.direct_mistake_line(mask, space='~')
                return error_string + pointer_string
            else:
                return error_string

        else:
            return self.message


class SourceIndexError(PreprocessorError):

    from context import Context
    def __init__(self,
                 message: str="",
                 handler: Callable[[List[str], int, Context], int]=...,
                 line: int | None = None):
        self.message = message
        self.handler = handler
        self.line_num = line
        super().__init__(message)

    def what(self, source: list[str]) -> str:
        """ returns detailed message about error """
        if self.line_num is not None and 0 <= self.line_num < len(source):
            line = source[self.line_num]
            return f"Handler '{self.handler}' returned invalid index; at line {self.line_num + 1}: {self.message}\n{line}"
        else:
            return self.message

    def __str__(self):
        return self.message

"""
For multylines, or parameter based directives,
build-time variables declarations
"""
class DirectiveSyntaxError(PreprocessorError):

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
        ) + '\n'

    def what(self, source: list[str], mask: list[int] | None = None) -> str:
        if self.line_num is not None and 0 <= self.line_num < len(source):
            line = source[self.line_num]
            error_string = f"Invalid directive syntax at line {self.line_num + 1}: {self.message}\n>{line}\n"

            if mask is not None:
                pointer_string = self.direct_mistake_line(mask)
            elif self.col_num is not None and 0 <= self.col_num < len(line):
                pointer_string = self.direct_mistake_line([self.col_num, 1])
            else:
                pointer_string = ''

            return error_string + pointer_string
        else:
            return self.message


class UnexpectedFileError(PreprocessorError):

    def __init__(self,
                 message: str,
                 filename: str,
                 line: int | None = None):
        super().__init__(message, line)
        self.filename = filename

    def what(self, source: list[str]):
        if self.line_num is not None and 0 <= self.line_num < len(source):
            line = source[self.line_num]
            error_string = f"Unexpected filename at line {self.line_num + 1}: {self.message}\n>{line}\n"
            pos = line.find(self.filename)
            pointer_string = DirectiveSyntaxError.direct_mistake_line(
                [pos + 1 if pos >= 0 else 0, len(self.filename)],
                space='~'
            )
            return error_string + pointer_string
        else:
            return self.message

    def __str__(self):
        return f"Unexpected filename: '{self.filename}';\n{self.message}"


class UndefinedVariableError(PreprocessorError):

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
            error_string = f"Invalid directive syntax at ({self.line_num + 1}): {self.message}\n>{line}\n"

            if self.col_num is not None and 0 <= self.col_num < len(line):
                mask = [ self.col_num, len(self.identifier) ]
                pointer_string = DirectiveSyntaxError.direct_mistake_line(mask)
                return error_string + pointer_string
            else:
                return error_string

        else:
            return self.message


class MacrosError(PreprocessorError):
    
    def __init__(self,
                 message: str,
                 line: int):
        super().__init__(message, line)


class MissedEndOfBlock(MacrosError):

    def __init__(self,
                 message: str,
                 line: int):
        super().__init__(message, line)

    def what(self, source: list[str], mask: list[int] | None = None) -> str:
        if self.line_num is not None and 0 <= self.line_num < len(source):
            line = source[self.line_num]
            error_string = f"Missed '@end' of block ({self.line_num + 1}): {self.message}\n>{line}\n"
            return error_string

        else:
            return self.message

    def __str__(self):
        return self.message


class ArgumentMismatchError(MacrosError):

    def __init__(self,
                 message: str,
                 line: int | None = None):
        super().__init__(message, line)

class MacrosSyntaxError(MacrosError):

    def __init__(self,
                 message: str,
                 line: int | None = None):
        super().__init__(message, line)

class RedefinitionWarning(PreprocessorWarning):
    pass
