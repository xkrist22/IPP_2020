<?php

function check_parser($dir_with_tests, $parse_script, $jexamxml, $recursive, $work_dir, $is_recursive_call = false) {
    $html = html_gen::get_instance("parse.php");
    $extracted_test_files = scandir($dir_with_tests);

    foreach ($extracted_test_files as $test_file) {
        if ($test_file == "." || $test_file == "..") {
            continue;
        }

        if (is_dir( $work_dir . $test_file) && $recursive) {
            check_parser($dir_with_tests . DIRECTORY_SEPARATOR . $test_file, $parse_script, $jexamxml, $recursive, $work_dir . $test_file . DIRECTORY_SEPARATOR, true);
        } else {
            $test_file_info = pathinfo($dir_with_tests . DIRECTORY_SEPARATOR . $test_file);
            if ($test_file_info['extension'] != "src") {
                continue;
            }

            // get data from .out file
            if (file_exists($dir_with_tests . DIRECTORY_SEPARATOR . $test_file_info['filename'] . ".out")) {
                $declared_output_file = $dir_with_tests . DIRECTORY_SEPARATOR . $test_file_info['filename'] . ".out";
                $remove_file = false;
            } else {
                $declared_output_file = $dir_with_tests . DIRECTORY_SEPARATOR . $test_file_info['filename'] . ".out";
                $temp_file_holder = fopen($dir_with_tests . DIRECTORY_SEPARATOR . $test_file_info['filename'] . ".out", "w+");
                $remove_file = true;
            }

            // get data from .rc file
            $declared_return_code = 0;

            if (file_exists($dir_with_tests . DIRECTORY_SEPARATOR . $test_file_info['filename'] . ".rc")) {
                $declared_return_code = file_get_contents($dir_with_tests . DIRECTORY_SEPARATOR . $test_file_info['filename'] . ".rc", true);
            }

            exec("php7.4 " . $parse_script . " <" . $dir_with_tests . DIRECTORY_SEPARATOR . $test_file, $generated_output, $generated_return_code);
       
            $temp_xml_file = tempnam($dir_with_tests, "temp");
            $temp_xml_file_handler = fopen($temp_xml_file, "w");
            foreach ($generated_output as $generated_output_line) {
                fwrite($temp_xml_file_handler, $generated_output_line);
                fwrite($temp_xml_file_handler, "\n");
            }  
            exec("java -jar " . $jexamxml . " " . $declared_output_file . " " . $temp_xml_file . " delta.xml /pub/courses/ipp/jexamxml/options", $note, $result);

            if (($result == 0 && $declared_return_code == 0 && $generated_return_code == 0) || ($declared_return_code == $generated_return_code && $declared_return_code != 0 && $generated_return_code != 0)) {
                $html->insert_passed($work_dir . $test_file_info['filename'], $declared_return_code, $generated_return_code);
            } else {
                $html->insert_failed($work_dir . $test_file_info['filename'], $declared_return_code, $generated_return_code);
            }
            fclose($temp_xml_file_handler);
            unlink($temp_xml_file);

            if ($remove_file) {
                unlink($declared_output_file);
                $remove_file = false;
            }
            $generated_output = "";
        }
    }
    if (!$is_recursive_call) {
        $html->print_html();
    }
    if (!$is_recursive_call) {
        unlink("delta.xml");
    }
}
