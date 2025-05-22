import xml.etree.ElementTree as ET
from line_analysis import get_default_line_wavelengths

import xml.etree.ElementTree as ET

def read_xml(file_path):
    """
    Reads an XML file and returns a dictionary containing the text content of each element.

    Args:
        file_path (str): The path to the XML file.

    Returns:
        dict: A dictionary where the keys are the element tags and the values are the text content of each element.
    """
    tree = ET.parse(file_path)
    root = tree.getroot()

    element_texts = {}

    for element in root.iter():
        if element != root:
            element_texts[element.tag] = element.text

    return element_texts

