class ConfigValidationException(Exception):
    """Raised when config validation failed"""
    pass


class ConfigFileParsingException(Exception):
    """Raised when config file content has incorrect format (not YAML)"""
    pass


class ConfigFileNotExists(Exception):
    """Raised when config file not exists"""
    pass
