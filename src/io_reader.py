class IOReader:
    def __init__(self, end_line=''):
        self.prototypes_list = []
        self.end_line = end_line
        self.__read()

    def get_prototypes_list(self):
        return self.prototypes_list

    def __read(self):
        print('\033[33mЧтобы закончить ввод подайте на вход "' + self.end_line + '"!\033[0m')
        while True:
            current_prototype = input('Объявление: ')
            if current_prototype == self.end_line:
                break
            self.prototypes_list.append(current_prototype)
