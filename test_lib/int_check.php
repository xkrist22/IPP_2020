<?php
/**
 * File contains function for checking parse.php,
 * created 9. 3. 2020
 *
 * @author Jiri Kristof, xkrist22
 * @version 1
 */

/**
 * @param string $dir_with_tests contains path to directory containing tests
 * @param string $int_script contains path to file containing script for interpreting
 * @param bool $recursive if it is true, function will be searching for test cases in subdirectories of $dir_with_tests
 * @param string $work_dir is directory from which test.php is invoke
 * @param bool $is_recursive_call decide whether the calling of function is done recursively or not
 */
function check_interpreter($dir_with_tests, $int_script, $recursive, $work_dir, $is_recursive_call = false) {
    $html = html_gen::get_instance("interpret.py");
    $extracted_test_files = scandir($dir_with_tests);

    foreach ($extracted_test_files as $test_file) {
        if ($test_file == "." || $test_file == "..") {
            continue;
        }

        if (is_dir($work_dir . $test_file) && $recursive) {
            check_interpreter($dir_with_tests . DIRECTORY_SEPARATOR . $test_file, $int_script, $recursive, $work_dir . $test_file . DIRECTORY_SEPARATOR, true);
        } else {
            $test_file_info = pathinfo($dir_with_tests . DIRECTORY_SEPARATOR . $test_file);
            if ($test_file_info['extension'] != "src") {
                continue;
            }

            // get data from .out file
            $delete_temp_output_file = false;
            if (file_exists($dir_with_tests . DIRECTORY_SEPARATOR . $test_file_info['filename'] . ".out")) {
                $declared_output_file = $dir_with_tests . DIRECTORY_SEPARATOR . $test_file_info['filename'] . ".out";
            } else {
                $declared_output_file = tempnam($dir_with_tests, "temp");
                $delete_temp_output_file = true;
            }

            // get data from .in file
            $delete_temp_input_file = false;
            if (file_exists($dir_with_tests . DIRECTORY_SEPARATOR . $test_file_info['filename'] . ".in")) {
                $input_file = $dir_with_tests . DIRECTORY_SEPARATOR . $test_file_info['filename'] . ".in";
            } else {
                $input_file = tempnam($dir_with_tests, "temp");
                $delete_temp_input_file = true;
            }

            // get data from .rc file
            $declared_return_code = 0;
            if (file_exists($dir_with_tests . DIRECTORY_SEPARATOR . $test_file_info['filename'] . ".rc")) {
                $declared_return_code = file_get_contents($dir_with_tests . DIRECTORY_SEPARATOR . $test_file_info['filename'] . ".rc", true);
            }



            $result_file = tempnam($dir_with_tests, "temp");
            exec("python3 " . $int_script . " --source=" . $dir_with_tests . DIRECTORY_SEPARATOR . $test_file . " --input=" . $input_file . " >" . $result_file,$_, $generated_return_code);

            exec("diff " . $result_file . " " . $declared_output_file, $_, $diff_result);

            if (($generated_return_code == 0 && $declared_return_code == 0 && $diff_result == 0) || ($declared_return_code == $generated_return_code && $declared_return_code != 0 && $generated_return_code != 0)) {
                $html->insert_passed($work_dir . $test_file_info['filename'], $declared_return_code, $generated_return_code);
            } else {
                $html->insert_failed($work_dir . $test_file_info['filename'], $declared_return_code, $generated_return_code);
            }

            if ($delete_temp_input_file) {
                unlink($input_file);
            }
            if ($delete_temp_output_file) {
                unlink($declared_output_file);
            }
            unlink($result_file);
        }
    }
    if (!$is_recursive_call) {
        $html->print_html();
    }
}
