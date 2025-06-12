
def replace_with_underscore(x: str):
    """
    Function to replace whitespaces between words underscore
    :param x: takes a string (required)
    :returns: formatted string with underscore(s)
    """
    return x.replace(" ", "_")


def first_letters_to_cap(x: str):
    """
    Function to convert every first letter of a word to uppercase
    :param x: takes a string (required)
    :returns: titlecase of words
    """
    return x.title()


def remove_trailing_space(x: str):
    """
    Function to remove trailing whitspaces
    :param x: takes a string (required)
    :returns: formated string with no trailing whitespaces
    """
    return x.strip()


def transform_col_names(data_list: list):
    """
    Function to transform list items to snake case format
    :param data_list: takes a list (required)
    :returns: list of items in snake_case
    """
    new_col = []
    for i in data_list:
        i = remove_trailing_space(i)
        i = replace_with_underscore(i)
        i = first_letters_to_cap(i)
        new_col.append(i)
    return new_col
