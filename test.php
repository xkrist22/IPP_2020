<?php
/**
 * File contains parsing of arguments, loading files containing parser, interpret, jexamxml utility,
 * loading directory with tests and invocation right checking routine
 *
 * @author Jiri Kristof, xkrist22
 */

    // including files
    include "def_lib/constants.php";
    include "test_lib/html_gen.php";
    include "test_lib/parse_check.php";
    include "test_lib/int_check.php";
    include "test_lib/parse_int_check.php";

    // default settings
    $recursive = false;
    $directory = "";
    $parse_script = "parse.php";
    $int_script = "interpret.py";
    $parse_only = false;
    $int_only = false;
    $jexamxml = "/pub/courses/ipp/jexamxml/jexamxml.jar";

    /*
     * Arguments checking
     */
    if (count($argv) >= 2) {
        if (count($argv) > 7) {
            error_handler(PARAMETER_ERROR);
        }

        $directory_loaded = false;
        $recursive_loaded = false;
        $parse_script_loaded = false;
        $int_script_loaded = false;
        $parse_only_loaded = false;
        $int_only_loaded = false;
        $jexamxml_loaded = false;
        $help_loaded = false;

	$skip_name = true;
        foreach ($argv as $arg) {
            if ($skip_name) {
		$skip_name = false;
                continue;
            }
            if (preg_match("/^--directory=(\/[^\\\?*:;{}\/]+)*[^\\\?*:;{}\/]+$/", $arg)) {
                // check --directory=path
                if ($directory_loaded || $help_loaded) {
                    error_handler(PARAMETER_ERROR);
                }
                $directory = strstr($arg, '=');
            	$directory = substr($directory, 1);
            	if (!file_exists(getcwd() . DIRECTORY_SEPARATOR . $directory)) {
                    error_handler(INPUT_FILE_ERROR);
                }
                $directory_loaded = true;
            } elseif (preg_match("/--recursive/", $arg)) {
                // check --recursive
                if ($recursive_loaded || $help_loaded) {
                    error_handler(PARAMETER_ERROR);
                }
                $recursive = true;
                $recursive_loaded = true;
            } elseif (preg_match("/^--parse-script=(\/[^\\\?*:;{}\/]+)*[^\\\?*:;{}\/]+$/", $arg)) {
                // check --parse-script=file
                if ($parse_script_loaded || $help_loaded) {
                    error_handler(PARAMETER_ERROR);
                }
                $parse_script = strstr($arg, "=");
		        $parse_script = substr($parse_script, 1);
                if (!file_exists(getcwd() . DIRECTORY_SEPARATOR . $parse_script)) {
                    error_handler(INPUT_FILE_ERROR);
                }

                $parse_script_loaded = true;
            } elseif (preg_match("/^--int-script=(\/[^\\\?*:;{}\/]+)*[^\\\?*:;{}\/]+$/", $arg)) {
                // check --int-script=file
                if ($int_script_loaded || $help_loaded) {
                    error_handler(PARAMETER_ERROR);
                }
                $int_script = strstr($arg, "=");
                $int_script = substr($int_script, 1);
                if (!file_exists(getcwd() . DIRECTORY_SEPARATOR . $int_script)) {
                    error_handler(INPUT_FILE_ERROR);
                }
                $int_script_loaded = true;
            } elseif (preg_match("/--parse-only/", $arg) && !$int_only && !$int_script_loaded) {
                // check --parse-only
                if ($parse_only_loaded || $help_loaded) {
                    error_handler(PARAMETER_ERROR);
                }
                $parse_only = true;
                $parse_only_loaded = true;
            } elseif (preg_match("/--int-only/", $arg) && !$parse_only && !$parse_script_loaded) {
                // check --int-only
                if ($int_only_loaded || $help_loaded) {
                    error_handler(PARAMETER_ERROR);
                }
                $int_only = true;
                $int_only_loaded = true;
            } elseif (preg_match("/^--jexamxml=(\/[^\\\?*:;{}\/]+)*[^\\\?*:;{}\/]+.jar$/", $arg)) {
                // check --jexamxml
                if ($jexamxml_loaded || $help_loaded) {
                    error_handler(PARAMETER_ERROR);
                }
                $jexamxml = strstr($arg, "=", true);
                $jexamxml = substr($jexamxml, 1);
                if (!file_exists($jexamxml)) {
                    error_handler(INPUT_FILE_ERROR);
                }

                $jexamxml_loaded = true;
            } elseif (preg_match("/^--help$/", $arg)
                        && !$directory_loaded && !$recursive_loaded && !$parse_script_loaded
                        && !$int_script_loaded && !$parse_only_loaded && !$int_only_loaded
                        && !$jexamxml_loaded && !$help_loaded
            ) {
                $help_loaded = true;
            } else {
                error_handler(PARAMETER_ERROR);
            }
        }
    }

    if ($help_loaded) {
        // if parametr --help was loaded, help is printed
        test_help();
    }

    // run correct testing module
    if ($parse_only) {
	if ($directory) {
            // test in given dir
            check_parser(getcwd() . DIRECTORY_SEPARATOR . $directory, $parse_script, $jexamxml, $recursive, $directory . DIRECTORY_SEPARATOR);
        } else {
            // test in actual dir
            check_parser(getcwd(), $parse_script, $jexamxml, $recursive, DIRECTORY_SEPARATOR);
        }
    } elseif ($int_only) {
       if ($directory) {
            // test in given dir
            check_interpreter(getcwd() . DIRECTORY_SEPARATOR . $directory, $int_script, $recursive, $directory . DIRECTORY_SEPARATOR);
        } else {
            // test in actual dir
            check_interpreter(getcwd(), $int_script, $recursive, DIRECTORY_SEPARATOR);
        }
    } else {
       if ($directory) {
            // test in given dir
            check_app(getcwd() . DIRECTORY_SEPARATOR . $directory, $parse_script, $int_script, $recursive, $directory . DIRECTORY_SEPARATOR);
        } else {
            // test in actual dir
            check_app(getcwd(), $parse_script, $int_script, $recursive, DIRECTORY_SEPARATOR);
        }
    }
    exit(RUN_OK);

