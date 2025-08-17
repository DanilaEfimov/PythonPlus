import time
import platform
import sys
import uuid
import os
import warnings

from errors import RedefinitionWarning


class BuildVarsTable:

    def __init__(self):
        self.vars = dict()

        qualifiers = ["const"]
        wrap = BuildVarsTable._wrap

        self.vars["__FILE__"] = wrap("", qualifiers)
        self.vars["__DATE__"] = wrap(time.strftime("%Y-%m-%d"), qualifiers)
        self.vars["__TIME__"] = wrap(time.strftime("%H:%M:%S"), qualifiers)
        self.vars["__DATETIME__"] = wrap(
            f"{self.vars['__DATE__']['value']} {self.vars['__TIME__']['value']}",
            qualifiers
        )
        self.vars["__EPOCH_TIME__"] = wrap(int(time.time()), qualifiers)
        self.vars["__VERSION__"] = wrap("1.0.0", qualifiers)
        self.vars["__PLATFORM__"] = wrap(platform.system(), qualifiers)
        self.vars["__PYTHON_VERSION__"] = wrap(sys.version.split()[0], qualifiers)
        self.vars["__COUNTER__"] = wrap(0, [])
        self.vars["__PWD__"] = wrap(os.getcwd(), qualifiers)
        self.vars["__UUID__"] = wrap(str(uuid.uuid4()), qualifiers)
        self.vars["__MAGIC_CODE__"] = wrap(0xABCDEF, qualifiers)

    @staticmethod
    def _wrap(value, qualifiers: list[str] | None) -> dict:
        return {
            "value": value,
            "qualifiers": qualifiers or []
        }

    def add(self, var, identifier: str, qualifiers: list[str]) -> None:
        if identifier in self.vars:
            warnings.warn("", RedefinitionWarning(f"variable '{identifier}' already defined"))

        table_line = {
            "value": var,
            "qualifiers": qualifiers
        }
        self.vars[identifier] = table_line