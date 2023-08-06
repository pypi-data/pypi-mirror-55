from unittest import TestCase

from scripts.helpers import commons
from scripts.helpers import logger_aditional_info


class TestShowStepInfo(TestCase):

    def setUp(self) -> None:
        def some_test_function():
            pass

    # def check_additional_info_decorator(self):
    #     self.assertEqual(logger_additional_info(self.some_test_function))


class TestCommons(TestCase):
    def setUp(self) -> None:
        self.test_cases_for_acronyms = [
            ['nation', 'NATION'],
            ['', ''],
            ['Census Tract', 'CT'],
            [
                'verylongstringwithoutanymeaning',
                'VERYLONGSTRINGWITHOUTANYMEANING',
            ],
            ['STATE', 'STATE'],
            ['COUNTY SUBDIVISION', 'CS'],
            ['999999999', '999999999'],
            ['00000 444444 222222', '042'],
            [42, '42'],
        ]

        self.test_cases_for_data_types = [
            [3, 'int'],
            [2, 'float'],
            [1, 'char'],
            [None, 'STATE'],
            [None, 'CS'],
            [None, '999999999'],
        ]

    def test_create_acronym(self):
        for case in self.test_cases_for_acronyms:
            self.assertEqual(commons.create_acronym(case[0]), case[1])

    def test_check_data_type(self):
        for case in self.test_cases_for_data_types:
            self.assertEqual(commons.check_data_type(case[1]), case[0])

    def test_get_variable_descriptions_from_file(self):
        self.assertNotEqual(
            {'var1': {
                'code': '', 'title': '', 'indent': '', 'category': '',
                'bubble_size_hint': '', 'method': '', 'color_palettes': '',
            }},
            commons.get_variable_descriptions_from_file(
                r'../templates/variable_definitions.csv',
            ),
        )
