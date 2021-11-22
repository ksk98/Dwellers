from itertools import zip_longest

from ansiwrap import ansilen

from settings import settings
from views.colors_enum import Color


class PrintUtility:
    @staticmethod
    def print_dividing_line():
        """
        Prints character few times in order to fill whole line
        """
        width = settings["MAX_WIDTH"]
        indx = 0
        while indx < width:
            print('-', end='')
            indx += 1
        print()

    @staticmethod
    def print_in_columns(column_list: list[list[str]], equal_size: bool = False):
        """
        Prints nice table. Handles any amount of columns.
        Takes list of lists as an argument - each list will be a single column and should contain strings (records).
        :param column_list: list of columns to print
        :param equal_size: determines if each column should have equal size or take only as much space as needed
        """
        width = settings["MAX_WIDTH"]

        # Divide width equally
        column_width = int(width / len(column_list))
        # Store all unused space
        width_excess = width - (column_width * len(column_list))

        length_list = []
        if not equal_size:
            # Get preferred length for each column
            columns_that_need_more_space = 0
            # Each column can give away unnecessary space to be used by columns that need them
            for column in column_list:
                max_width = PrintUtility._get_length_of_longest_element(column) + 2
                length_list.append(max_width)
                if max_width <= column_width:
                    width_excess += (column_width - max_width)
                else:
                    columns_that_need_more_space += 1

            # Determine portion of width_excess for each column that needs it
            width_portion = 0
            if columns_that_need_more_space != 0:
                width_portion = int(width_excess / columns_that_need_more_space)
            # TODO ADD REST TO LAST COLUMN

            # Set lengths
            for indx, length in enumerate(length_list):
                if length > column_width:
                    length_list[indx] = column_width + width_portion
        else:
            # All columns have equal size independently of their length
            for column in column_list:
                length_list.append(column_width)

        # Header of the table will be in bold
        header = True
        # Go through all columns row by row
        for row in zip_longest(*column_list, fillvalue=""):

            # Divide all records by length of their column
            divided_records = []
            for record_line, length in zip_longest(row, length_list):
                divided_records.append(PrintUtility.divide_if_too_long(record_line, length))

            # Go through whole row line by line
            for divided_row in zip_longest(*divided_records, fillvalue=""):
                for record_line, length in zip_longest(divided_row, length_list):
                    if header:
                        print(PrintUtility.ljust("§1" + record_line + "§0", length), end='')
                    else:
                        print(PrintUtility.ljust(record_line, length), end='')
                print()
            header = False

    @staticmethod
    def _get_length_of_longest_element(str_list: list[str]) -> int:
        """
        Returns length of the longest element in the list
        :param str_list: list to check
        :return: length of the longest element
        """
        longest = 0
        for element in str_list:
            if len(element) > longest:
                longest = len(element)
        return longest

    @staticmethod
    def divide_if_too_long(text: str, width: int = 0) -> list[str]:
        """
        Checks if given text is too wide to be printed in one line,
        if the string is too long, it is divided into multiple strings
        that have len() < width.
        Strings are divided at:
         - position of the last space (" ")
         - position of the character that won't fit in current line
        :param text:    to be divided
        :param width:   custom width
        :return: list of strings - each containing single line that will fit in the width cap
        """
        text = PrintUtility.insert_color_codes(text)
        if width == 0:
            width = settings["MAX_WIDTH"]  # this as a default parameter will not refresh
        if ansilen(text) > width:
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
                list += PrintUtility.divide_if_too_long(rest, width)
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
                list += PrintUtility.divide_if_too_long(rest, width)
                # And return it
                return list
        else:
            return [text]

    @staticmethod
    def print_with_dividing(text: str, rjust: bool = False, width: int = 0):
        """
        Prints text on screen, if the text is too long to fit on the screen,
        it is divided into multiple lines and then printed.
        Printed text is justified to the left by default. You can change that by setting rjust = True
        :param text: text to be printed
        :param rjust: text will be justified to the right if True
        :param width: custom width for rjust, settings["MAX_WIDTH"] by default
        """
        if width == 0:
            width = settings["MAX_WIDTH"]

        list = PrintUtility.divide_if_too_long(text)
        for line in list:
            if rjust:
                print(PrintUtility.rjust(line, width))
            else:
                print(PrintUtility.insert_color_codes(line))

    @staticmethod
    def insert_color_codes(text: str) -> str:
        """
        Replaces color labels (e.g. §b) with it's ANSI code.
        :param text: text to insert color codes
        :return: modified text
        """
        while True:
            indx = text.find("§")
            if indx == -1 or indx == len(text) - 1:
                break

            label = text[indx + 1]
            color_code = Color.get_value(label)

            text = text.replace("§" + label, color_code)
        return text

    @staticmethod
    def rjust(text: str, width: int = 0) -> str:
        """
        Justifies text to the right, but length of ANSI escape characters is not taken into count
        :param text: text to justify
        :param width:  target width of text
        :return: Modified text
        """
        if width == 0:
            # this can't be as default parameter, because it will not refresh
            width = settings["MAX_WIDTH"]
        text = PrintUtility.insert_color_codes(text)
        needed = len(text) - ansilen(text)
        return text.rjust(width + needed)

    @staticmethod
    def ljust(text: str, width: int = 0) -> str:
        """
        Justifies text to the left, but length of ANSI escape characters is not taken into count
        :param text: text to justify
        :param width:  target width of text
        :return: Modified text
        """
        if width == 0:
            # this can't be as default parameter, because it will not refresh
            width = settings["MAX_WIDTH"]
        text = PrintUtility.insert_color_codes(text)
        needed = len(text) - ansilen(text)
        return text.ljust(width + needed)

    @staticmethod
    def center(text: str, width: int = 0) -> str:
        """
        Centers text, but length of ANSI escape characters is not taken into count
        :param text: text to justify
        :param width:  target width of text
        :return: Modified text
        """
        if width == 0:
            width = settings["MAX_WIDTH"]
        text = PrintUtility.insert_color_codes(text)
        needed = len(text) - ansilen(text)
        return text.center(width + needed)
