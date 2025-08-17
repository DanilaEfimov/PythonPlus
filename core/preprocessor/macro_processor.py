import io
import tokenize
import re

from core.preprocessor.errors import MissedEndOfBlock, DirectiveSyntaxError
from utils import search_end
from handlers import directive_prefix


class Macros:

    def __init__(self, lines: list[str], line_index: int):
        header = lines[line_index]
        tokens = header.split()
        if Macros.is_multiline_syntax(header):
            end_index = search_end(lines, line_index)
            if end_index < line_index:
                raise MissedEndOfBlock(f"\n{header}\n", line_index)

            self.holder = tokens[1]
            self.body = '\n'.join(lines[line_index+1:end_index])

        elif Macros.is_singleline_syntax(header):
            body_start = header.find(self.holder) + len(self.holder)
            self.holder = tokens[1]
            self.body = header[body_start:].strip()

        else:
            raise DirectiveSyntaxError("checkout multi/single macro syntax", line_index)


    def replace(self, line: str) -> str:
        result = []
        tokens = tokenize.generate_tokens(io.StringIO(line).readline)

        for tok_type, tok_string, _, _, _ in tokens:
            if tok_type == tokenize.NAME and tok_string == self.holder:
                result.append((tok_type, self.holder))
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

    @staticmethod
    def is_multiline_syntax(line: str) -> bool:
        if Macros.is_valid_syntax(line):
            return len(line.split()) == 2
        return False

    @staticmethod
    def is_singleline_syntax(line: str) -> bool:
        if Macros.is_valid_syntax(line):
            return len(line) > 2
        return False


class ParamMacros(Macros):

    def __init__(self, line):
        super().__init__("holder")
        self.args = {}

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


"""
Class for preprocessing context. Contains and managing
macro defines: expands and save them
"""
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
