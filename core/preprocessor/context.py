import argparse
from enum import Enum, auto

from macro_processor import MacrosTable
from core.build_vars import BuildVarsTable


class State(Enum):
    INIT = auto()
    WAITING_END_OF_BLOCK = auto()


class Context:

    def __init__(self,
                 args: argparse.Namespace=...,
                 defines: list[str] | None = None,
                 filename: str="",
                 base_line: int=0,
                 col_num: int=0):
        self.config = args
        if defines is None:
            defines = {}
        self.table = MacrosTable(defines)
        self.filename = filename
        self.base_line = base_line
        self.col_num = col_num

        self.vars = BuildVarsTable()
        self.code = 0
        self.state = State.INIT