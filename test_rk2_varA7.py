import unittest
from rk2_varA7 import (
    Computer,
    Microprocessor,
    MicroprocessorComputer,
    DataService
)


class TestDataService(unittest.TestCase):

    def setUp(self):
        self.computers = [
            Computer(1, 'отдел кадров'),
            Computer(2, 'архивный отдел'),
            Computer(3, 'бухгалтерия'),
        ]

        self.microprocessors = [
            Microprocessor(1, 'Intel Core i7', 3700, 1),
            Microprocessor(2, 'Intel Core i5', 3200, 2),
            Microprocessor(3, 'Intel Xeon', 4200, 3),
        ]

        self.relations = [
            MicroprocessorComputer(1, 1),
            MicroprocessorComputer(2, 2),
            MicroprocessorComputer(3, 3),
        ]

        self.service = DataService()

    def test_create_one_to_many_relation(self):
        result = self.service.create_one_to_many_relation(
            self.computers, self.microprocessors
        )

        self.assertEqual(len(result), 3)

        expected_data = [
            ('Intel Core i7', 3700, 'отдел кадров'),
            ('Intel Core i5', 3200, 'архивный отдел'),
            ('Intel Xeon', 4200, 'бухгалтерия'),
        ]

        for expected, actual in zip(expected_data, result):
            self.assertEqual(expected[0], actual[0])
            self.assertEqual(expected[1], actual[1])
            self.assertEqual(expected[2], actual[2])

    def test_task_a1_one_to_many_sorted(self):
        test_data = [
            ('AMD Ryzen', 3500, 'бухгалтерия'),
            ('Intel Core i7', 3700, 'отдел кадров'),
            ('Intel Core i5', 3200, 'архивный отдел'),
        ]

        result = self.service.task_a1_one_to_many_sorted(test_data)

        expected_order = ['архивный отдел', 'бухгалтерия', 'отдел кадров']
        actual_order = [item[2] for item in result]

        self.assertEqual(expected_order, actual_order)
        self.assertEqual(len(result), 3)

    def test_task_a2_computers_total_frequency(self):
        test_data = [
            ('Intel Core i7', 3700, 'отдел кадров'),
            ('Intel Core i5', 3200, 'архивный отдел'),
            ('Intel Xeon', 4200, 'бухгалтерия'),
            ('AMD Ryzen 7', 3800, 'бухгалтерия'),
        ]

        test_computers = [
            Computer(1, 'отдел кадров'),
            Computer(2, 'архивный отдел'),
            Computer(3, 'бухгалтерия'),
        ]

        result = self.service.task_a2_computers_total_frequency(
            test_data, test_computers
        )

        self.assertEqual(len(result), 3)

        expected_results = {
            'бухгалтерия': 8000,
            'отдел кадров': 3700,
            'архивный отдел': 3200,
        }

        for computer_name, total_freq in result:
            self.assertEqual(expected_results[computer_name], total_freq)

        frequencies = [freq for _, freq in result]
        self.assertEqual(frequencies, sorted(frequencies, reverse=True))

    def test_task_a3_computers_with_department_and_microprocessors(self):
        test_computers = [
            Computer(1, 'отдел кадров'),
            Computer(2, 'архивный отдел'),
            Computer(3, 'бухгалтерия'),
            Computer(4, 'отдел разработки'),
        ]

        test_many_to_many = [
            ('Intel Core i7', 3700, 'отдел кадров'),
            ('Intel Core i5', 3200, 'архивный отдел'),
            ('Intel Xeon', 4200, 'бухгалтерия'),
            ('AMD Ryzen 7', 3800, 'отдел кадров'),
            ('AMD Ryzen 5', 3400, 'отдел разработки'),
        ]

        result = self.service.task_a3_computers_with_department_and_microprocessors(
            test_computers, test_many_to_many
        )

        self.assertEqual(len(result), 3)
        self.assertIn('отдел кадров', result)
        self.assertIn('архивный отдел', result)
        self.assertIn('отдел разработки', result)
        self.assertNotIn('бухгалтерия', result)

        expected_microprocessors = ['Intel Core i7', 'AMD Ryzen 7']
        self.assertEqual(sorted(result['отдел кадров']), sorted(expected_microprocessors))

    def test_create_many_to_many_relation(self):
        result = self.service.create_many_to_many_relation(
            self.computers, self.microprocessors, self.relations
        )

        self.assertEqual(len(result), 3)

        for item in result:
            self.assertIsInstance(item, tuple)
            self.assertEqual(len(item), 3)
            self.assertIsInstance(item[0], str)
            self.assertIsInstance(item[1], int)
            self.assertIsInstance(item[2], str)


if __name__ == '__main__':
    unittest.main(verbosity=2)