<?php
/**
 * File contains main algorithm for generating XML,
 * created 11. 2. 2020
 *
 * @author Jiri Kristof, xkrist22
 * @version 2.1
 */

    // including files
    include "def_lib/constants.php";
    include "parse_lib/instr.php";

    // checking of arguments
    if (count($argv) != 1) {
        if (count($argv) == 2) {
            // check if user want to print help
            if (count($argv) == 2 && ($argv[1] == "--help" || $argv[1] == "-help")) {
                printf("Script parse.php load IPPcode20 file from STDIN, ");
                printf("check its lexical and syntactic correctness and ");
                printf("print XML representation of the code to the STDOUT\n");
                printf("Program made by Jiri Kristof, xkrist22, FIT VUT\n");
                return 0;
            }
        }
        exit(PARAMETER_ERROR);
    }

    // checking first line
    $line = fgets(STDIN);
    // skipping whitespace lines
    while (preg_match("/^\s*$/", $line) || preg_match("/^\s*#.*$/", $line)) {
        $line = fgets(STDIN);
    }
    $line = trim($line);


    // removing inline comment from line
    if (preg_match("/^[^#]+#.*/", $line)) {
        $line = strstr($line, '#', true);
        $line = trim($line);
    }


    // if first line is not .IPPcode20, return error about missing header
    if (strcmp(strtoupper($line), ".IPPCODE20")) {
        error_handler(MISSING_HEADER);
    }

    // create object of DOMDocument
    // generating <header> element
    $xml = new DOMDocument("1.0", "UTF-8");

    // generate <program> element
    $program_elem = $xml->createElement("program");
    $program_elem->setAttribute("language", "IPPcode20");

    $instr_counter = 1;
    while ($line = fgets(STDIN)) {
        // checking and skipping whitespace lines and lines containing only comment
        if (preg_match("/^\W*#.*$/", $line) || preg_match("/^\W+$/", $line)) {
            continue;
        }

        $instr = new instruction($line);

        // generating <instruction> element
        $instr_elem = $xml->createElement("instruction");
        $instr_elem->setAttribute("order", $instr_counter);
        $instr_elem->setAttribute("opcode", $instr->opcode());

        /*
         * NOTE: char "#" means, that the operand value is empty, but operand in not empty
         */

        // generating <arg1> element
        if ($instr->operand_1() != NULL && $instr->get_ope1_type() != NULL) {
            $value = $instr->operand_1();
            if (!strcmp($value, "#")) {
                $value = "";
            }
            $arg1_elem = $xml->createElement("arg1", $value);
            $arg1_elem->setAttribute("type", $instr->get_ope1_type());

            $instr_elem->appendChild($arg1_elem);
        }

        // generating <arg2> element
        if ($instr->operand_2() != NULL && $instr->get_ope2_type() != NULL) {
            $value = $instr->operand_2();
            if (!strcmp($value, "#")) {
                $value = "";
            }
            $arg2_elem = $xml->createElement("arg2", $value);
            $arg2_elem->setAttribute("type", $instr->get_ope2_type());

            $instr_elem->appendChild($arg2_elem);
        }

        // generating <arg3> element
        if ($instr->operand_1() != NULL && $instr->get_ope3_type() != NULL) {
            $value = $instr->operand_3();
            if (!strcmp($value, "#")) {
                $value = "";
            }
            $arg3_elem = $xml->createElement("arg3", $value);
            $arg3_elem->setAttribute("type", $instr->get_ope3_type());

            $instr_elem->appendChild($arg3_elem);
        }
        $program_elem->appendChild($instr_elem);
        $instr_counter++;
    }

    $xml->appendChild($program_elem);

    // print XML code
    $xml->formatOutput = true;
    $xml_code = $xml->saveXML();
    printf("%s", $xml_code);

    exit(RUN_OK);
?>
