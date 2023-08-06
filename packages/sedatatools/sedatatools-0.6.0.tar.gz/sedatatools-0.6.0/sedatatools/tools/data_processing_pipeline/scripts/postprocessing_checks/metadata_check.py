"""
Postprocessing metadata check v0.01
For the doc part, please read it in C:\Projects\DataTeam\sedatatools\sedatatools\tools\data_processing_pipeline
\docs\Documentation_metadata_check_script.docx
"""
from lxml.etree import parse, XMLSchema, XMLSyntaxError
import lxml.etree as et
from loguru import logger
import os
import collections

from scripts.helpers.metadata_check_helpers import get_input_data


def xml_to_xsd_validation(file_xml, file_xsd):
    """
    Verify that the XML compliance with XSD
    :param file_xml: Input xml file
    :param file_xsd: xsd file which needs to be validated against xml
    :return: no return value, returning log if not ok
    """

    logger.info("Validating xml file: {0}".format(file_xml.split('/')[-1]))
    logger.info("xsd_file: {0}".format(file_xsd.split('/')[-1]))

    try:
        xml_doc = parse(file_xml)
        xsd_doc = parse(file_xsd)
        xmlschema = XMLSchema(xsd_doc)
        xmlschema.assert_(xml_doc)
        logger.info("YEAH! my xml file has validated")
        return True

    except XMLSyntaxError as err:
        logger.error("PARSING ERROR:{0}".format(err))
        return False

    except AssertionError as err:
        logger.error("Incorrect XML schema: {0}".format(err))
        return False

    except et.XMLSchemaParseError as err:
        logger.error(err)
        return False


def guid_systems_xml(all_systems_xml):
    """
    Getting all the guids from the systems metadata files
    :param all_systems_xml: all xmls from the metadata folder
    :return: dict_guid_all_xml with all the guids in the system.
    It will return element tag, element path and name of survey
    """

    guid_all_xml = {}

    for each_system_xml in all_systems_xml:
        tree_systems_xml = et.parse(each_system_xml)
        root_systems_xml = tree_systems_xml.getroot()

        for child in root_systems_xml.iter():
            if 'GUID' in child.attrib:
                guid_all_xml[child.attrib['GUID']] = child.tag, tree_systems_xml.getpath(child),\
                                                     child.base.split("/")[-1]

    return guid_all_xml


def guid_my_xml(file_xml):
    """
    Getting all the guids from the xml metadata file you're working on
    :param file_xml: the file you're working on
    :return: dict_guid_my_xml: dictionary with all the guids from that xml file.
    It will return element tag, element path
    """

    tree_my_xml = et.parse(file_xml)
    root_my_xml = tree_my_xml.getroot()

    guid_my_new_xml = {}

    for child in root_my_xml.iter():
        if 'GUID' in child.attrib:
            guid_my_new_xml[child.attrib['GUID']] = child.tag, tree_my_xml.getpath(child)

    return guid_my_new_xml


def check_uniqueness_guid_my_xml(file_xml):
    """
    Getting all the guids from the xml metadata file you're working on in a list
    :param file_xml: the file you're working on
    :return: list_guid_my_xml: list with all the guids from that xml file.
    """

    tree_my_xml = et.parse(file_xml)
    root_my_xml = tree_my_xml.getroot()

    only_guid_my_new_xml = []

    for child in root_my_xml.iter():
        if 'GUID' in child.attrib:
            only_guid_my_new_xml.append(child.attrib['GUID'])

    counter = 0
    for item, count in collections.Counter(only_guid_my_new_xml).items():
        if count > 1:
            counter += 1
            logger.error('The following GUIDs are duplicates in your xml: ' +
                         str(item) + '. Make sure to redistribute GUIDs and make it unique.')

    if counter > 0:
        return False
    else:
        return True


def guid_uniqueness(dict_all_guid, dict_my_xml):
    """
    Checking GUID uniqueness between systems xml and the xml you are working on
    :param dict_all_guid: all guid from the system
    :param dict_my_xml: guid from your xml
    :return: True or False, depending if there is double guid or not
    """

    counter = 0
    for old_key, old_value in dict_all_guid.items():
        for new_key, new_value in dict_my_xml.items():
            if new_key in old_key:
                counter += 1
                logger.error('GUID duplicates between\n systems xml: {0}, '
                             'on element: "{1}", with path: "{2}" \n and you new xml, '
                             'on element: "{3}", with path to it: "{4}"'.format
                             (str(old_value[2]), str(old_value[0]), str(old_value[1]), str(new_value[0]),
                              str(new_value[1])))

    if counter > 0:
        return False
    else:
        return True


