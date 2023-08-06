#!python
import unicodedata
import re
# Function to remove special characters and convert
# them in lower case from typical french names


def strip_accents(text):
    """
    Strip accents from input String.
    :param text: The input string.
    :type text: String.
    :returns: The processed String.
    :rtype: String.
    """
    try:
        text = unicode(text, 'utf-8')
    except (TypeError, NameError):  # unicode is a default on python 3
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)


def text_to_id(text):
    """
    Convert input text to id.
    :param text: The input string.
    :type text: String.
    :returns: The processed String.
    :rtype: String.
    """

    text = strip_accents(text)
    text = re.sub('[ ]+', '_', text)
    text = re.sub('[^0-9a-zA-Z_-]', '', text)
    text = re.sub('-', '', text)
    text = re.sub('_', '', text)
    text = text.replace(r'\/', '')
    text = text.replace(r'\\', ' ')
    return text.upper()
