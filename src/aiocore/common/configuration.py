import configparser
import sys
import os


class ConfigReader:
    __CONFIG_FILE = "src/config.ini"

    def __init__(self):
        """ Initialize config manager """
        config_file_path = os.path.join(sys.path[1], self.__CONFIG_FILE)

        if not os.path.exists(config_file_path):
            raise ConfigFileError()

        self.config = configparser.ConfigParser()
        self.config.read(config_file_path)

    def get_parameter(
            self,
            config_group: str,
            config_parameter: str
    ) -> str:
        """
        Return requested configuration parameter from specified group

        :param config_group:
        :param config_parameter:
        :return:
        """
        config = self.config

        if config_group not in config:
            raise ConfigGroupError(config_group)

        if config_parameter not in config[config_group]:
            raise ConfigParameterError(config_group, config_parameter)

        return config[config_group][config_parameter]


# Exceptions

class ConfigFileError(Exception):
    def __init__(self):
        """ Raise when the configuration file path does not exist in the main project directory """
        pass

    def __str__(self):
        return "The configuration file path does not exist in the main project directory."


class ConfigGroupError(Exception):
    def __init__(self, group_name: str):
        """
        Raised when the requested configuration group is not present in the config file

        :param group_name:
        :return:
        """
        self.group_name = group_name

    def __str__(self):
        return f"The requested configuration group \"{self.group_name}\" is not present in the configuration file."


class ConfigParameterError(Exception):
    def __init__(self, group_name: str, parameter_name: str):
        """
        Raised when the requested configuration parameter is not present in the config file

        :param group_name:
        :param parameter_name:
        :return:
        """
        self.group_name = group_name
        self.parameter_name = parameter_name

    def __str__(self):
        return f"The requested configuration parameter \"{self.parameter_name}\" is not " \
               f"present in specified group \"{self.group_name}\" of the configuration file."
