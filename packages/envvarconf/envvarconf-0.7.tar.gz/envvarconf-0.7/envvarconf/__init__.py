import os
import sys
from decimal import Decimal
from typing import Type, Dict, List


ALLOWED_TYPES = [
    str,
    int,
    float,
    Decimal,
]


class BaseSettings:
    def __init__(self, envvar_prefix: str, appname: str = ""):
        self.appname = appname
        self.envvar_prefix = envvar_prefix

    def get_annotations(self) -> Dict[str, Type]:
        return self.__annotations__

    def construct_envvarname(self, varname: str) -> str:
        return f"{self.envvar_prefix}_{varname}"

    def validate_definition(self):
        for varname, vartype in self.get_annotations().items():
            if vartype not in ALLOWED_TYPES:
                raise TypeError(f"Variable {varname} marked {vartype}, that not allowed for settings use")

    def set_var(self, varname: str, raw_value: str, vartype: Type):
        assert vartype in ALLOWED_TYPES
        try:
            varvalue = vartype(raw_value)
        except ValueError as ex:
            raise ValueError(f"There is error converting {varname}'s value '{raw_value}' to {vartype}'") from ex
        setattr(self, varname, varvalue)

    def validation_errors(self) -> List[str]:
        errs = []
        for varname, vartype in self.get_annotations().items():
            if not hasattr(self, varname):
                errs.append(f"{varname} is not defined")
        return errs

    def load_from_env(self):
        for varname, vartype in self.get_annotations().items():
            envvarname = self.construct_envvarname(varname)
            if envvarname in os.environ:
                self.set_var(varname, raw_value=os.environ[envvarname], vartype=vartype)

    def load(self):
        self.validate_definition()
        self.load_from_env()

        errors = self.validation_errors()
        if errors:
            print("There is errors in settings")
            print("\n".join([f" * {x}" for x in errors]))
            print()
            self.print_help_then_exit()

    def print_detailed(self):
        print(f"{self.appname or 'Application'} settings:")

        for varname, vartype in self.get_annotations().items():
            envvarname = self.construct_envvarname(varname)

            if hasattr(self, varname):
                varval = getattr(self, varname)
            else:
                varval = "NOT DEFINED!"

            print(f"{varname}({envvarname}) {vartype} = {varval}")

    def print_help_then_exit(self):
        self.print_detailed()
        sys.exit(1)

    def __str__(self):
        vs = []
        for varname, vartype in self.get_annotations().items():
            if hasattr(self, varname):
                varval = getattr(self, varname)
            else:
                varval = "?"

            vs.append(f"{varname}={varval}")

        v = ", ".join(vs)

        return f"<{self.__class__.__name__} {v}>"
