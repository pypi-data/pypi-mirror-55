from std import std
import sys
from parsers import Functionality, Parameter, Input
from formatters import (
    Output,
    Error,
    Documentation,
    Introspection,
)


class Exposable(object):
    starts_with = "eX://"
    auth_splitter = "@"
    method_seperator = "-"
    function_pointer = "!"
    instance_pointer = "#"
    ends_with = "/"

    def __init__(
        self,
        functionality=Functionality,
        parameter=Parameter,
        input=Input,
        output=Output,
        error=Error,
        introspection=Introspection,
        documentation=Documentation,
    ):
        self.input_set = (sys.argv, sys.stdin)
        self.functionality = functionality
        self.parameter = parameter
        self.input = input
        self.output = output
        self.error = error
        self.introspection = introspection

    def __call__(self, *args, **kwargs):
        self.function = self.functionality.parse(
            self.input_set
        )

        args, kwargs = self.parameter.parse(self.input_set)
        input = self.input.parse(self.input_set)

        with std(stdin_file=input, stderr_file="log") as s:
            result = self.function(*args, *kwargs)

        output = self.output.format(s.stdout.getvalue())
        if output:
            print(output)

        error = self.error.format(s.stderr.getvalue())
        if error:
            raise error

        return result

    def __repr__(self):
        hsh = ""
        if hasattr(self.function, "__qualname__"):
            hsh = (
                str(self.function_pointer)
                .join(
                    self.function.__qualname__.split(".")
                )
                .lower()
            )

        if hasattr(self.function, "__self__"):
            tmp = hsh.split(str(self.function_pointer))
            method_list = (
                str(self.method_seperator).join(tmp[0:-1]),
            )
            funcname = str(tmp[-1])
            hsh = (
                str(self.function_pointer).join(
                    [method_list, funcname]
                )
                + str(self.instance_pointer)
                + str(self.function.__self__)
            )
        hsh = (
            str(self.starts_with)
            + hsh
            + str(self.ends_with)
        )
        return hsh
