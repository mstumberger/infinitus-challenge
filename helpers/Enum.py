def enum(**enums):
    return type('Enum', (), enums)

ACTION = enum(PUT='PUT', GET='GET', DELETE='DELETE', FIND='FIND')
