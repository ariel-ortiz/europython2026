from sys import argv, stderr, exit

def get_source_filepath():
    if (len(argv) != 2):
        print('Please specify the name of the chiqui_forth source file.')
        exit(1)
    return argv[1]


def main():
    print(get_source_filepath())


if __name__ == '__main__':
    main()
