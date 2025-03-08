import logging

def report(line: int, msg: str):
    """
    Logs an error message with the specified line number and message content.

    This function creates a logger instance and logs an error message formatted
    to include the given line number and corresponding message. It is intended
    for use in scenarios where logging error details is necessary.

    :param line: The line number at which the error occurred.
    :type line: int
    :param msg: The error message describing the issue.
    :type msg: str
    :return: None
    """
    logger = logging.getLogger(__name__)
    logger.error(f"line {line}: {msg}")