def geo_plural_name_singular(xml_doc):
    """
    Checking if geo types plural names are singular
    :param xml_doc: current xml
    :return: log
    """

    tree_my_xml = et.parse(xml_doc)

    standard_us_plurals = ['States', 'Counties', 'Tracts', 'Places', 'Subdivisions', 'Regions', 'Divisions', 'Areas',
                           'Districts', 'Corporations', 'Lands', 'Cities']
    geo_labels_list = tree_my_xml.xpath('//geoType')
    plurals = [geo_plural_label.attrib['PluralName']
               for geo_plural_label in geo_labels_list
               for ele in standard_us_plurals if ele in geo_plural_label.attrib['PluralName']]

    not_plurals = [geo_plural_label.attrib['PluralName'] for geo_plural_label in geo_labels_list
                   if geo_plural_label.attrib['PluralName'] not in plurals]

    if len(not_plurals) > 0 and str(not_plurals) == 'Nation':
        logger.error('GEO TYPES PluralName SET AS SINGULAR: ' + str(not_plurals))


def geo_labels_plural(xml_doc):
    """
    Checking if geo types labels are written as plural instead of singular
    :param xml_doc: current xml
    :return: log
    """

    tree_my_xml = et.parse(xml_doc)

    standard_us_plurals = ['States', 'Counties', 'Tracts', 'Places', 'Subdivisions', 'Regions', 'Divisions', 'Areas',
                           'Districts', 'Corporations', 'Lands', 'Cities']
    geo_labels_list = tree_my_xml.xpath('//geoType')
    plurals = [geo_plural_label.attrib['Label']
               for geo_plural_label in geo_labels_list
               for ele in standard_us_plurals if ele in geo_plural_label.attrib['Label']]

    if len(plurals) > 0:
        logger.error('GEO TYPES Label SET AS PLURAL:' + str(plurals))


def geo_types_qlabel_indent(xml_doc):
    """
    Checking if geo types qlabels are not set properly: e.g. State-County is ok, Nation-State-County is not ok
    :param xml_doc: current xml
    :return: log
    """

    tree_my_xml = et.parse(xml_doc)

    geo_labels_list = tree_my_xml.xpath('//geoType')
    errors = []
    for gl in geo_labels_list:
        number_of_dashes = len([d for d in gl.attrib['QLabel'] if d == '-'])
        if number_of_dashes != int(gl.attrib['Indent']) - 1 and int(gl.attrib['Indent']) > 1:
            errors.append(gl.attrib['Label'])
    if len(errors) > 0:
        logger.error('GEO TYPES QLABEL NOT INDENTED PROPERLY: ' + str(errors))


def table_suffix_geo_summary(xml_doc):
    """
    Checking if DbTableSuffix is wrongly set
    :param xml_doc: current xml
    :return: log
    """

    tree_my_xml = et.parse(xml_doc)

    allowed_suffixes = ['Geo', '001']
    if tree_my_xml.xpath('/survey/GeoSurveyDataset/tables/table/@DbTableSuffix')[0] not in allowed_suffixes:
        logger.error('TABLE SUFFIX IN GEOGRAPHY SUMMARY FILE TABLES IS NOT SET IN SOME OF THESE SUFFIXES: ' +
                     str(allowed_suffixes))


