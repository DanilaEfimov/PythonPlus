import io
import re
import tokenize

from core.preprocessor.errors import ArgumentMismatchError, MacrosSyntaxError
from errors import DirectiveSyntaxError
from handlers import directive_prefix

class Macros:

    def __init__(self,
                 name: str,
                 body: str | None = None):
        self.name = name
        if body is None:
            self.body = ''
        else:
            self.body = body

    @staticmethod
    def is_valid_syntax(line: str) -> bool:
        return Macros.is_singleline_syntax(line) or Macros.is_multyline_syntax(line)

    @staticmethod
    def is_singleline_syntax(line: str) -> bool:
        splited = [word.strip() for word in line.split()]
        if len(splited) > 2:
            return (splited[0] == f"{directive_prefix}define"
                and bool(re.fullmatch(r'[A-Za-z_]+', splited[1])))
        return False

    @staticmethod
    def is_multyline_syntax(line: str) -> bool:
        splited = [word.strip() for word in line.split()]
        if len(splited) == 2:
            return (splited[0] == f"{directive_prefix}define"
                    and bool(re.fullmatch(r'[A-Za-z_]+', splited[1])))
        return False

    def set_body(self, body: str) -> None:
        self.body = body

    def expand(self, line: str) -> str:
        new_tokens = []
        for token in tokenize.tokenize(io.BytesIO(line.encode()).readline):
            if token.type == tokenize.NAME and token.string.strip() == self.name:
                token = tokenize.TokenInfo(
                    type=token.type,
                    string=self.body,
                    start=token.start,
                    end=token.end,
                    line=token.line
                )
            new_tokens.append(token)
        result = tokenize.untokenize(new_tokens).decode('utf-8')
        return result

class ParamMacros(Macros):

    def __init__(self,
                 name: str,
                 body: str | None = None,
                 params: list[str] | None = None):
        super().__init__(name, body)
        if params is None:
            self.params = []
        else:
            self.params = [Macros(name) for name in params]

    @staticmethod
    def is_singleline_syntax(line: str) -> bool:
        pattern = rf'^{re.escape(directive_prefix)}define\s+\w+\s*\([^()]*\)\s+.+$'
        return bool(re.match(pattern, line.strip()))

    @staticmethod
    def is_multyline_syntax(line: str) -> bool:
        pattern = rf'^{re.escape(directive_prefix)}define\s+\w+\s*\([^()]*\)\s*$'
        return bool(re.match(pattern, line.strip()))

    @staticmethod
    def get_name(line: str) -> str:
        pattern = rf'{re.escape(directive_prefix)}define\s+(?P<name>\w+)'
        match = re.search(pattern, line)
        if match:
            name = match.group('name')
            return name
        raise DirectiveSyntaxError(f"Invalid parameter macros syntax:\n{line}")

    def get_values(self, line: str) -> list[str]:
        pattern = rf'{re.escape(directive_prefix)}define\s+{re.escape(self.name)}\s*\((?P<args>[^()]*)\)'
        match = re.match(pattern, line)
        if not match:
            raise MacrosSyntaxError(f"Invalid macro call: {line}")
        args_str = match.group("args")
        args = [arg.strip() for arg in args_str.split(",") if arg.strip()]
        return args

    def set_params(self, values: list[str]) -> None:
        size = len(self.params)
        if len(values) != size:
            raise ArgumentMismatchError(f"required {size}, given {len(values)}\n{values}")

        for i in range(size):
            self.params[i].set_body(values[i])

    def expand(self, line: str) -> str:
        pattern = rf'''
            \b{re.escape(self.name)}\b
            \s*
            \((?P<args>[^()]*?)\)
            '''
        match = re.search(pattern, line, re.VERBOSE)
        new_tokens = []
        for token in tokenize.tokenize(io.BytesIO(line.encode()).readline):
            pass

"""
Class for preprocessing context. Contains and managing
macro defines: expands and save them
"""
class MacrosTable:

    def __init__(self,
                 defines: list[str]):
        self.table = []
        for name in defines:
            self.table.append(Macros(name))

    def append(self, macros: Macros) -> None:
        self.table.append(macros)

    def pop(self, index: int) -> None:
        self.table.pop(index)

    def expand(self, line: str) -> str:
        for macros in self.table:
            line = macros.expand(line)
        return line


def expand_macros(lines: list[str], table: MacrosTable) -> int:
    """
    essential function of macro processor
    :param lines: source code
    :param table: table of defined macros
    :return: exit code of preprocessing
    """
    for i, line in enumerate(lines):
        if line.strip():
            lines[i] = table.expand(line)
    return 0

