import io
import tokenize
import re

from errors import MissedEndOfBlock, DirectiveSyntaxError
from utils import search_end
from handlers import directive_prefix


class Macros:

    def __init__(self,
                 lines: list[str],
                 line_index: int):
        if self.is_multiline_syntax(lines[line_index]):
            self.init_by_lines(lines, line_index)
        elif self.is_singleline_syntax(lines[line_index]):
            self.init_by_line(lines, line_index)
        else:
            self.body = ""
            self.name = ""

    @staticmethod
    def is_multiline_syntax(line: str) -> bool:
        splited = line.split()
        if len(splited) != 2:
            return False
        return (splited[0] == f"{directive_prefix}define"
                and bool(re.match(r"\w+$", splited[1])))

    @staticmethod
    def is_singleline_syntax(line: str) -> bool:
        splited = line.split()
        if len(splited) < 3:
            return False

        return (splited[0] == f"{directive_prefix}define"
                and bool(re.match(r"\w+$", splited[1])))

    def init_by_lines(self,
                      lines: list[str],
                      line_index: int) -> None:
        if not hasattr(self, "inited"):
            if not Macros.is_multiline_syntax(lines[line_index]):
                raise DirectiveSyntaxError("invalid multiline macro define syntax", line_index)
            end_index = search_end(lines, line_index)
            if end_index <= line_index:
                raise MissedEndOfBlock(f"{lines[line_index]}", line_index)

            self.body = lines[line_index + 1:end_index]
            self.name = lines[line_index].split()[1]
            setattr(self, "inited", True)

    def init_by_line(self,
                     lines: list[str],
                     line_index: int) -> None:
        if not hasattr(self, "inited"):
            if not Macros.is_multiline_syntax(lines[line_index]):
                raise DirectiveSyntaxError("invalid single line macro define syntax", line_index)

            splited = lines[line_index].split()
            self.body = ' '.join(splited[2:])
            self.name = splited[1]
            setattr(self, "inited", True)


class MacrosParam(Macros):

    """ this syntax have not '('
    but every parameter have predefined name as
    {param_prefix}{number} (p_0, p_1, P_2 ...) """
    param_prefix = "p_"

    def __init__(self,
                 lines: list[str],
                 line_index: int):
        super().__init__(lines, line_index)
        self.signature = 0
        self.search_parameters()

    def search_parameters(self):
        if not hasattr(self, "params_inited"):
            found = True
            self.signature = 0
            while bool(found):
                found = re.search(rf'\bp_{self.signature}\b', self.body)
                self.signature += 1
            setattr(self, "params_inited", True)

"""
Class for preprocessing context. Contains and managing
macro defines: expands and save them
"""
class MacrosTable:

    def __init__(self,
                 defines: list[str]):
        pass


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