def table_var_case(xml_doc):
    """
    Checking if table or variable labels are not set to title case
    :param xml_doc: current xml
    :return: log
    """

    tree_my_xml = et.parse(xml_doc)

    variables = tree_my_xml.xpath('//variable')
    untitlecased_words = ['to', 'a', 'an', 'the', 'by', 'for', 'in', 'of', 'on', 'and', 'as', 'but', 'or',
                          'than', 'with', '(m2)', '%']
    exceptions = ['FIPS', 'GED', 'PhD', 'BA', 'MA', 'HH', 'S/R', 'GQ', 'HU', 'HS', 'LF', 'P/T/M', 'Haw/PI', 'US',
                  'N/H', 'DollarYear']
    errors = []
    for var in variables:
        label = var.attrib['label']
        for el in untitlecased_words:
            label = label.replace(el, '')
        if not label.istitle() and label not in exceptions:
            errors.append([var.attrib['name'], var.attrib['label']])

    tables = tree_my_xml.xpath('//tables/table')
    for tab in tables:
        label = tab.attrib['title']
        for el in untitlecased_words:
            label = label.replace(el, '')
        if not label.istitle() and label not in exceptions:
            errors.append([tab.attrib['displayName'], tab.attrib['title']])

    if len(errors) > 0:
        logger.error('TABLE AND VARIABLE LABELS NOT IN TITLE CASE: ' + str(errors))


def source_publisher_exist(xml_doc):
    """
    Checking if source or publisher is set.
    :param xml_doc: current xml
    :return: log
    """

    tree_my_xml = et.parse(xml_doc)

    datasets = tree_my_xml.xpath('//SurveyDatasets/SurveyDataset')
    errors = []

    for ds in datasets:
        err = []
        if ds.attrib['source'] == '':
            err.append('source')
        if ds.attrib['publisher'] == '':
            err.append('publisher')
        if len(err) > 0:
            errors.append([ds.attrib['name'], *err])
    if len(errors) > 0:
        logger.error('SOURCE AND PUBLISHER ARE NOT SET PROPERLY.')


def survey_name(xml_doc):
    """
    Checking if survey name is short.
    :param xml_doc: current xml
    :return: log
    """
    tree_my_xml = et.parse(xml_doc)

    survey_name_attrib = tree_my_xml.xpath('/survey/@name')[0]
    if len(survey_name_attrib) > 10:
        logger.warning('SURVEY NAME NOT REALLY SHORT. MAKE IT SHORTER.')


def check_if_dollar_year_set(xml_doc):
    """
    Checking if Dollar Year is set.
    :param xml_doc: current xml
    :return: log
    """
    tree_my_xml = et.parse(xml_doc)

    errors = []
    tables_list = tree_my_xml.xpath("//table")

    for tab in tables_list:
        list_to_fix = tab.xpath(".//variable[contains(@label,'DollarYear')]")
        if len(list_to_fix) > 0:
            if tab.attrib['DollarYear'] == '0':
                errors.append([tab.attrib['displayName'], tab.attrib['title']])
    if len(errors) > 0:
        logger.error('DOLLAR YEAR NOT SET FOR ' + str(errors))


def check_if_gd_instead_guid(xml_doc):
    """
    Checking if there is GD instead of GUID.
    :param xml_doc: current xml
    :return: log
    """

    tree_my_xml = et.parse(xml_doc)
    root_my_xml = tree_my_xml.getroot()

    errors = []

    for child in root_my_xml.iter():
        if 'GD' in child.attrib:
            errors.append([child.sourceline])

    if len(errors) > 0:
        logger.error('GD on line(s) ' + str(errors) + ' present, '
                                                      'please change it to GUID or open xml in metadata editor, '
                                                      'save it and close it.')


def main(all_systems_xml, my_xml, xsd_schema):

    all_xml = []

    for file in os.listdir(all_systems_xml):
        if file.endswith(".xml"):
            all_xml.append(os.path.join(all_systems_xml, file))

    xml_to_xsd_validation(my_xml, xsd_schema)
    dict_guid_all_xml = guid_systems_xml(all_xml)
    dict_guid_my_xml = guid_my_xml(my_xml)
    check_uniqueness_guid_my_xml(my_xml)
    guid_uniqueness(dict_guid_all_xml, dict_guid_my_xml)
    geo_plural_name_singular(my_xml)
    geo_types_qlabel_indent(my_xml)
    geo_labels_plural(my_xml)
    table_suffix_geo_summary(my_xml)
    table_var_case(my_xml)
    source_publisher_exist(my_xml)
    survey_name(my_xml)
    check_if_dollar_year_set(my_xml)
    check_if_gd_instead_guid(my_xml)


if __name__ == "__main__":

    # xml_path = '../tests/res/xml_to_be_checked/correct_metadata.xml'

    # all_xml_path = '../tests/res/systems_xml_files'

    all_xml_path, xml_path, xsd_path = get_input_data()
    main(all_xml_path, xml_path, xsd_path)
