def print_whole_line_of_char(char: chr, width: int):
    indx = 0
    while indx < width:
        print(char, end='')
        indx += 1
    print()


def print_in_two_columns(column_list: list[list[str]], width: int):
    if len(column_list) == 2:
        left_column_elements = column_list[0]
        right_column_elements = column_list[1]
        for left, right in zip(left_column_elements, right_column_elements):
            elements_length = len(left) + len(right)
            rest = width - elements_length
            if rest > 0:
                print(left, end='')
                for x in range(0, rest):
                    print(' ', end='')
            else:
                print(left)
                for x in range(0, width - len(right)):
                    print(' ', end='')
            print(right)
        if len(left_column_elements) > len(right_column_elements):
            right_len = len(right_column_elements)
            left_len = len(left_column_elements)
            for x in range (right_len, left_len):
                print(left_column_elements[x])
        else:
            right_len = len(right_column_elements)
            left_len = len(left_column_elements)
            for x in range (left_len, right_len):
                for y in range(0, width - len(right_column_elements[x])):
                    print(' ', end='')
                print(right_column_elements[x])
