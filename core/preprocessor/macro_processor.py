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

    @classmethod
    def from_name(cls, name: str):
        free_pattern = "\"\"\"\"\"\""
        return Macros([f"{directive_prefix}define {name} {free_pattern}"], 0)

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

            self.body = '\n'.join(lines[line_index + 1:end_index])
            self.name = lines[line_index].split()[1]
            lines[line_index:end_index+1] = []
            setattr(self, "inited", True)

    def init_by_line(self,
                     lines: list[str],
                     line_index: int) -> None:
        if not hasattr(self, "inited"):
            if not Macros.is_singleline_syntax(lines[line_index]):
                raise DirectiveSyntaxError("invalid single line macro define syntax", line_index)

            splited = lines[line_index].split()
            self.body = ' '.join(splited[2:])
            self.name = splited[1]
            lines.pop(line_index)
            setattr(self, "inited", True)

    def expand(self, line: str) -> str:
        pattern = rf"\b{re.escape(self.name)}\b"
        line = re.sub(pattern, self.body, line)
        return line


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
        self.params = []

    def search_parameters(self) -> None:
        if not hasattr(self, "params_inited"):
            self.signature = 0
            while bool(re.search(rf'\b{self.param_prefix}{self.signature}\b', self.body)):
                self.signature += 1
            setattr(self, "params_inited", True)

    def read_parameters(self, line: str) -> None:
        match = re.search(rf'{re.escape(self.name)}\[\s*(.*?)\s*\]', line)
        if not match:
            self.params = []
            return

        items = match.group(1).split(",")
        params = [item.strip() for item in items]
        if len(params) != self.signature:
            raise ValueError(
                f"Number of parameters ({len(self.params)}) does not match the expected ({self.signature}): {self.name}"
            )
        self.params = params

    @classmethod
    def from_name_and_sign(cls, name: str, signature: int):
        free_pattern = "\"\"\"\"\"\""
        macros = MacrosParam([f"{directive_prefix}define {name} {free_pattern}"], 0)
        macros.signature = signature
        return macros

    def expand(self, line: str) -> str:
        body = self.body
        for i in range(self.signature):
            pattern = fr"\b{self.param_prefix}{i}\b"
            body = re.sub(pattern, self.params[i], body)

        pattern = rf'{re.escape(self.name)}\[[^\]]*\]'
        result = re.sub(pattern, body, line)
        return result


"""
Class for preprocessing context. Contains and managing
macro defines: expands and save them
"""
class MacrosTable:

    def __init__(self,
                 defines: list[str]):
        self.table = []
        for name in defines:
            self.add_single(name)

    def expand(self, line: str) -> str:
        for macros in self.table:
            line = macros.expand(line)
        return line

    def add_single(self, name: str) -> None:
        self.table.append(Macros.from_name(name))

    def add_param(self, name: str, signature: int) -> None:
        self.table.append(MacrosParam.from_name_and_sign(name, signature))


def expand_macros(lines: list[str], table: MacrosTable) -> int:
    """
    essential function of macro processor
    :param lines: source code
    :param table: table of defined macros
    :return: exit code of preprocessing
    """
    if not hasattr(expand_macros, "macros_expanded"):
        for i, line in enumerate(lines):
            lines[i] = table.expand(line)
        setattr(expand_macros, "macros_expanded", True)
        return 0
    return 1
