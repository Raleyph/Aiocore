from abc import ABC, abstractmethod


class DataInjector(ABC):
    @abstractmethod
    def inject(self, message: str, variables: list[str]):
        pass

    @staticmethod
    def check_consistency(inject):
        def wrapper(*args, **kwargs):
            string: str = args[1]
            variables: list[str] = args[2]

            for variable in variables:
                if string.find(variable) == -1:
                    raise DataConsistencyError(variable)

            return inject(*args, **kwargs)
        return wrapper


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


class DataConsistencyError(Exception):
    def __init__(self, variable: str):
        """
        Raised when the variables specified in content properties are not present in the string

        :param variable:
        """
        self.variable = variable

    def __str__(self):
        return f"The variable \"{self.variable}\" are not present in the string."
