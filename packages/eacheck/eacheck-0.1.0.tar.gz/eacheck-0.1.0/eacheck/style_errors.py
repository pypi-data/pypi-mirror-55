"""
Adapters for XML errors.

An adapter is an object that provides domain-specific apis for another object,
called adaptee.
"""
import re
import logging


LOGGER = logging.getLogger(__name__)


EXPOSE_ELEMENTNAME_PATTERN = re.compile(r"(?<=Element )'.*?'")


def search_element_name(message):
    """Try to locate in `message` the element name pointed as error.

    :param message: is a lxml error log message.
    """
    match = EXPOSE_ELEMENTNAME_PATTERN.search(message)
    if match is None:
        LOGGER.info('cannot find the element name in message')
        LOGGER.debug('failed regexp was %s on message "%s"', 
                EXPOSE_ELEMENTNAME_PATTERN.pattern, message)
        raise ValueError('cannot find the element name in message')

    else:
        element_name = match.group(0).strip("'")
        LOGGER.info('found element name "%s" in message', element_name)

        return element_name


def search_element(doc, xpath, line=None):
    """Try to locate in `doc` the element expressed as `xpath`.
    """
    for elem in doc.xpath(xpath):
        if line is None:
            return elem

        elif elem.sourceline == line:
            return elem

        else:
            continue

    # raise ValueError if the element could not be located.
    LOGGER.info('could not find element "%s"', xpath)
    raise ValueError('could not find element "%s"' % xpath)


#--------------------------------
# adapters for XML style errors
#--------------------------------
class StyleErrorBase(object):
    """Acts like an interface for EruditArticle style errors.

    A basic implementation of `get_apparent_element` is provided.
    """
    line = message = level = None
    label = u''

    def get_apparent_element(self, doc):
        """The apparent element presenting the error at doc.

        This base implementation tries to discover the element name by
        searching the string pattern `Element 'element name'` on message.
        """
        return NotImplemented


class SchemaStyleError(StyleErrorBase):
    """ DTD errors.
    """
    level = u'DTD Error'

    def __init__(self, err_object, label=u'', namespace=None):
        self._err = err_object
        self.message = self._err.message if namespace is None else self._err.message.replace(namespace, '')
        self.line = self._err.line
        self.label = label

    def get_apparent_element(self, doc):
        for elem in doc.iter():
            if elem.sourceline == self.line:
                return elem

        LOGGER.info("cannot find element at the line %s", self.line)
        raise ValueError("cannot find element at the line %s" % self.line)
