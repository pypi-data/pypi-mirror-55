import re


class Interface:
    def __init__(self, title_program, additional_message, pattern_name, data_type, main_algorithm):

        # Some Global variables
        self.author = 'Будзінський Є. О. КМ-91'  # Name of Author
        self.end_message = 'Дякуємо, що обираєте нас <3'  # Message which show when program is end

        self.decor_sign = '='  # Symbol which used for decorate text
        self.equal_symbol = '='  # Symbol for equal in enter message

        self.separator = ' '  # Separator for element in string
        self.anti_separator = ''  # Anti-Separator

        self.true_button = 'y'  # Button which read as True value
        self.false_button = 'n'  # Button which read as False value

        self.start_message = 'Бажаєте розпочати тестування? Y/N '  # Value start message
        self.continue_message = 'Бажаєте продовжити тестування? Y/N '  # Value continue message

        self.type_error = '▲ Помилковий тип введених даних'  # Message for inform about type error
        self.error_message = '▲ Введені дані не задовільняють умову'  # Message for inform about some local error
        self.critical_error = 'Something went wrong. Critical ERROR.'  # Message for inform about global error

        self.title = title_program  # Value title of program
        self.sub_message = additional_message  # Value of additional message (optionally)

        self.pattern = pattern_name  # Array with names of variables
        self.typeof = data_type  # What type all of variables (REMADE)

        # Some Regular Expressions
        self.regular_float_check = '^-?[0-9]+(\\.[0-9]+)?$'
        self.regular_int_check = '^[0-9]+$'
        self.regular_int_check_neg = '^-?[0-9]+$'

        self.algorithm = main_algorithm  # Name of Main Algorithm

    def hello(self):
        """
        Вітання з користувачем
        :return: str, string, 'hello user'
        """
        k = max(len(self.author), len(self.title))
        print("{d}\n{t}\n{a}\n{d}".format(a=self.author, t=self.title, d=self.decor_sign * k))

    def bye(self):
        """
        Прощання з користувачем
        :return: str, string, 'bye user'
        """
        exit('\n{d}\n{m}\n{d}'.format(m=self.end_message, d=self.decor_sign * len(self.end_message)))

    def waiter(self, input_message):
        """
        Функція очікування дій користувача
        :param input_message: str, string, 'Бажаєте розпочати тетстування'
        :return: bool, True/False, True
        """
        pressed_button = input(input_message)  # Отримання натиснутої кнопки
        if pressed_button.lower() == self.true_button:
            return True
        elif pressed_button.lower() == self.false_button:  # Перевірка яка кнопка була нажата
            return False
        else:
            print(self.type_error)
            return self.waiter(input_message)

    def trim(self, string):
        """
        Функція що викидає зайві пробіли з вхідного рядка
        :param string: str, string, 'some string with space'
        :return: str, text, 'somestringwithspace'
        """
        if isinstance(string, str):
            array = string.split()
            return self.anti_separator.join(array)
        else:
            exit(self.critical_error)

    def int_check(self, data, negative=False):
        """
        Функція перевірки цілих чисел
        :param data: str, string, 's12'
        :param negative: bool, True/False, True
        :return: bool, True/False, True
        """
        if negative:
            return bool(re.match(self.regular_int_check_neg, data))
        else:
            return bool(re.match(self.regular_int_check, data))

    def float_check(self, data):
        """
        Функція перевірки чисел з плаваючою точкою
        :param data: str, string, 's12'
        :return: bool, True/False, True
        """
        return bool(re.match(self.regular_float_check, data))

    def str_parse(self, data):
        """
        Функція перебору вхідного рядка
        :param data: str, string, ''
        :return:
        """
        array = data.split()
        return self.separator.join(array)

    def cycle_check(self, data_array, element_pattern):
        """
        Рекурсивна заміна While True
        :param data_array: dict, {'key': 'something'}, {'raw': '123'}
        :param element_pattern: array, ['something'], ['str']
        :return: None
        """
        current_data = input("{} {} ".format(element_pattern, self.equal_symbol))
        if current_data:
            trim_current_data = self.trim(current_data)
            if self.typeof == 'str':
                data_array[element_pattern] = self.str_parse(current_data)
            elif self.typeof == 'int':
                if not self.int_check(trim_current_data):
                    print(self.type_error)
                    self.cycle_check(data_array, element_pattern)
                else:
                    data_array[element_pattern] = int(trim_current_data)
            elif self.typeof == 'float':
                if not self.float_check(trim_current_data):
                    print(self.type_error)
                    self.cycle_check(data_array, element_pattern)
                else:
                    data_array[element_pattern] = float(trim_current_data)
        else:
            data_array[element_pattern] = ''

    def get_data(self):
        """
        Функція отримування даних від користувача
        :return: dict, {'key': 'something'}, {'raw': '123'}
        """
        data = {}  # Ініціалізація основного словника
        if self.sub_message:
            print(self.sub_message)
        for p in self.pattern:  # Перебір усіх елементів шаблону
            self.cycle_check(data, p)
        return data

    def start(self):
        """
        Ініціалізація старту інтерфейсу
        :return: None
        """
        self.hello()
        if self.waiter(self.start_message):
            self.main()
        else:
            self.bye()

    def main(self):
        """
        Створення основовної частини інтерфейсу програми
        :return: None
        """
        data = self.get_data()
        self.algorithm(data)
        if self.waiter(self.continue_message):
            self.main()
        else:
            self.bye()
