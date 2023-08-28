from abc import ABC, abstractmethod
from string import Formatter


def check_consistency(injector):
    def wrapper(*args, **kwargs):
        string = args[1]
        variables = args[2]
        message_variables = [fn for _, fn, _, _ in Formatter().parse(string) if fn is not None]

        for variable in variables:
            if variable not in message_variables:
                DataConsistencyError(variable)

        return injector(*args, **kwargs)
    return wrapper()


class InjectorBase(ABC):
    @abstractmethod
    def inject(self, string: str, variables: list[str]) -> str:
        pass


# Exceptions

class InjectorPresenceError(Exception):
    def __init__(self, string: str):
        """
        Raised when the DataInjector object not initialized, when the variables to be
        injected into the string are specified

        :param string:
        """
        self.string = string

    def __str__(self):
        return f"The DataInjector object not initialized, when variables to be injected " \
               f"into the \"{self.string}\" are specified."


class InjectError(Exception):
    def __init__(self):
        """ Raised when injector is empty """

    def __str__(self):
        return "Injector is empty."


class DataConsistencyError(Exception):
    def __init__(self, variable: str):
        """
        Raised when the variables specified in injectors properties are not present in the string

        :param variable:
        """
        self.variable = variable

    def __str__(self):
        return f"The variable \"{self.variable}\" are not present in the string."
