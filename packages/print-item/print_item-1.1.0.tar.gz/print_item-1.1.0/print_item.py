"""This is print_item.py module, which print item that may contain nested collection"""


def print_item(items, level):
    if not isinstance(items, list):
        for i in range(level):
            print('\t', end='')
        print(items)
    else:
        for i in items:
            print_item(i, level + 1)
