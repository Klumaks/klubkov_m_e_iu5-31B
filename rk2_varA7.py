from operator import itemgetter
from typing import List, Dict, Tuple


class Microprocessor:
    def __init__(self, id: int, model: str, frequency: int, computer_id: int):
        self.id = id
        self.model = model
        self.frequency = frequency
        self.computer_id = computer_id


class Computer:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name


class MicroprocessorComputer:
    def __init__(self, computer_id: int, microprocessor_id: int):
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


class DataService:

    @staticmethod
    def create_one_to_many_relation(
            computers_list: List[Computer],
            microprocessors_list: List[Microprocessor]
    ) -> List[Tuple[str, int, str]]:
        return [
            (m.model, m.frequency, c.name)
            for c in computers_list
            for m in microprocessors_list
            if m.computer_id == c.id
        ]

    @staticmethod
    def create_many_to_many_relation(
            computers_list: List[Computer],
            microprocessors_list: List[Microprocessor],
            relations_list: List[MicroprocessorComputer]
    ) -> List[Tuple[str, int, str]]:
        many_to_many_temp = [
            (c.name, mc.computer_id, mc.microprocessor_id)
            for c in computers_list
            for mc in relations_list
            if c.id == mc.computer_id
        ]

        return [
            (m.model, m.frequency, comp_name)
            for comp_name, comp_id, micro_id in many_to_many_temp
            for m in microprocessors_list if m.id == micro_id
        ]

    @staticmethod
    def task_a1_one_to_many_sorted(
            one_to_many_data: List[Tuple[str, int, str]]
    ) -> List[Tuple[str, int, str]]:
        return sorted(one_to_many_data, key=itemgetter(2))

    @staticmethod
    def task_a2_computers_total_frequency(
            one_to_many_data: List[Tuple[str, int, str]],
            computers_list: List[Computer]
    ) -> List[Tuple[str, int]]:
        result_unsorted = []

        computer_groups = {}
        for m_model, m_freq, c_name in one_to_many_data:
            if c_name not in computer_groups:
                computer_groups[c_name] = []
            computer_groups[c_name].append(m_freq)

        for c_name, frequencies in computer_groups.items():
            total_frequency = sum(frequencies)
            result_unsorted.append((c_name, total_frequency))

        return sorted(result_unsorted, key=itemgetter(1), reverse=True)

    @staticmethod
    def task_a3_computers_with_department_and_microprocessors(
            computers_list: List[Computer],
            many_to_many_data: List[Tuple[str, int, str]]
    ) -> Dict[str, List[str]]:
        result = {}

        for computer in computers_list:
            if 'отдел' in computer.name.lower():
                computer_microprocessors = [
                    m_model
                    for m_model, m_freq, comp_name in many_to_many_data
                    if comp_name == computer.name
                ]
                result[computer.name] = computer_microprocessors

        return result


def main():
    service = DataService()

    one_to_many = service.create_one_to_many_relation(computers, microprocessors)
    many_to_many = service.create_many_to_many_relation(
        computers, microprocessors, microprocessors_computers
    )

    print('Задание A1')
    print('Список всех связанных микропроцессоров и компьютеров, отсортированный по компьютерам:')
    task1_result = service.task_a1_one_to_many_sorted(one_to_many)
    for item in task1_result:
        print(f'Микропроцессор: {item[0]}, Частота: {item[1]}, Компьютер: {item[2]}')

    print('\n' + '=' * 50 + '\n')

    print('Задание A2')
    print('Список компьютеров с суммарной частотой микропроцессоров, отсортированный по суммарной частоте:')
    task2_result = service.task_a2_computers_total_frequency(one_to_many, computers)
    for item in task2_result:
        print(f'Компьютер: {item[0]}, Суммарная частота: {item[1]}')

    print('\n' + '=' * 50 + '\n')

    print('Задание A3')
    print('Список всех компьютеров с "отдел" в названии и их микропроцессоры:')
    task3_result = service.task_a3_computers_with_department_and_microprocessors(
        computers, many_to_many
    )
    for computer_name, microprocessors_list in task3_result.items():
        print(f'Компьютер: {computer_name}')
        print(f'  Микропроцессоры: {", ".join(microprocessors_list)}')


if __name__ == '__main__':
    main()