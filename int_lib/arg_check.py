import int_lib.err
import sys
import re


def arg_check():
    help_loaded = False
    source_loaded = False
    input_loaded = False
    source_file = None
    input_file = None
    skip_name_of_file = True
    for arg in sys.argv:
        if (skip_name_of_file):
            skip_name_of_file = False
            continue

        if (re.match(r'--help', arg) and not source_loaded and not input_loaded and not help_loaded):
            help_loaded = True

        elif (re.match(r'--source=.*', arg) and not source_file):
            source_file = arg[9:]
            source_loaded = True

        elif (re.match(r'--input=.*', arg)):
            input_file = arg[8:]
            input_loaded = True

        else:
            int_lib.err.error_handler(int_lib.err.MISSING_PARAMETERS)

    if (help_loaded):
        print_help()

    if (not source_file and not input_file):
        int_lib.err.error_handler(int_lib.err.MISSING_PARAMETERS)

    # loading source file from stdin
    # loading input file from file
    elif (not source_file and input_file):
        source_text = sys.stdin.readlines()
        temp_file = open(input_file)
        if (not temp_file):
            int_lib.err.error_handler(int_lib.err.INPUT_FILE_ERROR)
        input_text = temp_file.read().splitlines()
        temp_file.close()
        return source_text, input_text

    elif (source_file and not input_file):
        input_text = None
        temp_file = open(source_file)
        if (not temp_file):
            int_lib.err.error_handler(int_lib.err.INPUT_FILE_ERROR)

        source_text = temp_file.readlines()
        temp_file.close()
        return source_text, input_text

    elif (source_file and input_file):
        temp_file = open(input_file)
        if (not temp_file):
            int_lib.err.error_handler(int_lib.err.INPUT_FILE_ERROR)
        input_text = temp_file.read().splitlines()
        temp_file.close()

        temp_file = open(source_file)
        if (not temp_file):
            int_lib.err.error_handler(int_lib.err.INPUT_FILE_ERROR)
        source_text = temp_file.readlines()
        temp_file.close()

        return source_text, input_text


def print_help():
    print("""Program loads XML representation of the program written in language IPPcode20 and interprets it
You can use these parameters:
    --help          print help
    --source=path   set path to source file (file with XML)
    --input=path    set path to input file (file with inputs)
    One of parameters for setting input or source must be set
Program made by Jiri Kristof, xkrist22, FIT VUT""")
    exit(0)
