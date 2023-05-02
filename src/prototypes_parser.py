from consts import *
import re


class PrototypesParser:
    def __init__(self, prototypes_list, debug=False):
        self.debug_mode = debug
        self.parsed_prototypes_list = []
        self.prototypes_list = prototypes_list
        self.current_prototype_string = ''
        self.index = 0
        self.__parse()

    def get_parsed_prototypes_list(self):
        return self.parsed_prototypes_list

    def __parse(self):
        for prototype_string in self.prototypes_list:
            self.current_prototype_string = prototype_string
            self.index = 0

            prototype, ok = self.__parse_prototype()
            self.parsed_prototypes_list.append(prototype)
            if ok:
                print('\033[32mPrototype "' + prototype_string + '" is correct!')
                print('Tokenize: ' + str(prototype) + '\033[0m')
            else:
                print('\033[31mError in prototype "' + prototype_string + '" !\033[0m')

    def __eat_spaces(self):
        current_token = self.current_prototype_string[self.index]
        while current_token == SPACE_TOKEN:
            self.index += 1
            current_token = self.current_prototype_string[self.index]

    def __parse_prototype(self):
        # print('<prototype>')
        tokens_list = []

        type_token, ok = self.__parse_type()
        if ok:
            tokens_list.extend(type_token)
        else:
            return [], False

        self.__eat_spaces()

        name_token, ok = self.__parse_name()
        if ok:
            tokens_list.extend(name_token)
        else:
            return [], False

        self.__eat_spaces()

        if self.current_prototype_string[self.index] == LEFT_PAREN_TOKEN:
            tokens_list.append(LEFT_PAREN_TOKEN)
            self.index += 1
        else:
            if self.debug_mode:
                print(
                    '\033[33mWarning: "(" expected in rule <prototype> in string "' +
                    self.current_prototype_string +
                    '"\033[0m'
                )
            return [], False

        self.__eat_spaces()

        arguments_list, ok = self.__parse_arguments_list()
        if ok:
            tokens_list.extend(arguments_list)
        else:
            return [], False

        self.__eat_spaces()

        if self.current_prototype_string[self.index] == RIGHT_PAREN_TOKEN:
            tokens_list.append(RIGHT_PAREN_TOKEN)
            self.index += 1
        else:
            if self.debug_mode:
                print(
                    '\033[33mWarning: ")" expected in rule <prototype> in string "' +
                    self.current_prototype_string +
                    '"\033[0m'
                )
            return [], False

        self.__eat_spaces()

        if self.current_prototype_string[self.index] == SEMICOLON_TOKEN:
            tokens_list.append(SEMICOLON_TOKEN)
            self.index += 1
        else:
            if self.debug_mode:
                print(
                    '\033[33mWarning: ";" expected in rule <prototype> in string "' +
                    self.current_prototype_string +
                    '"\033[0m'
                )
            return [], False

        return tokens_list, True

    def __parse_type(self):
        # print('<type>')
        tokens_list = []

        sign_token, ok = self.__parse_sign()
        if ok:
            tokens_list.extend(sign_token)

            self.__eat_spaces()

            integer_name_token, ok = self.__parse_integer_name()
            if ok:
                tokens_list.extend(integer_name_token)
                return tokens_list, True
            else:
                if self.debug_mode:
                    print(
                        '\033[33mWarning: <integer_name> expected in rule <type> in string "' +
                        self.current_prototype_string +
                        '"\033[0m'
                    )
                return [], False

        integer_name_token, ok = self.__parse_integer_name()
        if ok:
            tokens_list.extend(integer_name_token)
            return tokens_list, True

        not_integer_name_token, ok = self.__parse_not_integer_name()
        if ok:
            tokens_list.extend(not_integer_name_token)
            return tokens_list, True

        if self.debug_mode:
            print(
                '\033[33mWarning: <sign> <integer_name> or <(not_)integer_name> expected in rule <type> in string "' +
                self.current_prototype_string +
                '"\033[0m'
            )
        return [], False

    def __parse_name(self):
        # print('<name>')
        tokens_list = []

        name_token, ok = self.__find_and_get_name_token()
        if ok:
            tokens_list.append(name_token)
            return tokens_list, True
        else:
            if self.debug_mode:
                print(
                    '\033[33mWarning: [a-zA-Z][a-zA-Z0-9_]* expected in rule <name> in string "' +
                    self.current_prototype_string +
                    '"\033[0m'
                )
            return [], False

    def __parse_not_empty_arguments_list(self):
        pass

    def __parse_arguments_list(self):
        # print('<args_list>')
        tokens_list = []

        if self.current_prototype_string[self.index] == SEMICOLON_TOKEN \
                or self.index < len(self.current_prototype_string) - 1 \
                and self.current_prototype_string[self.index] == RIGHT_PAREN_TOKEN \
                and self.current_prototype_string[self.index + 1] == SEMICOLON_TOKEN:
            return tokens_list, True

        argument_tokens, ok = self.__parse_argument()
        if ok:
            tokens_list.extend(argument_tokens)
            self.__eat_spaces()
        else:
            if self.debug_mode:
                print(
                    '\033[33mWarning: <argument> expected in rule <arguments_list> in string "' +
                    self.current_prototype_string +
                    '"\033[0m'
                )
            return [], False

        if self.current_prototype_string[self.index] == COMMA_TOKEN:
            tokens_list.append(COMMA_TOKEN)
            self.index += 1

            self.__eat_spaces()

            arguments_list_tokens, ok = self.__parse_arguments_list()
            if ok:
                tokens_list.extend(arguments_list_tokens)
                return tokens_list, True
            else:
                if self.debug_mode:
                    print(
                        '\033[33mWarning: <arguments_list> expected in rule <arguments_list> in string "' +
                        self.current_prototype_string +
                        '"\033[0m'
                    )
                return [], False
        else:
            return tokens_list, True

    def __check_and_read_token(self, token):
        tokens_list = []

        try:
            if self.current_prototype_string.index(token, self.index) == self.index:
                self.index += len(token)
                tokens_list.append(token)
                return tokens_list, True
        except ValueError:
            return [], False

        return [], False

    def __check_and_read_multiple_tokens(self, tokens_list):
        for current_token in tokens_list:
            token, ok = self.__check_and_read_token(current_token)
            if ok:
                return token, ok

        return [], False

    def __parse_sign(self):
        # print('<sign>')
        token, ok = self.__check_and_read_multiple_tokens([
            UNSIGNED_TOKEN,
            SIGNED_TOKEN
        ])
        if ok:
            return token, ok

        if self.debug_mode:
            print(
                '\033[33mWarning: "(un)signed" expected in rule <sign> in string "' +
                self.current_prototype_string +
                '"\033[0m'
            )
        return [], False

    def __parse_integer_name(self):
        # print('<integer_name>')
        token, ok = self.__check_and_read_multiple_tokens([
            INT_TOKEN,
            CHAR_TOKEN,
            SHORT_TOKEN
        ])
        if ok:
            return token, ok

        first_long_token, ok = self.__check_and_read_token(LONG_TOKEN)
        if ok:
            self.__eat_spaces()

            second_long_token, second_ok = self.__check_and_read_token(LONG_TOKEN)
            if ok:
                return [first_long_token, second_long_token], second_ok
            else:
                return first_long_token, ok
        else:
            if self.debug_mode:
                print(
                    '\033[33mWarning: "int" or "char" or "short" or "long" or "long long" '
                    'expected in rule <integer_name> in string "' +
                    self.current_prototype_string +
                    '"\033[0m'
                )
            return [], False

    def __parse_not_integer_name(self):
        # print('<not_integer_name>')
        token, ok = self.__check_and_read_multiple_tokens([
            FLOAT_TOKEN,
            DOUBLE_TOKEN,
            BOOL_TOKEN
        ])
        if ok:
            return token, ok

        long_token, ok = self.__check_and_read_token(LONG_TOKEN)
        if ok:
            self.__eat_spaces()

            second_double_token, second_ok = self.__check_and_read_token(DOUBLE_TOKEN)
            if second_ok:
                return [long_token, second_double_token], second_ok
            else:
                if self.debug_mode:
                    print(
                        '\033[33mWarning: "float" or "double" or "bool" or "long double" '
                        'expected in rule <not_integer_name> in string "' +
                        self.current_prototype_string +
                        '"\033[0m'
                    )
                return [], False
        else:
            if self.debug_mode:
                print(
                    '\033[33mWarning: "float" or "double" or "bool" or "long double" '
                    'expected in rule <not_integer_name> in string "' +
                    self.current_prototype_string +
                    '"\033[0m'
                )
            return [], False

    def __parse_argument(self):
        # print('<argument>')
        tokens_list = []

        type_tokens, ok = self.__parse_type()
        if ok:
            tokens_list.extend(type_tokens)
        else:
            if self.debug_mode:
                print(
                    '\033[33mWarning: <type> expected in rule <argument> in string "' +
                    self.current_prototype_string +
                    '"\033[0m'
                )
            return [], False

        self.__eat_spaces()

        name_token, ok = self.__parse_name()
        if ok:
            tokens_list.extend(name_token)
        else:
            if self.debug_mode:
                print(
                    '\033[33mWarning: <name> expected in rule <argument> in string "' +
                    self.current_prototype_string +
                    '"\033[0m'
                )
            return [], False

        return tokens_list, True

    def __find_and_get_name_token(self):
        current_name = ''

        current_char = self.current_prototype_string[self.index]
        if re.match(r"[a-zA-Z]", current_char):
            current_name += current_char
            self.index += 1
        else:
            if self.debug_mode:
                print(
                    '\033[33mWarning: [a-zA-Z] expected in rule <name> in string "' +
                    self.current_prototype_string +
                    '"\033[0m'
                )
            return '', False

        current_char = self.current_prototype_string[self.index]
        while current_char != SPACE_TOKEN \
                and current_char != COMMA_TOKEN \
                and current_char != LEFT_PAREN_TOKEN \
                and current_char != RIGHT_PAREN_TOKEN:
            if re.match(r"[a-zA-Z0-9_]", current_char):
                current_name += current_char
                self.index += 1
                current_char = self.current_prototype_string[self.index]
            else:
                if self.debug_mode:
                    print(
                        '\033[33mWarning: [a-zA-Z0-9_]* expected in rule <name> in string "' +
                        self.current_prototype_string +
                        '"\033[0m'
                    )
                return '', False

        return current_name, True
