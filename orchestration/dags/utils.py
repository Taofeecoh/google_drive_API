
def replace_with_underscore(x: str):
    """
    Function to strip and replace whitespaces between words with _score
    :param x: a string (required)
    :returns: formatted string with underscore(s)
    """
    x = x.strip()
    return x.replace(" ", "_")


def to_snakecase(data_list: list):
    """
    Function to transform list items to snake_case
    :param data_list: takes a list (required)
    :returns: list of items in snake_case
    """
    col = [replace_with_underscore(i.lower()) for i in data_list]
    return col
