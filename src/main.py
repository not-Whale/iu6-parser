import io_reader
import file_reader
import prototypes_parser

# io_reader = io_reader.IOReader()
file_reader = file_reader.FileReader('./tests/test1.txt')

# input1 = io_reader.get_prototypes_list()
input2 = file_reader.get_prototypes_list()

# print(input1)
print(input2)

parser = prototypes_parser.PrototypesParser(input2, True)
