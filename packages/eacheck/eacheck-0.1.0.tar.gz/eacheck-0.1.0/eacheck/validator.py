import os
import logging

from lxml import etree

from eacheck import style_errors

PATH = os.path.dirname(os.path.realpath(__file__))

logger = logging.getLogger(__name__)


class SchemaError(Exception):
    pass


class EASchema():

    SCHEMA_VERSION = '3.0.0'

    def __init__(self, version=None):
        self.version = version or self.SCHEMA_VERSION
        self.schema = self._parse_schema()

    def _parse_schema(self):
        schema_path = '%s/schema/article/%s/eruditarticle.xsd' % (PATH, self.version)
        
        try:
            schema_str = open(schema_path)
        except FileNotFoundError:
            msg = 'Schema version (%s) not supported', self.version
            logger.exception(msg)
            raise SchemaError(msg)

        parsed_schema = etree.parse(schema_str)


        return etree.XMLSchema(parsed_schema)


class XMLValidator():

    XMLNS = '{http://www.erudit.org/xsd/article}'

    def __init__(self, schema_version=None, label=''):
        self.schema = EASchema(version=schema_version).schema
        self.label = label

    def _parse_xml(self, xmlfile):

        xml = etree.parse(xmlfile)

        return xml

    def is_validate(self, xmlfile):
        
        xml = self._parse_xml(xmlfile)

        validation = self.schema.validate(xml)

        return validation

    def validate(self, xmlfile):
        """
        Validate xmlfile against the given DTD.
        Returns a tuple comprising the validation status and the errors list.
        """
        xml = self._parse_xml(xmlfile)

        result = self.schema.validate(xml)
        errors = [style_errors.SchemaStyleError(err, label=self.label, namespace=self.XMLNS)
                  for err in self.schema.error_log]

        return result, errors

