import unittest
from scripts.postprocessing_checks import metadata_check

import lxml.etree as et

good_file = r'./res/xml_to_be_checked/good_file.xml'
bad_file = r'./res/xml_to_be_checked/bad_file.xml'
correctxml = r'./res/xml_to_be_checked/correct_metadata.xml'
correctxsd = r'./res/xml_to_be_checked/correct_schema.xsd'
incorrectxml = r'./res/xml_to_be_checked/incorrect_metadata.xml'
incorrectxsd = r'./res/xml_to_be_checked/incorrect_schema.xsd'

tree_my_xml = et.parse(good_file)

system_guid = {
            '2a64633f-f707-4abd-844a-e2184217ef0f': ('survey_element', '/path/survey', 'name_survey.xml'),
            'acb8f93f-34ab-485d-884d-bb278e42d51c': ('survey_element', '/path/survey', 'name_survey.xml')
        }

my_xml_guid = {
    '6c62a09a-34cd-47ef-b6bb-1e5a58813790': ('survey_element', '/path/survey'),
    'ec7bd1e4-00df-4095-a8e8-c62d5f5d8f1c': ('survey_element', '/path/survey')
}

my_xml_guid_same_as_system_guid = {
    '2a64633f-f707-4abd-844a-e2184217ef0f': ('survey_element', '/path/survey'),
    'b42777a6-1f48-43b8-beac-b1283f45f564': ('survey_element', '/path/survey')
}

unique_xml = r'./res/xml_to_be_checked/correct_metadata.xml'
not_unique_xml = r'./res/xml_to_be_checked/not_unique_guid.xml'


class TestClass(unittest.TestCase):

    def test_xml_to_xsd_validation(self):
        self.assertTrue(metadata_check.xml_to_xsd_validation(correctxml, correctxsd))
        self.assertFalse(metadata_check.xml_to_xsd_validation(correctxml, incorrectxsd))
        self.assertFalse(metadata_check.xml_to_xsd_validation(incorrectxml, correctxsd))
        self.assertFalse(metadata_check.xml_to_xsd_validation(correctxsd, correctxml))

        with self.assertRaises(OSError):
            metadata_check.xml_to_xsd_validation(correctxml, './xml_to_be_checked/schema.xsd')
            metadata_check.xml_to_xsd_validation('./xml_to_be_checked/correct_meta.xml', correctxsd)
            metadata_check.xml_to_xsd_validation('', correctxsd)
            metadata_check.xml_to_xsd_validation(correctxml, '')

        with self.assertRaises(AttributeError):
            metadata_check.xml_to_xsd_validation(incorrectxml, 6)
            metadata_check.xml_to_xsd_validation(6, correctxsd)

    def test_guid_uniqueness(self):
        self.assertTrue(metadata_check.guid_uniqueness(system_guid, my_xml_guid))
        self.assertFalse(metadata_check.guid_uniqueness(system_guid, my_xml_guid_same_as_system_guid))

    def test_check_uniqueness_guid_my_xml(self):
        self.assertFalse(metadata_check.check_uniqueness_guid_my_xml(not_unique_xml))
        self.assertTrue(metadata_check.check_uniqueness_guid_my_xml(unique_xml))

    def test_geo_plural_name_singular(self):
        self.assertLogs(metadata_check.geo_plural_name_singular(bad_file),
                        "GEO TYPES PluralName SET AS SINGULAR: ['Nations Area', 'State', 'Census Tract']")
        self.assertLogs(metadata_check.geo_plural_name_singular(good_file))

    def test_geo_labels_plural(self):
        self.assertLogs(metadata_check.geo_labels_plural(bad_file),
                        "GEO TYPES Label SET AS PLURAL:['States']")
        self.assertLogs(metadata_check.geo_labels_plural(good_file))

    def test_geo_types_qlabel_indent(self):
        self.assertLogs(metadata_check.geo_types_qlabel_indent(bad_file),
                        "GEO TYPES QLABEL NOT INDENTED PROPERLY: ['Census Tract']")
        self.assertLogs(metadata_check.geo_types_qlabel_indent(good_file))

    def test_table_suffix_geo_summary(self):
        self.assertLogs(metadata_check.table_suffix_geo_summary(bad_file),
                        "TABLE SUFFIX IN GEOGRAPHY SUMMARY FILE TABLES IS NOT SET IN SOME OF THESE SUFFIXES: "
                        "['Geo', '001']")
        self.assertLogs(metadata_check.table_suffix_geo_summary(good_file))

    def test_table_var_case(self):
        self.assertLogs(metadata_check.table_var_case(bad_file),
                        "TABLE AND VARIABLE LABELS NOT IN TITLE CASE: [['NHS2015_003_AREA11', "
                        "'Area Of Land Cover Class 11, open water'], "
                        "['NHS2015_003', '2011 Data on 2015 Boundaries (square meters)']]")
        self.assertLogs(metadata_check.table_var_case(good_file))

    def test_source_publisher_exist(self):
        self.assertLogs(metadata_check.source_publisher_exist(bad_file),
                        "SOURCE AND PUBLISHER ARE NOT SET PROPERLY.")
        self.assertLogs(metadata_check.source_publisher_exist(good_file))

    def test_survey_name(self):
        self.assertLogs(metadata_check.survey_name(bad_file),
                        "SURVEY NAME NOT REALLY SHORT. MAKE IT SHORTER.")
        self.assertLogs(metadata_check.survey_name(good_file))

    def test_check_if_dollar_year_set(self):
        self.assertLogs(metadata_check.check_if_dollar_year_set(bad_file),
                        "DOLLAR YEAR NOT SET FOR [['NHS2015_001', 'Land Area Coverage (Square Meters)']]")
        self.assertLogs(metadata_check.check_if_dollar_year_set(good_file))

    def test_check_if_gd_instead_guid(self):
        self.assertLogs(metadata_check.check_if_gd_instead_guid(bad_file),
                        "GD on line(s) [[78], [112]] present, please change it to GUID or open xml in metadata editor, "
                        "save it and close it.")
        self.assertLogs(metadata_check.check_if_gd_instead_guid(good_file))
