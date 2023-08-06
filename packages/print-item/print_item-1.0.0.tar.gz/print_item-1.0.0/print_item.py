"""This is print_item.py module, which print item that may contain nested collection"""


def print_item(items):
    if not isinstance(items, list):
        print(items)
    else:
        for i in items:
            print_item(i)
