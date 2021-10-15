from settings import settings


def print_whole_line_of_char(char: chr):
    """
    Prints character few times in order to fill whole line
    :param char: to be printed
    """
    width = settings["MAX_WIDTH"]
    indx = 0
    while indx < width:
        print(char, end='')
        indx += 1
    print()


def print_in_two_columns(column_list: list[list[str]]):
    """
    Prints two lists in separate columns
    :param column_list:
    """
    width = settings["MAX_WIDTH"]
    if len(column_list) == 2:
        left_column_elements = column_list[0]
        right_column_elements = column_list[1]

        # Print both lists until one ends
        for left, right in zip(left_column_elements, right_column_elements):
            rest = width - len(left)
            if rest > len(right): # both values can be printed in the same line
                print(left, end='')
            else:
                # print(divide_if_too_long(left))
                print(left)
                rest = width    # whole new line for the right element

            print(right.rjust(rest))

        rcol_len = len(right_column_elements)
        lcol_len = len(left_column_elements)

        # Print rest of the left column
        if lcol_len > rcol_len:
            for x in range(rcol_len, lcol_len):
                print(left_column_elements[x])

        # Print rest of the right column
        else:
            for x in range(lcol_len, rcol_len):
                print(right_column_elements[x].rjust(width))


def divide_if_too_long(text: str):
    # TODO implement this
    # TODO recursion?
    width = settings["MAX_WIDTH"]
    if len(text) > width:
        # search for the last indx in the line
        indx = text.find(" ", width, 0)
        if indx >= 0:
            return text[:indx] + "\n" + text[indx + 1:]
        else:
            return text[:indx] + "\n" + text[indx:]


