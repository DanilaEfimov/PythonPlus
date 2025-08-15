import time
import platform
import sys
import uuid
import os

class BuildVarsTable:
    def __init__(self):
        self.vars = {}

        self.vars["__FILE__"] = ""
        self.vars["__DATE__"] = time.strftime("%Y-%m-%d")
        self.vars["__TIME__"] = time.strftime("%H:%M:%S")
        self.vars["__DATETIME__"] = f"{self.vars['__DATE__']} {self.vars['__TIME__']}"
        self.vars["__EPOCH_TIME__"] = int(time.time())
        self.vars["__VERSION__"] = "1.0.0"
        self.vars["__PLATFORM__"] = platform.system()
        self.vars["__PYTHON_VERSION__"] = sys.version.split()[0]
        self.vars["__COUNTER__"] = 0
        self.vars["__PWD__"] = os.getcwd()
        self.vars["__UUID__"] = str(uuid.uuid4())
        self.vars["__MAGIC_CODE__"] = 0xABCDEF

    def add(self, var, identifier: str, qualifiers: list[str]) -> None:
        pass