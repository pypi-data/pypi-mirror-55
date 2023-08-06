'''
this is file comment
'''


def print_lol(data):
    for item in data:
        if isinstance(item, list):
            print_lol(item)
        else:
            print(item)


if __name__ == "__main__":
    cast = ["Cleese", "Palin", 'Jone', ['a', 'b', ['c1', 'c2']]]
    print_lol(cast)
