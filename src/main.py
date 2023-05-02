import io_reader
import file_reader
import prototypes_parser
import argparse


if __name__ == '__main__':
    argument_parser = argparse.ArgumentParser(
        prog='C++ prototype parser',
        description='Parser, lexer and tokenizer of C++ function prototypes',
        epilog='I love u iu6 bmstu!'
    )

    argument_parser.add_argument(
        '-f', '--file',
        action='store',
        dest='filename'
    )
    argument_parser.add_argument(
        '-d', '--debug',
        action='store_true'
    )

    arguments = argument_parser.parse_args()
    debug = arguments.debug

    if arguments.filename is not None:
        file_reader = file_reader.FileReader(arguments.filename)
        input_prototypes = file_reader.get_prototypes_list()
    else:
        end_line = input('Какую строку использовать как ограничитель для окончания ввода? ')
        io_reader = io_reader.IOReader(end_line)
        input_prototypes = io_reader.get_prototypes_list()

    parser = prototypes_parser.PrototypesParser(input_prototypes, debug)
