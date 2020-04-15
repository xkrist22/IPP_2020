<?php
/**
 * File contains error codes and function which is able to exit program if there is error,
 * created 11. 2. 2020
 *
 * @author Jiri Kristof, xkrist22
 * @version 2.1
 */

    // global constants
    const RUN_OK = 0;
    const PARAMETER_ERROR = 10;
    const INPUT_FILE_ERROR = 11;
    const OUTPUT_FILE_ERROR = 12;
    const MISSING_HEADER = 21;
    const UNKNOWN_OPCODE = 22;
    const LEX_SYN_ERROR = 23;
    const XML_FORMAT_ERROR = 31;
    const XML_STRUCT_ERROR = 32;
    const INTERNAL_ERROR = 99;

    // CSS code for test.php output
    const CSS = "<style>body {margin:0; color:#2A2C2B ;background-color:#e9eef0 ;font-family:Verdana,Geneva,sans-serif; font-size:14px; } h1 {margin:0; padding:10px; display:flex; flex-direction:row; flex-wrap: wrap; justify-content:space-around; align-items:center; background-color:#2A2C2B; color:white; font-size:30px; font-weight:500;} #statistics{height:70px; background-color:white; display:flex; flex-direction:column; justify-content:center; padding:20px; font-size:15px; color:#536c78;} #statistics div{padding:5px;}#statistics div b{font-weight:500;} .line div{width:25%; display:flex; align-items:center; justify-content:center;} .line{display:flex; flex-direction:row; flex-wrap:nowrap; justify-content:space-around; width:90vw; height:40px; margin: 15px auto; padding:5px; background-color:white; box-shadow:0 0 7px 0 #7d98a5;} .head{background-color:#e9eef0; box-shadow:none;} .passed{color:#43A047; font-weight:600;} .failed{color:#D40D12; font-weight:600;}</style>\n";

    /**
     * Function for writing error report to STDERR and returning right return value
     * @param int $error_code holds the error value, which will program return
     */
    function error_handler($error_code) {
        switch ($error_code) {
            case PARAMETER_ERROR:
                fwrite(STDERR, "Missing parameter or invalid combination of parameters!" . PHP_EOL);
                fwrite(STDERR, "For help run the script with parameter --help" . PHP_EOL);
                exit(PARAMETER_ERROR);

            case INPUT_FILE_ERROR:
                fwrite(STDERR, "Problems with opening input file!" . PHP_EOL);
                fwrite(STDERR, "For help run the script with parameter --help" . PHP_EOL);
                exit(INPUT_FILE_ERROR);

            case OUTPUT_FILE_ERROR:
                fwrite(STDERR, "Problems with opening output file!" . PHP_EOL);
                fwrite(STDERR, "For help run the script with parameter --help" . PHP_EOL);
                exit(OUTPUT_FILE_ERROR);

            case MISSING_HEADER:
                fwrite(STDERR, "Missing header!" . PHP_EOL);
                fwrite(STDERR, "For help run the script with parameter --help" . PHP_EOL);
                exit(MISSING_HEADER);

            case UNKNOWN_OPCODE:
                fwrite(STDERR, "Unknown opcode!" . PHP_EOL);
                fwrite(STDERR, "For help run the script with parameter --help" . PHP_EOL);
                exit(UNKNOWN_OPCODE);

            case LEX_SYN_ERROR:
                fwrite(STDERR, "Lexical or syntactic error!" . PHP_EOL);
                fwrite(STDERR, "For help run the script with parameter --help" . PHP_EOL);
                exit(LEX_SYN_ERROR);

            case XML_FORMAT_ERROR:
                fwrite(STDERR, "XML file is not well-formed" . PHP_EOL);
                fwrite(STDERR, "For help run the script with parameter --help" . PHP_EOL);
                exit(XML_FORMAT_ERROR);

            case XML_STRUCT_ERROR:
                fwrite(STDERR, "Problems with XML structure" . PHP_EOL);
                fwrite(STDERR, "For help run the script with parameter --help" . PHP_EOL);
                exit(XML_STRUCT_ERROR);

            case INTERNAL_ERROR:
                fwrite(STDERR, "Internal error!" . PHP_EOL);
                fwrite(STDERR, "For help run the script with parameter --help" . PHP_EOL);
                exit(INTERNAL_ERROR);

            default:
                fwrite(STDERR, "Unknown error!" . PHP_EOL);
                fwrite(STDERR, "For help run the script with parameter --help" . PHP_EOL);
                exit(INTERNAL_ERROR);
        }
    }

    function test_help() {
        printf("Script test.php automatically tests parse.php and interpret.py. ");
        printf("You can use these parameters:\n");
        printf("\t--help\tprint help\n");
        printf("\t--directory=path\tscript will search tests in directory defined in path\n");
        printf("\t--recursive\tscript will search tests in subdirectories \n");
        printf("\t--parse-script=file\tYou can choose file with script for parsing IPPcode20. Defaultly is set to parse.php\n");
        printf("\t--int-script=file\tYou can choose file with script for interpreting XML representaqtion of program. Defaultly is set to interpret.py\n");
        printf("\t--parse-only\ttesting only script for parsing IPPcode20 to XML (parse.php defaultly)\n");
        printf("\t--int-only\ttesting only script for interpreting XML (interpret.py defaultly)\n");
        printf("\t--jexamxml=file\tset path to the A7Soft JExamXML utility (defaultly /pub/courses/ipp/jexamxml/jexamxml.jar)\n");
        printf("Program made by Jiri Kristof, xkrist22, FIT VUT\n");
        exit(RUN_OK);
    }

?>
