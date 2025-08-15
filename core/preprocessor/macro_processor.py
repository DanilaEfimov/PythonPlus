import re

class Macros:

    def __init__(self, holder: str, name: str):
        self.holder = holder
        self.name = name
    
    @staticmethod
    def replace(line: str) -> str:
        pass

    @staticmethod
    def is_valid_syntax(line: str) -> bool:
        pass


class ParamMacros(Macros):

    def __init__(self,
                 holder: str,
                 name: str,
                 args: list[str]):
        super().__init__(holder, name)
        self.args = args

    @staticmethod
    def replace(line: str) -> str:
        pass

    @staticmethod
    def is_valid_syntax(line: str) -> bool:
        pass

class MacrosTable:

    def __init__(self,
                 defines: list[str]):
        self.table = [Macros(holder, "") for holder in defines]

    def is_defined(self, symbol: str) -> bool:
        return any([macro.holder == symbol for macro in self.table])

    def replace(self, line: str, holder: str) -> str:
        pass