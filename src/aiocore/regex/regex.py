import re


class Regex:
    """

    """

    @staticmethod
    def check_expression(string: str, pattern: str) -> bool:
        return True if re.match(pattern, string) else False
