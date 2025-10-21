class InfraChecksError(Exception):
    pass


class YamlLoadingError(InfraChecksError):
    pass


class TemplatedYAMLError(YamlLoadingError):
    def __init__(self, message: str = "YAML appears to contain templating and cannot be parsed safely.") -> None:
        super().__init__(message)
