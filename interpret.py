import int_lib.arg_check
import int_lib.xml
import int_lib.interpreter

if (__name__ == "__main__"):
    source_text, input_text = int_lib.arg_check.arg_check()
    xml_code = int_lib.xml.load_xml_code(source_text)
    interpret = int_lib.interpreter.interpreter(xml_code, input_text)
    interpret.interpreting_init()
    exit(0)
