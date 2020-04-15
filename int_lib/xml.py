import int_lib.err
import re
import xml.etree.cElementTree as ET

def load_xml_code(source_text_arr):
    xml_root = None
    source_text = ''.join(source_text_arr)
    source_text = replace_escape(source_text)
    try:
        xml_root = ET.fromstring(source_text)
    except ET.ParseError:
        int_lib.err.error_handler(int_lib.err.NOT_WELL_FORMED_XML)

    """
    sorting XML file
    NOTE: interpret.py typically get XML representation from parse.php, which generated sorted XML.
    For this reason is used bubble sort
    """
    for i in range(len(xml_root)):
        try:
            if int(xml_root[i].attrib['order']) <= 0:
                int_lib.err.error_handler(int_lib.err.NOT_WELL_FORMED_XML)
              
            for j in range(0, len(xml_root) - i - 1):
                if (int(xml_root[j].attrib['order']) > int(xml_root[j + 1].attrib['order'])):
                    temp = xml_root[j]
                    xml_root[j] = xml_root[j + 1]
                    xml_root[j + 1] = temp
        except KeyError:
            int_lib.err.error_handler(int_lib.err.BAD_XML_STRUCTURE)

    return xml_root


def replace_escape(source_text):
    ret_str = ""
    to_skip = 0
    for i in range(len(source_text)):
        if (to_skip != 0):
            to_skip = to_skip - 1
            continue

        if (source_text[i] == "\\" and re.match(r'[0-9]', source_text[i + 1]) and re.match(r'[0-9]', source_text[i + 2]) and re.match(r'[0-9]', source_text[i + 3])):
            ret_str = ret_str + chr(int(source_text[i + 1] + source_text[i + 2] + source_text[i + 3]))
            to_skip = 3
        else:
            ret_str = ret_str + source_text[i]
    return ret_str
