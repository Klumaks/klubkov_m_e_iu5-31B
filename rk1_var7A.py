from operator import itemgetter


class Microprocessor:
    def __init__(self, id, model, frequency, computer_id):
        self.id = id
        self.model = model
        self.frequency = frequency
        self.computer_id = computer_id


class Computer:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class MicroprocessorComputer:
    def __init__(self, computer_id, microprocessor_id):
        self.computer_id = computer_id
        self.microprocessor_id = microprocessor_id


computers = [
    Computer(1, 'отдел кадров'),
    Computer(2, 'архивный отдел'),
    Computer(3, 'бухгалтерия'),
    Computer(11, 'отдел разработки'),
    Computer(22, 'архивный отдел тестирования'),
    Computer(33, 'бухгалтерия финансов'),
]


microprocessors = [
    Microprocessor(1, 'Intel Core i7', 3700, 1),
    Microprocessor(2, 'Intel Core i5', 3200, 2),
    Microprocessor(3, 'Intel Xeon', 4200, 3),
    Microprocessor(4, 'AMD Ryzen 7', 3800, 3),
    Microprocessor(5, 'AMD Ryzen 5', 3400, 3),
]


microprocessors_computers = [
    MicroprocessorComputer(1, 1),
    MicroprocessorComputer(2, 2),
    MicroprocessorComputer(3, 3),
    MicroprocessorComputer(3, 4),
    MicroprocessorComputer(3, 5),
    MicroprocessorComputer(11, 1),
    MicroprocessorComputer(22, 2),
    MicroprocessorComputer(33, 3),
    MicroprocessorComputer(33, 4),
    MicroprocessorComputer(33, 5),
]


def main():
    one_to_many = [(m.model, m.frequency, c.name)
                   for c in computers
                   for m in microprocessors
                   if m.computer_id == c.id]

    many_to_many_temp = [(c.name, mc.computer_id, mc.microprocessor_id)
                         for c in computers
                         for mc in microprocessors_computers
                         if c.id == mc.computer_id]

    many_to_many = [(m.model, m.frequency, comp_name)
                    for comp_name, comp_id, micro_id in many_to_many_temp
                    for m in microprocessors if m.id == micro_id]

    print('Задание A1')
    print('Список всех связанных микропроцессоров и компьютеров, отсортированный по компьютерам:')
    res_11 = sorted(one_to_many, key=itemgetter(2))
    for item in res_11:
        print(f'Микропроцессор: {item[0]}, Частота: {item[1]}, Компьютер: {item[2]}')

    print('\n' + '=' * 50 + '\n')

    print('Задание A2')
    print('Список компьютеров с суммарной частотой микропроцессоров, отсортированный по суммарной частоте:')
    res_12_unsorted = []

    computer_groups = {}
    for m_model, m_freq, c_name in one_to_many:
        if c_name not in computer_groups:
            computer_groups[c_name] = []
        computer_groups[c_name].append(m_freq)

    for c_name, frequencies in computer_groups.items():
        total_frequency = sum(frequencies)
        res_12_unsorted.append((c_name, total_frequency))

    res_12 = sorted(res_12_unsorted, key=itemgetter(1), reverse=True)
    for item in res_12:
        print(f'Компьютер: {item[0]}, Суммарная частота: {item[1]}')

    print('\n' + '=' * 50 + '\n')

    print('Задание A3')
    print(
        'Список всех компьютеров, у которых в названии присутствует слово "отдел", и список работающих в них микропроцессоров:')
    res_13 = {}

    for c in computers:
        if 'отдел' in c.name.lower():
            c_microprocessors = [m_model for m_model, m_freq, comp_name in many_to_many
                                 if comp_name == c.name]
            res_13[c.name] = c_microprocessors

    for computer_name, microprocessors_list in res_13.items():
        print(f'Компьютер: {computer_name}')
        print(f'  Микропроцессоры: {", ".join(microprocessors_list)}')


if __name__ == '__main__':
    main()