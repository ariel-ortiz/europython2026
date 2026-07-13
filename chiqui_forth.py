from os.path import splitext
from sys import argv, stderr, exit
from wasmtime import wat2wasm


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


def declare_vars(vars):
    result = []
    for var in sorted(vars):
        result.append(f'    (local ${var} i32)')
    return result


def code_generation(tokens):
    result = []
    for token in tokens:
        if is_number(token):
            result.append(f'    i32.const {token}')
        elif token in OPERATION:
            for statement in OPERATION[token]:
                result.append(f'    {statement}')
        elif is_var_name(token):
            result.append(f'    local.get ${token}')
        elif token[-1] == '!' and is_var_name(token[:-1]):
            result.append(f'    local.set ${token[:-1]}')
        else:
            print(f"Error: '{token}' is not a valid word.",
                  file=stderr)
            exit(1)
    return result


WAT_TEMPLATE = ''';; chiqui_forth compiler WAT output

(module
  (import "forth" "emit" (func $emit (param i32)))
  (import "forth" "input" (func $input (result i32)))
  (import "forth" "print" (func $print (param i32)))
  (func (export "_start")
{}
  )
)'''


def create_target_files(source_path, compiled_lines):
    base_name, _ = splitext(source_path)
    wat_source = WAT_TEMPLATE.format('\n'.join(compiled_lines))
    with open(f'{base_name}.wat', 'w') as file:
        file.write(wat_source)
    with open(f'{base_name}.wasm', 'wb') as file:
        file.write(wat2wasm(wat_source))


def main():
    """Control all the steps carried out by the compiler."""

    # === FRONT END ===
    source_path = get_source_filepath()
    raw_tokens = read_words(source_path)
    tokens = remove_comments(raw_tokens)

    # === BACK END ===
    variable_declarations = declare_vars(find_vars_used(tokens))
    instruction_body = code_generation(tokens)
    compiled_lines = variable_declarations + instruction_body
    create_target_files(source_path, compiled_lines)


if __name__ == '__main__':
    main()
