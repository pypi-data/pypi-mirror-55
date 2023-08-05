import phpserialize

from typing import Any, Optional


class Replacer:
    """
    Class which replaces substring in a string. Class takes into account that a string can be serialized and
    before a find/replace action it deserializes a string.
    """
    def __init__(self, serializer: Optional[Any] = None):
        self.__serializer = serializer or phpserialize

        try:
            assert callable(self.__serializer.dumps)
        except (AssertionError, AttributeError):
            raise AttributeError('Serializer must have a defined "dumps" method.')

        try:
            assert callable(self.__serializer.loads)
        except (AssertionError, AttributeError):
            raise AttributeError('Serializer must have a defined "loads" method.')

    def replace(self, string: str, old: str, new: str) -> str:
        if not isinstance(string, str):
            return string

        try:
            value = self.__serializer.loads(string.encode())
            self.__recursive_replace(old, new, value)
            value = self.__serializer.dumps(value).decode()

            return value
        except (TypeError, ValueError):
            return string.replace(old, new)

    def __recursive_replace(self, old: str, new: str, obj: Any):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if isinstance(value, str):
                    val: str = obj[key]
                    val = val.replace(old, new)
                    obj[key] = val
                elif isinstance(value, bytes):
                    val: str = obj[key].decode()
                    val = val.replace(old, new)
                    obj[key] = val.encode()
                else:
                    self.__recursive_replace(old, new, obj[key])
                    
        if isinstance(obj, list):
            for index in range(len(obj)):
                if isinstance(obj[index], str):
                    val: str = obj[index]
                    val = val.replace(old, new)
                    obj[index] = val
                elif isinstance(obj[index], bytes):
                    val: str = obj[index].decode()
                    val = val.replace(old, new)
                    obj[index] = val.encode()
                else:
                    self.__recursive_replace(old, new, obj[index])
