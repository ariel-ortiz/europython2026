from sys import argv, stderr, exit

def get_source_filepath():
    if (len(argv) != 2):
        print('Please specify the name of the chiqui_forth source file.',
              file=stderr)
        exit(1)
    return argv[1]


def read_words(input_file_name):
    try:
        with open(input_file_name) as source_file:
            source = source_file.read()
        return source.split()
    except FileNotFoundError:
        print(f'Oops! File not found: {input_file_name}',
              file=stderr)
        exit(1)


def remove_comments(tokens):
    result = []
    inside_comment = False
    for token in tokens:
        if inside_comment:
            if token == ')':
                inside_comment = False
        elif token == '(':
            inside_comment = True
        elif token == ')':
            print("Error: Unmatched closing parenthesis ')' found outside of a comment block.",
                  file=stderr)
            exit(1)
        else:
            result.append(token)
    if inside_comment:
        print("Error: End of input reached while searching for closing ')' delimiter.",
              file=stderr)
        exit(1)
    return result


OPERATION = {
    '*': ['i32.mul'],
    '+': ['i32.add'],
    '.': ['call $print'],
    'emit': ['call $emit'],
    'input': ['call $input'],
    'nl': [
        'i32.const 10',
        'call $emit'
    ],
}


def is_var_name(token):
    return (token[0].isalpha()
            and token.isalnum()
            and token not in OPERATION)


def is_number(token):
    return token.removeprefix('-').isdigit()


def find_vars_used(tokens):
    names = set()
    for token in tokens:
        name = token[:-1] if token[-1] == '!' else token
        if is_var_name(name):
            names.add(name)
    return names


def main():
    print(remove_comments(read_words(get_source_filepath())))


if __name__ == '__main__':
    main()
