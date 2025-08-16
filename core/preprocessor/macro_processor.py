import io
import tokenize
import re

from handlers import directive_prefix


class Macros:

    def __init__(self, holder: str, name: str):
        self.holder = holder
        self.name = name

    def replace(self, line: str) -> str:
        result = []
        tokens = tokenize.generate_tokens(io.StringIO(line).readline)

        for tok_type, tok_string, _, _, _ in tokens:
            if tok_type == tokenize.NAME and tok_string == self.name:
                result.append((tok_type, self.name))
            else:
                result.append((tok_type, tok_string))

        return tokenize.untokenize(result)

    @staticmethod
    def is_valid_syntax(line: str) -> bool:
        pattern = rf"""
            ^\s*
            {re.escape(directive_prefix)}define
            \s+
            ([A-Za-z_][A-Za-z0-9_]*)
            \s+
            (.*)
            $
            """
        return bool(re.match(pattern, line))


class ParamMacros(Macros):

    def __init__(self,
                 holder: str,
                 name: str,
                 args: list[str]):
        super().__init__(holder, name)
        self.args = args

    def replace(self, line: str) -> str:
        pass

    @staticmethod
    def is_valid_syntax(line: str) -> bool:
        pattern = rf"""^\s*  
            {re.escape(directive_prefix)}define
            \s+
            ([A-Za-z_][A-Za-z0-9_]*)
            \s*
            (?:\(([^)]*)\))?
            \s+
            (.+)$
            """
        return bool(re.match(pattern, line, re.VERBOSE))


class MacrosTable:

    def __init__(self,
                 defines: list[str]):
        self.table = [Macros(holder, "") for holder in defines]

    def is_defined(self, symbol: str) -> bool:
        return any([macro.holder == symbol for macro in self.table])

    def replace(self, line: str) -> str:
        for macro in self.table:
            line = macro.replace(line)
        return line


def expand_macros(lines: list[str], table: MacrosTable) -> int:
    """
    essential function of macro processor
    :param lines: source code
    :param table: table of defined macros
    :return: exit code of preprocessing
    """
    if not hasattr(expand_macros, "macros_expanded"):
        setattr(expand_macros, "macros_expanded", True)
        for i, line in enumerate(lines):
            lines[i] = table.replace(line)
        return 0
    return 1
