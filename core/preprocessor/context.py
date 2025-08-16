from argparse import Namespace
from enum import Enum, auto


class State(Enum):
    INIT = auto()
    READING_FILE = auto()
    WAITING_END_OF_BLOCK = auto()


class Context:

    def __init__(self,
                 args: Namespace=...,
                 defines: list[str] | None = None,
                 filename: str="",
                 base_line: int=0,
                 col_num: int=0):

        from macro_processor import MacrosTable
        from core.build_vars import BuildVarsTable

        self.config = args
        if defines is None:
            # defines given by '-D' flag
            defines = {}
        self.macro_table = MacrosTable(defines)

        # global context position
        self.filename = filename
        self.base_line = base_line
        self.col_num = col_num

        self.vars_table = BuildVarsTable()
        self.code = 0
        self.state = State.INIT
