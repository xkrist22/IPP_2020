import sys

MISSING_PARAMETERS = 10
INPUT_FILE_ERROR = 11
OUTPUT_FILE_ERROR = 12
NOT_WELL_FORMED_XML = 31
BAD_XML_STRUCTURE = 32
SEMANTICS_ERROR = 52
BAD_OPERAND_TYPES = 53
NOT_EXISTING_VARIABLE = 54
NOT_EXISTING_FRAME = 55
MISSING_VALUE = 56
BAD_VALUE = 57
STRING_ERROR = 58
INTERNAL_ERROR = 99


def error_handler(error_code):
    if (error_code == MISSING_PARAMETERS):
        sys.stderr.write("Missing parameter or invalid combination of parameters!\n")
        exit(MISSING_PARAMETERS)

    elif (error_code == INPUT_FILE_ERROR):
        sys.stderr.write("Problems with opening input file!\n")
        exit(INPUT_FILE_ERROR)

    elif (error_code == OUTPUT_FILE_ERROR):
        sys.stderr.write("Problems with opening output file!\n")
        exit(OUTPUT_FILE_ERROR)

    elif (error_code == NOT_WELL_FORMED_XML):
        sys.stderr.write("XML code is not well-formed!\n")
        exit(NOT_WELL_FORMED_XML)

    elif (error_code == BAD_XML_STRUCTURE):
        sys.stderr.write("XML code has bad structure!\n")
        exit(BAD_XML_STRUCTURE)

    elif (error_code == SEMANTICS_ERROR):
        sys.stderr.write("Semantic error found!\n")
        exit(SEMANTICS_ERROR)

    elif (error_code == BAD_OPERAND_TYPES):
        sys.stderr.write("Operand type is not compatible for operation!\n")
        exit(BAD_OPERAND_TYPES)

    elif (error_code == NOT_EXISTING_VARIABLE):
        sys.stderr.write("Not existing variable loaded!\n")
        exit(NOT_EXISTING_VARIABLE)

    elif (error_code == NOT_EXISTING_FRAME):
        sys.stderr.write("Not existing frame loaded!\n")
        exit(NOT_EXISTING_FRAME)

    elif (error_code == MISSING_VALUE):
        sys.stderr.write("Missing value in variable, data stack or call stack!\n")
        exit(MISSING_VALUE)

    elif (error_code == BAD_VALUE):
        sys.stderr.write("Bad operand value (dividing by zero, ...)!\n")
        exit(BAD_VALUE)

    elif (error_code == STRING_ERROR):
        sys.stderr.write("String operations is not used correctly!\n")
        exit(STRING_ERROR)

    elif (error_code == INTERNAL_ERROR):
        sys.stderr.write("Internal error!\n")
        exit(INTERNAL_ERROR)

    else:
        sys.stderr.write("Unknown error!\n")
        exit(INTERNAL_ERROR)
