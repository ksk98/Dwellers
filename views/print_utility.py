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
    Prints two lists in separate columns. If both values are too wide to be printed in the same line,
    left one will be printed first, and the right one in the next line (but justified to the right)
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
                print_with_dividing(left)
                rest = width    # whole new line for the right element

            print_with_dividing(right, rjust=True, width=rest)

        rcol_len = len(right_column_elements)
        lcol_len = len(left_column_elements)

        # Print rest of the left column
        if lcol_len > rcol_len:
            for x in range(rcol_len, lcol_len):
                print_with_dividing(left_column_elements[x])

        # Print rest of the right column
        else:
            for x in range(lcol_len, rcol_len):
                print_with_dividing(right_column_elements[x], rjust=True, width=width)


def divide_if_too_long(text: str) -> list[str]:
    """
    Checks if given text is too wide to be printed in one line,
    if the string is too long, it is divided into multiple strings
    that have len() < MAX_WIDTH.
    Strings are divided at:
     - position of the last space (" ")
     - position of the character that won't fit in current line
    :param text:    to be divided
    :return: list of strings - each containing single line that will fit in the MAX_WIDTH cap
    """
    width = settings["MAX_WIDTH"]
    if len(text) > width:
        # Search for the last indx in the line
        indx = text.rfind(" ", 0, width)
        if indx >= 0:
            # First line is ready
            line = text[:indx]
            # So add it to the list
            list: list[str] = [line]
            # Rest may be too long
            rest = text[indx+1:]
            # So check it and then append to the list
            list += divide_if_too_long(rest)
            # And return it
            return list
        else:
            # Cut it at the last character
            line = text[:width]
            # So add it to the list
            list: list[str] = [line]
            # Rest may be too long
            if text[width] != " ":
                rest = text[width:]
            else:
                rest = text[width+1:]
            # So check it and then append to the list
            list += divide_if_too_long(rest)
            # And return it
            return list
    else:
        return [text]


def print_with_dividing(text: str, rjust: bool = False, width: int = settings["MAX_WIDTH"]):
    """
    Prints text on screen, if the text is too long to fit on the screen,
    it is divided into multiple lines and then printed.
    Printed text is justified to the left by default. You can change that by setting rjust = True
    :param text: text to be printed
    :param rjust: text will be justified to the right if True
    :param width: custom width for rjust, settings["MAX_WIDTH"] by default
    """
    list = divide_if_too_long(text)
    for line in list:
        if rjust:
            print(line.rjust(width))
        else:
            print(line)
