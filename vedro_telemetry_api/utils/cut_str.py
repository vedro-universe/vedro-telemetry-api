__all__ = ("cut_str",)


def cut_str(string: str, length: int, separator: str = "..") -> str:
    """
    Truncate a string to a specified length, inserting a separator if necessary.

    This function shortens the input string to a specified maximum length, inserting
    a separator (default: "..") in the middle if the string exceeds the allowed length.
    The separator replaces the middle part of the string, while preserving the start
    and end portions.

    :param string: The input string to be truncated.
    :param length: The maximum allowed length of the string, including the separator.
                   Must be greater than the length of the separator.
    :param separator: The string to insert in the middle when truncating. Defaults to "..".
    :return: The original string if it is within the specified length, or a truncated version
             with the separator inserted if it exceeds the maximum length.
    :raises ValueError: If the `length` is less than or equal to the length of the separator.
                        The message will indicate that the length must exceed the separator length.
    """
    if length <= len(separator):
        raise ValueError("Length must be greater than the length of the separator")

    if len(string) <= length:
        return string

    length -= len(separator)
    return string[:length // 2] + separator + string[-length // 2:]
