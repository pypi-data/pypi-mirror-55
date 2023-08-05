import os
import sys
import argparse
import json
import logging
import logging.config

from eacheck import validator

logger = logging.getLogger(__name__)

LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL', 'DEBUG')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,

    'formatters': {
        'console': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'datefmt': '%H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'level': LOGGING_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'console',
            'stream': sys.stdout
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': LOGGING_LEVEL,
            'propagate': False,
        },
        'converter': {
            'level': LOGGING_LEVEL,
            'propagate': True,
        }
    }
}

def str_out(xml_path, validation):
    status, errors = validation
    print(xml_path, status)
    for item in errors:
        print('\t', item.level, item.line, item.message)

def json_out(xml_path, validation):
    status, errors = validation

    output = {
        'xml': xml_path,
        'is_valid': status,
        'errors': [{'level':item.level, 'line':item.line, 'error':item.message} for item in errors]
    }

    print(json.dumps(output, indent=4))

def run(xml_paths, json):

    for xml_path in xml_paths:

        xmlvalidator = validator.XMLValidator()
        xml = open(xml_path)

        output = str_out
        if json is True:
            output = json_out

        output(xml_path, xmlvalidator.validate(xml))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source', nargs='*')

    parser.add_argument(
        '--json',
        '-j',
        help='JSON as output format',
        action='store_true'
    )

    parser.add_argument(
        '--log_level',
        '-l',
        help='Logging level',
        choices=['ERROR', 'WARNING', 'INFO', 'DEBUG'],
        default='INFO'
    )

    args = parser.parse_args()

    LOGGING['handlers']['console']['level'] = args.log_level
    for lg, content in LOGGING['loggers'].items():
        content['level'] = args.log_level

    logging.config.dictConfig(LOGGING)

    run(args.source, args.json)