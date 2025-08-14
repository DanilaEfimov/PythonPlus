import re

class Macros:

    def __init__(self, holder: str, name: str):
        self.holder = holder
        self.name = name
    
    @staticmethod
    def replace(line: str) -> str:
        pass

class ParamMacros(Macros):

    def __init__(self):
        pass

    @staticmethod
    def replace(line: str) -> str:
        pass

class MacrosTable:

    def __init__(self):
        self.table = []