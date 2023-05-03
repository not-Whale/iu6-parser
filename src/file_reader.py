class FileReader:
    def __init__(self, path):
        self.path_to_file = path
        self.prototypes_list = []
        self.__parse()

    def get_prototypes_list(self):
        return self.prototypes_list

    def __parse(self):
        with open(self.path_to_file) as input_file:
            self.prototypes_list = list(map(lambda x: x.replace('\n', ''), input_file.readlines()))
