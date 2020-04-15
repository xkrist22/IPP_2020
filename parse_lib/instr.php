<?php
/**
 * File contains class for working with instructions,
 * created 14. 2. 2020
 *
 * @author Jiri Kristof, xkrist22
 * @version 2.1
 */

/**
 * Class instruction holds data about instruction and operations for working with instructions
 * @var mixed|string $instr_name is NULL before construct, after constructing it holds name of instruction
 * @var mixed|string $ope1 is NULL before construct, after constructing it holds value of first operand
 * @var mixed|string $ope2 is NULL before construct, after constructing it holds value of second operand
 * @var mixed|string $ope3 is NULL before construct, after constructing it holds value of third operand
 * @var mixed|string $ope1_type is NULL before construct, after constructing it holds type of first operand
 * @var mixed|string $ope2_type is NULL before construct, after constructing it holds type of second operand
 * @var mixed|string $ope3_type is NULL before construct, after constructing it holds type of third operand
 */
    class instruction {
        private $instr_name = NULL;
        private $ope1 = NULL;
        private $ope1_type = NULL;
        private $ope2 = NULL;
        private $ope2_type = NULL;
        private $ope3 = NULL;
        private $ope3_type = NULL;

        /**
         * instruction constructor.
         * @param String $line is loaded line from STDIN (it should only contain non-only-whitespace line or non-only-comment line)
         */
        public function __construct($line) {
            // removing whitespaces from begin and end of the string
            $line = trim($line);
            // removing inline comment from line
            if (preg_match("/^[^#]+#.*/", $line)) {
                $line = strstr($line, '#', true);
                $line = trim($line);
            }

            // split line to words
            $words = preg_split("/\s+/", $line);

            // load object data from words
            if (count($words) == 1) {
                $this->instr_name = $words[0];

            } elseif (count($words) == 2) {
                $this->instr_name = $words[0];
                $this->ope1 = $words[1];

            } elseif (count($words) == 3) {
                $this->instr_name = $words[0];
                $this->ope1 = $words[1];
                $this->ope2 = $words[2];

            } elseif (count($words) == 4) {
                $this->instr_name = $words[0];
                $this->ope1 = $words[1];
                $this->ope2 = $words[2];
                $this->ope3 = $words[3];

            } else {
                error_handler(LEX_SYN_ERROR);
            }

            // checking if loaded instruction is valid
            // getting operand types
            $this->instruction_validation();
        }

        /**
         * Function check lexical and syntactic correctness of instruction and extracting operand types
         * @return bool return value is true, if instruction is correct; if it is not, method call function
         *              error_handler and the program ends with right error code
         */
        private function instruction_validation() {
            $instr_name = strtoupper($this->instr_name);

            /*
             * Note that strcmp returns 0 (equal to false), if strings are equal
             * and anything else if they are not equal, so return value is turned
             * with ! operator to get bool value if strings are equal or not.
             */
            if (!strcmp($instr_name, "MOVE")) {
                // MOVE <var> <symb>
                // checking number of operands
                if ($this->operand_count() != 2) {
                    error_handler(LEX_SYN_ERROR);
                }

                // checking operands
                if (!$this->ope_is_var($this->ope1)) {
                    error_handler(LEX_SYN_ERROR);
                }
                if (!$this->ope_is_symb($this->ope2)) {
                    error_handler(LEX_SYN_ERROR);
                }

                // getting operand types
                $this->ope1_type = $this->ope_is_var($this->ope1);
                $this->ope2_type = $this->ope_is_symb($this->ope2);

            } elseif (!strcmp($instr_name, "CREATEFRAME")) {
                // CREATEFRAME
                // checking number of operands
                if ($this->operand_count() != 0) {
                    error_handler(LEX_SYN_ERROR);
                }

            } elseif (!strcmp($instr_name, "PUSHFRAME")) {
                // PUSHFRAME
                // checking number of operands
                if ($this->operand_count() != 0) {
                    error_handler(LEX_SYN_ERROR);
                }

            } elseif (!strcmp($instr_name, "POPFRAME")) {
                // POPFRAME
                // checking number of operands
                if ($this->operand_count() != 0) {
                    error_handler(LEX_SYN_ERROR);
                }

            } elseif (!strcmp($instr_name, "DEFVAR")) {
                // DEFVAR <var>
                // checking number of operands
                if ($this->operand_count() != 1) {
                    print("err\n");
                    error_handler(LEX_SYN_ERROR);
                }

                // checking operands
                if (!$this->ope_is_var($this->ope1)) {
                    error_handler(LEX_SYN_ERROR);
                }

                // getting operand types
                $this->ope1_type = $this->ope_is_var($this->ope1);

            } elseif (!strcmp($instr_name, "CALL")) {
                // CALL <label>
                // checking number of operands
                if ($this->operand_count() != 1) {
                    error_handler(LEX_SYN_ERROR);
                }

                // checking operands
                if (!$this->ope_is_label($this->ope1)) {
                    error_handler(LEX_SYN_ERROR);
                }

                // getting operand types
                $this->ope1_type = $this->ope_is_label($this->ope1);

            } elseif (!strcmp($instr_name, "RETURN")) {
                // RETURN
                // checking number of operands
                if ($this->operand_count() != 0) {
                    error_handler(LEX_SYN_ERROR);
                }

            } elseif (!strcmp($instr_name, "PUSHS")) {
                // PUSHS <symb>
                // checking number of operands
                if ($this->operand_count() != 1) {
                    error_handler(LEX_SYN_ERROR);
                }

                // checking operands
                if (!$this->ope_is_symb($this->ope1)) {
                    error_handler(LEX_SYN_ERROR);
                }

                // getting operand types
                $this->ope1_type = $this->ope_is_symb($this->ope1);

            } elseif (!strcmp($instr_name, "POPS")) {
                // POPS <var>
                // checking number of operands
                if ($this->operand_count() != 1) {
                    error_handler(LEX_SYN_ERROR);
                }

                // checking operands
                if (!$this->ope_is_var($this->ope1)) {
                    error_handler(LEX_SYN_ERROR);
                }

                // getting operand types
                $this->ope1_type = $this->ope_is_var($this->ope1);

            } elseif (!strcmp($instr_name, "ADD")) {
                // ADD <var> <symb> <symb>
                // checking number of operands
                if ($this->operand_count() != 3) {
                    error_handler(LEX_SYN_ERROR);
                }

                // checking operands
                if (!$this->ope_is_var($this->ope1)) {
                    error_handler(LEX_SYN_ERROR);
                }
                if (!$this->ope_is_symb($this->ope2)) {
                    error_handler(LEX_SYN_ERROR);
                }
                if (!$this->ope_is_symb($this->ope3)) {
                    error_handler(LEX_SYN_ERROR);
                }

                // getting operand types
                $this->ope1_type = $this->ope_is_var($this->ope1);
                $this->ope2_type = $this->ope_is_symb($this->ope2);
                $this->ope3_type = $this->ope_is_symb($this->ope3);


            } elseif (!strcmp($instr_name, "SUB")) {
                // SUB <var> <symb> <symb>
                // checking number of operands
                if ($this->operand_count() != 3) {
                    error_handler(LEX_SYN_ERROR);
                }

                // checking operands
                if (!$this->ope_is_var($this->ope1)) {
                    error_handler(LEX_SYN_ERROR);
                }
                if (!$this->ope_is_symb($this->ope2)) {
                    error_handler(LEX_SYN_ERROR);
                }
                if (!$this->ope_is_symb($this->ope3)) {
                    error_handler(LEX_SYN_ERROR);
                }

                // getting operand types
                $this->ope1_type = $this->ope_is_var($this->ope1);
                $this->ope2_type = $this->ope_is_symb($this->ope2);
                $this->ope3_type = $this->ope_is_symb($this->ope3);

            } elseif (!strcmp($instr_name, "MUL")) {
                // MUL <var> <symb> <symb>
                // checking number of operands
                if ($this->operand_count() != 3) {
                    error_handler(LEX_SYN_ERROR);
                }

                // checking operands
                if (!$this->ope_is_var($this->ope1)) {
                    error_handler(LEX_SYN_ERROR);
                }
                if (!$this->ope_is_symb($this->ope2)) {
                    error_handler(LEX_SYN_ERROR);
                }
                if (!$this->ope_is_symb($this->ope3)) {
                    error_handler(LEX_SYN_ERROR);
                }

                // getting operand types
                $this->ope1_type = $this->ope_is_var($this->ope1);
                $this->ope2_type = $this->ope_is_symb($this->ope2);
                $this->ope3_type = $this->ope_is_symb($this->ope3);

            } elseif (!strcmp($instr_name, "IDIV")) {
                // IDIV <var> <symb> <symb>
                // checking number of operands
                if ($this->operand_count() != 3) {
                    error_handler(LEX_SYN_ERROR);
                }

                // checking operands
                if (!$this->ope_is_var($this->ope1)) {
                    error_handler(LEX_SYN_ERROR);
                }
                if (!$this->ope_is_symb($this->ope2)) {
                    error_handler(LEX_SYN_ERROR);
                }
                if (!$this->ope_is_symb($this->ope3)) {
                    error_handler(LEX_SYN_ERROR);
                }

                // getting operand types
                $this->ope1_type = $this->ope_is_var($this->ope1);
                $this->ope2_type = $this->ope_is_symb($this->ope2);
                $this->ope3_type = $this->ope_is_symb($this->ope3);

            } elseif (!strcmp($instr_name, "LT")) {
                // LT <var> <symb> <symb>
                // checking number of operands
                if ($this->operand_count() != 3) {
                    error_handler(LEX_SYN_ERROR);
                }

                // checking operands
                if (!$this->ope_is_var($this->ope1)) {
                    error_handler(LEX_SYN_ERROR);
                }
                if (!$this->ope_is_symb($this->ope2)) {
                    error_handler(LEX_SYN_ERROR);
                }
                if (!$this->ope_is_symb($this->ope3)) {
                    error_handler(LEX_SYN_ERROR);
                }

                // getting operand types
                $this->ope1_type = $this->ope_is_var($this->ope1);
                $this->ope2_type = $this->ope_is_symb($this->ope2);
                $this->ope3_type = $this->ope_is_symb($this->ope3);

            } elseif (!strcmp($instr_name, "GT")) {
                // GT <var> <symb> <symb>
                // checking number of operands
                if ($this->operand_count() != 3) {
                    error_handler(LEX_SYN_ERROR);
                }

                // checking operands
                if (!$this->ope_is_var($this->ope1)) {
                    error_handler(LEX_SYN_ERROR);
                }
                if (!$this->ope_is_symb($this->ope2)) {
                    error_handler(LEX_SYN_ERROR);
                }
                if (!$this->ope_is_symb($this->ope3)) {
                    error_handler(LEX_SYN_ERROR);
                }

                // getting operand types
                $this->ope1_type = $this->ope_is_var($this->ope1);
                $this->ope2_type = $this->ope_is_symb($this->ope2);
                $this->ope3_type = $this->ope_is_symb($this->ope3);

            } elseif (!strcmp($instr_name, "EQ")) {
                // EQ <var> <symb> <symb>
                // checking number of operands
                if ($this->operand_count() != 3) {
                    error_handler(LEX_SYN_ERROR);
                }

                // checking operands
                if (!$this->ope_is_var($this->ope1)) {
                    error_handler(LEX_SYN_ERROR);
                }
                if (!$this->ope_is_symb($this->ope2)) {
                    error_handler(LEX_SYN_ERROR);
                }
                if (!$this->ope_is_symb($this->ope3)) {
                    error_handler(LEX_SYN_ERROR);
                }

                // getting operand types
                $this->ope1_type = $this->ope_is_var($this->ope1);
                $this->ope2_type = $this->ope_is_symb($this->ope2);
                $this->ope3_type = $this->ope_is_symb($this->ope3);

            } elseif (!strcmp($instr_name, "AND")) {
                // AND <var> <symb> <symb>
                // checking number of operands
                if ($this->operand_count() != 3) {
                    error_handler(LEX_SYN_ERROR);
                }

                // checking operands
                if (!$this->ope_is_var($this->ope1)) {
                    error_handler(LEX_SYN_ERROR);
                }
                if (!$this->ope_is_symb($this->ope2)) {
                    error_handler(LEX_SYN_ERROR);
                }
                if (!$this->ope_is_symb($this->ope3)) {
                    error_handler(LEX_SYN_ERROR);
                }

                // getting operand types
                $this->ope1_type = $this->ope_is_var($this->ope1);
                $this->ope2_type = $this->ope_is_symb($this->ope2);
                $this->ope3_type = $this->ope_is_symb($this->ope3);

            } elseif (!strcmp($instr_name, "OR")) {
                // LT <var> <symb> <symb>
                // checking number of operands
                if ($this->operand_count() != 3) {
                    error_handler(LEX_SYN_ERROR);
                }

                // checking operands
                if (!$this->ope_is_var($this->ope1)) {
                    error_handler(LEX_SYN_ERROR);
                }
                if (!$this->ope_is_symb($this->ope2)) {
                    error_handler(LEX_SYN_ERROR);
                }
                if (!$this->ope_is_symb($this->ope3)) {
                    error_handler(LEX_SYN_ERROR);
                }

                // getting operand types
                $this->ope1_type = $this->ope_is_var($this->ope1);
                $this->ope2_type = $this->ope_is_symb($this->ope2);
                $this->ope3_type = $this->ope_is_symb($this->ope3);

            } elseif (!strcmp($instr_name, "NOT")) {
                // NOT <var> <symb>
                // checking number of operands
                if ($this->operand_count() != 2) {
                    error_handler(LEX_SYN_ERROR);
                }

                // checking operands
                if (!$this->ope_is_var($this->ope1)) {
                    error_handler(LEX_SYN_ERROR);
                }
                if (!$this->ope_is_symb($this->ope2)) {
                    error_handler(LEX_SYN_ERROR);
                }

                // getting operand types
                $this->ope1_type = $this->ope_is_var($this->ope1);
                $this->ope2_type = $this->ope_is_symb($this->ope2);

            } elseif (!strcmp($instr_name, "INT2CHAR")) {
                // INT2CHAR <var> <symb>
                // checking number of operands
                if ($this->operand_count() != 2) {
                    error_handler(LEX_SYN_ERROR);
                }

                // checking operands
                if (!$this->ope_is_var($this->ope1)) {
                    error_handler(LEX_SYN_ERROR);
                }
                if (!$this->ope_is_symb($this->ope2)) {
                    error_handler(LEX_SYN_ERROR);
                }

                // getting operand types
                $this->ope1_type = $this->ope_is_var($this->ope1);
                $this->ope2_type = $this->ope_is_symb($this->ope2);

            } elseif (!strcmp($instr_name, "STRI2INT")) {
                // STRI2INT <var> <symb> <symb>
                // checking number of operands
                if ($this->operand_count() != 3) {
                    error_handler(LEX_SYN_ERROR);
                }

                // checking operands
                if (!$this->ope_is_var($this->ope1)) {
                    error_handler(LEX_SYN_ERROR);
                }
                if (!$this->ope_is_symb($this->ope2)) {
                    error_handler(LEX_SYN_ERROR);
                }
                if (!$this->ope_is_symb($this->ope3)) {
                    error_handler(LEX_SYN_ERROR);
                }

                // getting operand types
                $this->ope1_type = $this->ope_is_var($this->ope1);
                $this->ope2_type = $this->ope_is_symb($this->ope2);
                $this->ope3_type = $this->ope_is_symb($this->ope3);

            } elseif (!strcmp($instr_name, "READ")) {
                // READ <var> <type>
                // checking number of operands
                if ($this->operand_count() != 2) {
                    error_handler(LEX_SYN_ERROR);
                }
                // checking operands
                if (!$this->ope_is_var($this->ope1)) {
                    error_handler(LEX_SYN_ERROR);
                }
                if (!$this->ope_is_type($this->ope2)) {
                    error_handler(LEX_SYN_ERROR);
                }

                // getting operand types
                $this->ope1_type = $this->ope_is_var($this->ope1);
                $this->ope2_type = $this->ope_is_type($this->ope2);


            } elseif (!strcmp($instr_name, "WRITE")) {
                // WRITE <symb>
                // checking number of operands
                if ($this->operand_count() != 1) {
printf("count error\n");
                    error_handler(LEX_SYN_ERROR);
                }
                // checking operands
                if (!$this->ope_is_symb($this->ope1)) {
printf("symb error\n");
                    error_handler(LEX_SYN_ERROR);
                }

                // getting operand types
                $this->ope1_type = $this->ope_is_symb($this->ope1);

            } elseif (!strcmp($instr_name, "CONCAT")) {
                // CONCAT <var> <symb> <symb>
                // checking number of operands
                if ($this->operand_count() != 3) {
                    error_handler(LEX_SYN_ERROR);
                }

                // checking operands
                if (!$this->ope_is_var($this->ope1)) { 
                    error_handler(LEX_SYN_ERROR);
                }
                if (!$this->ope_is_symb($this->ope2)) {
                    error_handler(LEX_SYN_ERROR);
                }
                if (!$this->ope_is_symb($this->ope3)) {
                    error_handler(LEX_SYN_ERROR);
                }

                // getting operand types
                $this->ope1_type = $this->ope_is_var($this->ope1);
                $this->ope2_type = $this->ope_is_symb($this->ope2);
                $this->ope3_type = $this->ope_is_symb($this->ope3);

            } elseif (!strcmp($instr_name, "STRLEN")) {
                // STRLEN <var> <symb>
                // checking number of operands
                if ($this->operand_count() != 2) {
                    error_handler(LEX_SYN_ERROR);
                }

                // checking operands
                if (!$this->ope_is_var($this->ope1)) {
                    error_handler(LEX_SYN_ERROR);
                }
                if (!$this->ope_is_symb($this->ope2)) {
                    error_handler(LEX_SYN_ERROR);
                }

                // getting operand types
                $this->ope1_type = $this->ope_is_var($this->ope1);
                $this->ope2_type = $this->ope_is_symb($this->ope2);

            } elseif (!strcmp($instr_name, "GETCHAR")) {
                // GETCHAR <var> <symb> <symb>
                // checking number of operands
                if ($this->operand_count() != 3) {
                    error_handler(LEX_SYN_ERROR);
                }

                // checking operands
                if (!$this->ope_is_var($this->ope1)) {
                    error_handler(LEX_SYN_ERROR);
                }
                if (!$this->ope_is_symb($this->ope2)) {
                    error_handler(LEX_SYN_ERROR);
                }
                if (!$this->ope_is_symb($this->ope3)) {
                    error_handler(LEX_SYN_ERROR);
                }

                // getting operand types
                $this->ope1_type = $this->ope_is_var($this->ope1);
                $this->ope2_type = $this->ope_is_symb($this->ope2);
                $this->ope3_type = $this->ope_is_symb($this->ope3);

            } elseif (!strcmp($instr_name, "SETCHAR")) {
                // SETCHAR <var> <symb> <symb>
                // checking number of operands
                if ($this->operand_count() != 3) {
                    error_handler(LEX_SYN_ERROR);
                }

                // checking operands
                if (!$this->ope_is_var($this->ope1)) {
                    error_handler(LEX_SYN_ERROR);
                }
                if (!$this->ope_is_symb($this->ope2)) {
                    error_handler(LEX_SYN_ERROR);
                }
                if (!$this->ope_is_symb($this->ope3)) {
                    error_handler(LEX_SYN_ERROR);
                }

                // getting operand types
                $this->ope1_type = $this->ope_is_var($this->ope1);
                $this->ope2_type = $this->ope_is_symb($this->ope2);
                $this->ope3_type = $this->ope_is_symb($this->ope3);

            } elseif (!strcmp($instr_name, "TYPE")) {
                // TYPE <var> <symb>
                // checking number of operands
                if ($this->operand_count() != 2) {
                    error_handler(LEX_SYN_ERROR);
                }

                // checking operands
                if (!$this->ope_is_var($this->ope1)) {
                    error_handler(LEX_SYN_ERROR);
                }
                if (!$this->ope_is_symb($this->ope2)) {
                    error_handler(LEX_SYN_ERROR);
                }

                // getting operand types
                $this->ope1_type = $this->ope_is_var($this->ope1);
                $this->ope2_type = $this->ope_is_symb($this->ope2);

            } elseif (!strcmp($instr_name, "LABEL")) {
                // LABEL <label>
                // checking number of operands
                if ($this->operand_count() != 1) {
                    error_handler(LEX_SYN_ERROR);
                }

                // checking operands
                if (!$this->ope_is_label($this->ope1)) {
                    error_handler(LEX_SYN_ERROR);
                }

                // getting operand types
                $this->ope1_type = $this->ope_is_label($this->ope1);

            } elseif (!strcmp($instr_name, "JUMP")) {
                // JUMP <label>
                // checking number of operands
                if ($this->operand_count() != 1) {
                    error_handler(LEX_SYN_ERROR);
                }

                // checking operands
                if (!$this->ope_is_label($this->ope1)) {
                    error_handler(LEX_SYN_ERROR);
                }

                // getting operand types
                $this->ope1_type = $this->ope_is_label($this->ope1);

            } elseif (!strcmp($instr_name, "JUMPIFEQ")) {
                // JUMPIFEQ <label> <symb> <symb>
                // checking number of operands
                if ($this->operand_count() != 3) {
                    error_handler(LEX_SYN_ERROR);
                }

                // checking operands
                if (!$this->ope_is_label($this->ope1)) {
                    printf("label 1 error");
                    error_handler(LEX_SYN_ERROR);
                }
                if (!$this->ope_is_symb($this->ope2)) {
                    printf("symb 2 error");
                    error_handler(LEX_SYN_ERROR);
                }
                if (!$this->ope_is_symb($this->ope3)) {
                    printf("symb 3 error");
                    error_handler(LEX_SYN_ERROR);
                }

                // getting operand types
                $this->ope1_type = $this->ope_is_label($this->ope1);
                $this->ope2_type = $this->ope_is_symb($this->ope2);
                $this->ope3_type = $this->ope_is_symb($this->ope3);

            } elseif (!strcmp($instr_name, "JUMPIFNEQ")) {
                // JUMPIFNEQ <label> <symb> <symb>
                // checking number of operands
                if ($this->operand_count() != 3) {
                    error_handler(LEX_SYN_ERROR);
                }

                // checking operands
                if (!$this->ope_is_label($this->ope1)) {
                    error_handler(LEX_SYN_ERROR);
                }
                if (!$this->ope_is_symb($this->ope2)) {
                    error_handler(LEX_SYN_ERROR);
                }
                if (!$this->ope_is_symb($this->ope3)) {
                    error_handler(LEX_SYN_ERROR);
                }

                // getting operand types
                $this->ope1_type = $this->ope_is_label($this->ope1);
                $this->ope2_type = $this->ope_is_symb($this->ope2);
                $this->ope3_type = $this->ope_is_symb($this->ope3);

            } elseif (!strcmp($instr_name, "EXIT")) {
                // EXIT <symb>
                // checking number of operands
                if ($this->operand_count() != 1) {
                    error_handler(LEX_SYN_ERROR);
                }

                // checking operands
                if (!$this->ope_is_symb($this->ope1)) {
                    error_handler(LEX_SYN_ERROR);
                }

                // getting operand types
                $this->ope1_type = $this->ope_is_symb($this->ope1);

            } elseif (!strcmp($instr_name, "DPRINT")) {
                // DPRINT <symb>
                // checking number of operands
                if ($this->operand_count() != 1) {
                    error_handler(LEX_SYN_ERROR);
                }

                // checking operands
                if (!$this->ope_is_symb($this->ope1)) {
                    error_handler(LEX_SYN_ERROR);
                }

                // getting operand types
                $this->ope1_type = $this->ope_is_symb($this->ope1);

            } elseif (!strcmp($instr_name, "BREAK")) {
                // BREAK
                // checking number of operands
                if ($this->operand_count() != 0) {
                    error_handler(LEX_SYN_ERROR);
                }

            } else {
                // unknown opcode
                error_handler(UNKNOWN_OPCODE);
            }
            return true;
        }

        /**
         * Function for accessing (only reading) to the name of opcode
         * @return mixed|string|null value of the opcode UPPERCACED
         */
        public function opcode() {
            return strtoupper($this->instr_name);
        }

        /**
         * Function for accessing (only reading) to the name of first operand
         * @return mixed|string|null string value of the first operand, if there is no operand, returns NULL
         */
        public function operand_1() {
            if ($this->ope1 == NULL) {
                return NULL;
            }

            if (preg_match("/label|type|var/", $this->ope1_type)) {
                // if operand type is type, var or label, send in as it is
                $str = preg_replace("/&/", "&amp;", $this->ope1);
                $str = preg_replace("/</", "&lt;", $str);
                $str = preg_replace("/>/", "&gt;", $str);
                $str = preg_replace("/\"/", "&quot;", $str);
                $str = preg_replace("/'/", "&apos;", $str);
            } elseif (preg_match("/int|bool|nil/", $this->ope1_type)) {
                // if operand type is int, bool or nil, send it without type info and @ char
                $str = preg_replace("/int@|string@|bool@|nil@/", "", $this->ope1, 1);
            } else {
                // if operand type is string, send it without type info, @ char and change <, > and & chars
                $str = preg_replace("/string@/", "", $this->ope1, 1);
                $str = preg_replace("/&/", "&amp;", $str);
                $str = preg_replace("/</", "&lt;", $str);
                $str = preg_replace("/>/", "&gt;", $str);
                $str = preg_replace("/\"/", "&quot;", $str);
                $str = preg_replace("/'/", "&apos;", $str);
 
            }

            /*
             * WARNING: string can be now empty, so we insert into it value,
             * which it cannot really have to notify about this situation
             */
            if ($str === '') {
                $str = "#";
            }
            return $str;
        }

        /**
         * Function for accessing (only reading) to the name of second operand
         * @return mixed|string|null string value of the second operand, if there is no operand, returns NULL
         */
        public function operand_2() {
            if ($this->ope2 == NULL) {
                return NULL;
            }

            if (preg_match("/label|type|var/", $this->ope2_type)) {
                // if operand type is type, var or label, send in as it is
                $str = preg_replace("/&/", "&amp;", $this->ope2);
                $str = preg_replace("/</", "&lt;", $str);
                $str = preg_replace("/>/", "&gt;", $str);
                $str = preg_replace("/\"/", "&quot;", $str);
                $str = preg_replace("/'/", "&apos;", $str);

            }  elseif (preg_match("/int|bool|nil/", $this->ope2_type)) {
                // if operand type is int, bool or nil, send it without type info and @ char
                $str = preg_replace("/int@|string@|bool@|nil@/", "", $this->ope2, 1);
            } else {
                // if operand type is string, send it without type info, @ char and change <, > and & chars
                $str = preg_replace("/string@/", "", $this->ope2, 1);
                $str = preg_replace("/&/", "&amp;", $str);
                $str = preg_replace("/</", "&lt;", $str);
                $str = preg_replace("/>/", "&gt;", $str);
                $str = preg_replace("/\"/", "&quot;", $str);
                $str = preg_replace("/'/", "&apos;", $str);
            }

            /*
             * WARNING: value of operand can be now empty (after deleting type info),
             * so we insert into it value, which it cannot really have to notify about this situation
             */
            if ($str === '') {
                $str = "#";
            }
            return $str;
        }

        /**
         * Function for accessing (only reading) to the name third operand
         * @return mixed|string|null string value of the third operand, if there is no operand, returns NULL
         */
        public function operand_3() {
            if ($this->ope3 == NULL) {
                return NULL;
            }

            if (preg_match("/label|type|var/", $this->ope3_type)) {
                // if operand type is type, var or label, send in as it is
                $str = preg_replace("/&/", "&amp;", $this->ope3);
                $str = preg_replace("/</", "&lt;", $str);
                $str = preg_replace("/>/", "&gt;", $str);
                $str = preg_replace("/\"/", "&quot;", $str);
                $str = preg_replace("/'/", "&apos;", $str);
            }  elseif (preg_match("/int|bool|nil/", $this->ope3_type)) {
                // if operand type is int, bool or nil, send it without type info and @ char
                $str = preg_replace("/int@|string@|bool@|nil@/", "", $this->ope3, 1);
            } else {
                // if operand type is string, send it without type info, @ char and change <, > and & chars
                $str = preg_replace("/string@/", "", $this->ope3, 1);
                $str = preg_replace("/&/", "&amp;", $str);
                $str = preg_replace("/</", "&lt;", $str);
                $str = preg_replace("/>/", "&gt;", $str);
                $str = preg_replace("/\"/", "&quot;", $str);
                $str = preg_replace("/'/", "&apos;", $str);
           }

            /*
             * WARNING: string can be now empty, so we insert into it value,
             * which it cannot really have to notify about this situation
             */
            if ($str === '') {
                $str = "#";
            }
            return $str;
        }

        public function get_ope1_type() {
            return $this->ope1_type;
        }

        public function get_ope2_type() {
            return $this->ope2_type;
        }

        public function get_ope3_type() {
            return $this->ope3_type;
        }

        /**
         * @param mixed $ope value of the operand, which method check
         * @return mixed|string|bool method return string "var", if operand is valid variable in language IPPcode20
         *                           method return false, if it is not valid variable
         */
        private function ope_is_var($ope) {
            if (preg_match("/^[GLT]F@[A-Za-z_$%&*!?\-][A-Za-z0-9_$%&*!?\-]*$/", $ope)) {
                return "var";
            } else {
                return false;
            }
        }

        /**
         * @param mixed $ope value of the operand, which method check
         * @return mixed|string|bool method return string representing type of the operand
         *                           , if operand is valid variable or constant in language IPPcode20
         *                           method return false, if it is not valid variable or constant
         */
        private function ope_is_symb($ope) {
            if (preg_match("/^[GLT]{0,1}F@[A-Za-z0-9_$%&*!?\-]+$/", $ope)) {
                return "var";
            } elseif (preg_match("/^bool@(true|false){0,1}$/", $ope)) {
                return "bool";
            } elseif (preg_match("/^nil@(nil){0,1}$/", $ope)) {
                return "nil";
            } elseif (preg_match("/^int@[+-]{0,1}[0-9]+$/", $ope)) {
                return "int";
            } elseif (preg_match("/^string@(([^ \s\\\#])|(\\\[0-9]{3}))*$/", $ope)) {
                return "string";
            } else {
                return false;
            }
        }

        /**
         * @param mixed $ope value of the operand, which method check
         * @return mixed|string|bool method return string "type", if operand is in set {int, string, bool},
         *              else it return false
         *
         */
        private function ope_is_type($ope) {
            if (preg_match("/^(int|string|bool)$/", $ope)) {
                return "type";
            } else {
                return false;
            }
        }

        /**
         * @param mixed $ope value of the operand, which method check
         * @return mixed|string|bool method return string "label", if operand is valid label in language IPPcode20
         *              method return false, if it is not valid label
         */
        private function ope_is_label($ope) {
            if (preg_match("/^[A-Za-z0-9_$%&*!?\-]+$/", $ope)) {
                return "label";
            } else {
                return false;
            }

        }

        /**
         * @return int method return number of operands of instruction
         */
        private function operand_count() {
            $count = 0;
            if ($this->ope1 != NULL) {
                $count++;
            }
            if ($this->ope2 != NULL) {
                $count++;
            }
            if ($this->ope3 != NULL) {
                $count++;
            }
            return $count;
        }
    }
?>
