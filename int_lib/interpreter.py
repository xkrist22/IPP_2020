import int_lib.err
import int_lib.hash_table
import int_lib.stack
import re
import sys


class interpreter:
    def __init__(self, xml_code, input_text):
        self.__global_frame = int_lib.hash_table.hash_table()  #
        self.__input = input_text
        self.__input_line_index = 0
        self.__xml_code_root = xml_code
        self.__data_stack = int_lib.stack.stack()  #
        self.__frame_stack = int_lib.stack.stack()  #
        self.__labels = int_lib.hash_table.hash_table()  #
        self.__global_frame = int_lib.hash_table.hash_table()  #
        self.__temp_frame = None  #
        self.__call_stack = int_lib.stack.stack()  #

    def interpreting_init(self):
        self.check_xml_structure()
        self.interpreting()

    def check_xml_structure(self):
        # checking of tag <program>
        if (self.__xml_code_root.tag != "program"):
            int_lib.err.error_handler(int_lib.err.BAD_XML_STRUCTURE)

        if ("language" not in self.__xml_code_root.attrib.keys()):
            int_lib.err.error_handler(int_lib.err.BAD_XML_STRUCTURE)

        if (self.__xml_code_root.attrib['language'] != "IPPcode20"):
            int_lib.err.error_handler(int_lib.err.BAD_XML_STRUCTURE)

        for key in self.__xml_code_root.attrib.keys():
            if (key != "name" and key != "description" and key != "language"):
                int_lib.err.error_handler(int_lib.err.BAD_XML_STRUCTURE)

        # checking of tags <instruction>
        order_arr = []
        for instruction_tag in self.__xml_code_root:
            if (instruction_tag.tag != "instruction"):
                int_lib.err.error_handler(int_lib.err.BAD_XML_STRUCTURE)

            if (len(instruction_tag) < 0 or len(instruction_tag) > 3):
                int_lib.err.error_handler(int_lib.err.BAD_XML_STRUCTURE)

            if (len(instruction_tag) == 1):
                if (instruction_tag[0].tag != "arg1"):
                    int_lib.err.error_handler(int_lib.err.BAD_XML_STRUCTURE)

            if (len(instruction_tag) == 2):
                if (instruction_tag[0].tag == "arg2" and instruction_tag[1].tag == "arg1"):
                    temp = instruction_tag[0]
                    instruction_tag[0] = instruction_tag[1]
                    instruction_tag[1] = temp
                if (instruction_tag[0].tag != "arg1"):
                    int_lib.err.error_handler(int_lib.err.BAD_XML_STRUCTURE)
                if (instruction_tag[1].tag != "arg2"):
                    int_lib.err.error_handler(int_lib.err.BAD_XML_STRUCTURE)

            if (len(instruction_tag) == 3):
                if (instruction_tag[0].tag == "arg1" and instruction_tag[1].tag == "arg3" and instruction_tag[2].tag =="arg2"):
                    temp = instruction_tag[1]
                    instruction_tag[1] = instruction_tag[2]
                    instruction_tag[2] = temp

                elif (instruction_tag[0].tag == "arg2" and instruction_tag[1].tag == "arg1" and instruction_tag[2].tag =="arg3"):
                    temp = instruction_tag[0]
                    instruction_tag[0] = instruction_tag[1]
                    instruction_tag[1] = temp

                elif (instruction_tag[0].tag == "arg2" and instruction_tag[1].tag == "arg3" and instruction_tag[2].tag =="arg1"):
                    temp_i0 = instruction_tag[0]
                    temp_i1 = instruction_tag[1]
                    instruction_tag[0] = instruction_tag[2]
                    instruction_tag[1] = temp_i0
                    instruction_tag[2] = temp_i1

                elif (instruction_tag[0].tag == "arg3" and instruction_tag[1].tag == "arg1" and instruction_tag[2].tag =="arg2"):
                    temp_i0 = instruction_tag[0]
                    temp_i2 = instruction_tag[2]
                    instruction_tag[0] = instruction_tag[1]
                    instruction_tag[1] = temp_i2
                    instruction_tag[2] = temp_i0

                elif (instruction_tag[0].tag == "arg3" and instruction_tag[1].tag == "arg2" and instruction_tag[2].tag =="arg1"):
                    temp = instruction_tag[0]
                    instruction_tag[0] = instruction_tag[2]
                    instruction_tag[2] = temp
 

                if (instruction_tag[0].tag != "arg1"):
                    int_lib.err.error_handler(int_lib.err.BAD_XML_STRUCTURE)
                if (instruction_tag[1].tag != "arg2"):
                    int_lib.err.error_handler(int_lib.err.BAD_XML_STRUCTURE)
                if (instruction_tag[2].tag != "arg3"):
                    int_lib.err.error_handler(int_lib.err.BAD_XML_STRUCTURE)

            if ("order" not in instruction_tag.attrib.keys()):
                int_lib.err.error_handler(int_lib.err.BAD_XML_STRUCTURE)
            if ("opcode" not in instruction_tag.attrib.keys()):
                int_lib.err.error_handler(int_lib.err.BAD_XML_STRUCTURE)

            instruction_tag.attrib['order'] = int(instruction_tag.attrib['order'])
            if (instruction_tag.attrib['order'] in order_arr or instruction_tag.attrib['order'] <= 0):
                int_lib.err.error_handler(int_lib.err.BAD_XML_STRUCTURE)
            order_arr.append(instruction_tag.attrib['order'])

            for key in instruction_tag.attrib.keys():
                if (key != "order" and key != "opcode"):
                    int_lib.err.error_handler(int_lib.err.BAD_XML_STRUCTURE)


            for arg_tag in instruction_tag:
                if (arg_tag.tag != "arg1" and arg_tag.tag != "arg2" and arg_tag.tag != "arg3"):
                    int_lib.err.error_handler(int_lib.err.BAD_XML_STRUCTURE)

                if ("type" not in arg_tag.attrib.keys()):
                    int_lib.err.error_handler(int_lib.err.BAD_XML_STRUCTURE)

                for key in arg_tag.attrib.keys():
                    if (key != "type"):
                        int_lib.err.error_handler(int_lib.err.BAD_XML_STRUCTURE)


                for err_tag in arg_tag:
                    if (err_tag):
                        int_lib.err.error_handler(int_lib.err.BAD_XML_STRUCTURE)

    @staticmethod
    def check_arg_count(instruction, arg_count):
        if (len(instruction) != arg_count):
            int_lib.err.error_handler(int_lib.err.BAD_XML_STRUCTURE)

    @staticmethod
    def check_types(instruction, type1=None, type2=None, type3=None):
        if (type1):
            if (not re.match(type1, instruction[0].attrib['type'])):
                int_lib.err.error_handler(int_lib.err.BAD_OPERAND_TYPES)
        if (type2):
            if (not re.match(type2, instruction[1].attrib['type'])):
                int_lib.err.error_handler(int_lib.err.BAD_OPERAND_TYPES)
        if (type3):
            if (not re.match(type3, instruction[2].attrib['type'])):
                int_lib.err.error_handler(int_lib.err.BAD_OPERAND_TYPES)

    def check_frame(self, check_tf = False, check_lf = False):
        if (check_tf and not check_lf):
            if (self.__temp_frame == None):
                return False
            else:
                return True
        elif (not check_tf and check_lf):
            if (not self.__frame_stack.is_empty()):
                return True
            else:
                return False
        elif (check_tf and check_lf):
            if (self.__temp_frame == None or self.__frame_stack.is_empty()):
                return False
            else:
                return True
        else:
            return None

    def exists(self, var):
        frame = self.get_frame(var.text)
        if (frame == 0):  # global frame
            if (self.__global_frame.search(var.text[3:])):
                return True
            else:
                return False
        elif (frame == 1):  # local grame
            if (self.__frame_stack.is_empty()):
                return None
            if (self.__frame_stack.top().search(var.text[3:])):
                return True
            else:
                return False
        else:  # temp frame
            try:
                if (self.__temp_frame.search(var.text[3:])):
                    return True
                else:
                    return False
            except AttributeError:
                return None

    def get_var_value(self, arg):
        if (arg.attrib['type'] != "var"):
            return None
        frame = self.get_frame(arg.text)
        if (frame == 0):  # global frame
            value = self.__global_frame.read(arg.text[3:])
            if (isinstance(value, bool)):
                int_lib.err.error_handler(int_lib.err.NOT_EXISTING_VARIABLE)
            else:
                return self.__global_frame.read(arg.text[3:])[1]
        elif (frame == 1):  # local frame
            if (self.check_frame(check_lf=True) == True):
                value = self.__frame_stack.top().read(arg.text[3:])
                if (isinstance(value, bool)):
                    int_lib.err.error_handler(int_lib.err.NOT_EXISTING_VARIABLE)
                else:
                    return self.__frame_stack.top().read(arg.text[3:])[1]
            else:
                int_lib.err.error_handler(int_lib.err.NOT_EXISTING_FRAME)
        else:  # temp frame
            if (self.check_frame(check_tf=True) == True):
                value = self.__temp_frame.read(arg.text[3:])
                if (isinstance(value, bool)):
                    int_lib.err.error_handler(int_lib.err.NOT_EXISTING_VARIABLE)
                else:
                    return self.__temp_frame.read(arg.text[3:])[1]
            else:
                int_lib.err.error_handler(int_lib.err.NOT_EXISTING_FRAME)

    def get_var_type(self, arg):
        if (arg.attrib['type'] != "var"):
            return None
        frame = self.get_frame(arg.text)
        if (frame == 0):  # global frame
            value = self.__global_frame.read(arg.text[3:])
            if (isinstance(value, bool)):
                int_lib.err.error_handler(int_lib.err.NOT_EXISTING_VARIABLE)
            else:
                return self.__global_frame.read(arg.text[3:])[0]
        elif (frame == 1):  # local frame
            if (self.check_frame(check_lf=True) == True):
                value = self.__frame_stack.top().read(arg.text[3:])
                if (isinstance(value, bool)):
                    int_lib.err.error_handler(int_lib.err.NOT_EXISTING_VARIABLE)
                else:
                    return self.__frame_stack.top().read(arg.text[3:])[0]
            else:
                int_lib.err.error_handler(int_lib.err.NOT_EXISTING_FRAME)
        else:  # temp frame
            if (self.check_frame(check_tf=True) == True):
                value = self.__temp_frame.read(arg.text[3:])
                if (isinstance(value, bool)):
                    int_lib.err.error_handler(int_lib.err.NOT_EXISTING_VARIABLE)
                else:
                    return self.__temp_frame.read(arg.text[3:])[0]
            else:
                int_lib.err.error_handler(int_lib.err.NOT_EXISTING_FRAME)

    @staticmethod
    def get_frame(var):
        if (var[:2] == "GF"):
            return 0
        elif (var[:2] == "LF"):
            return 1
        elif (var[:2] == "TF"):
            return 2
        else:
            int_lib.err.error_handler(int_lib.err.SEMANTICS_ERROR)

    def interpreting(self):
        i = 0
        # first loop for getting labels
        while i < len(self.__xml_code_root):
            if (self.__xml_code_root[i].attrib['opcode'].upper() == "LABEL"):
                self.call_label(self.__xml_code_root[i], i)
            i = i + 1

        i = 0
        # second loop for executing code
        while i < len(self.__xml_code_root):
            if (self.__xml_code_root[i].attrib['opcode'].upper() == "MOVE"):
                self.call_move(self.__xml_code_root[i])

            elif (self.__xml_code_root[i].attrib['opcode'].upper() == "CREATEFRAME"):
                self.call_createframe(self.__xml_code_root[i])

            elif (self.__xml_code_root[i].attrib['opcode'].upper() == "PUSHFRAME"):
                self.call_pushframe(self.__xml_code_root[i])

            elif (self.__xml_code_root[i].attrib['opcode'].upper() == "POPFRAME"):
                self.call_popframe(self.__xml_code_root[i])

            elif (self.__xml_code_root[i].attrib['opcode'].upper() == "DEFVAR"):
                self.call_defvar(self.__xml_code_root[i])

            elif (self.__xml_code_root[i].attrib['opcode'].upper() == "CALL"):
                i = self.call_call(self.__xml_code_root[i], i)
                continue

            elif (self.__xml_code_root[i].attrib['opcode'].upper() == "RETURN"):
                i = self.call_return(self.__xml_code_root[i])
                continue

            elif (self.__xml_code_root[i].attrib['opcode'].upper() == "PUSHS"):
                self.call_pushs(self.__xml_code_root[i])

            elif (self.__xml_code_root[i].attrib['opcode'].upper() == "POPS"):
                self.call_pops(self.__xml_code_root[i])

            elif (self.__xml_code_root[i].attrib['opcode'].upper() == "ADD"):
                self.call_add(self.__xml_code_root[i])

            elif (self.__xml_code_root[i].attrib['opcode'].upper() == "SUB"):
                self.call_sub(self.__xml_code_root[i])

            elif (self.__xml_code_root[i].attrib['opcode'].upper() == "MUL"):
                self.call_mul(self.__xml_code_root[i])

            elif (self.__xml_code_root[i].attrib['opcode'].upper() == "IDIV"):
                self.call_idiv(self.__xml_code_root[i])

            elif (self.__xml_code_root[i].attrib['opcode'].upper() == "LT"):
                self.call_lt(self.__xml_code_root[i])

            elif (self.__xml_code_root[i].attrib['opcode'].upper() == "GT"):
                self.call_gt(self.__xml_code_root[i])

            elif (self.__xml_code_root[i].attrib['opcode'].upper() == "EQ"):
                self.call_eq(self.__xml_code_root[i])

            elif (self.__xml_code_root[i].attrib['opcode'].upper() == "AND"):
                self.call_and(self.__xml_code_root[i])

            elif (self.__xml_code_root[i].attrib['opcode'].upper() == "OR"):
                self.call_or(self.__xml_code_root[i])

            elif (self.__xml_code_root[i].attrib['opcode'].upper() == "NOT"):
                self.call_not(self.__xml_code_root[i])

            elif (self.__xml_code_root[i].attrib['opcode'].upper() == "INT2CHAR"):
                self.call_int2char(self.__xml_code_root[i])

            elif (self.__xml_code_root[i].attrib['opcode'].upper() == "STRI2INT"):
                self.call_stri2int(self.__xml_code_root[i])

            elif (self.__xml_code_root[i].attrib['opcode'].upper() == "READ"):
                self.call_read(self.__xml_code_root[i])

            elif (self.__xml_code_root[i].attrib['opcode'].upper() == "WRITE"):
                self.call_write(self.__xml_code_root[i])

            elif (self.__xml_code_root[i].attrib['opcode'].upper() == "CONCAT"):
                self.call_concat(self.__xml_code_root[i])

            elif (self.__xml_code_root[i].attrib['opcode'].upper() == "STRLEN"):
                self.call_strlen(self.__xml_code_root[i])

            elif (self.__xml_code_root[i].attrib['opcode'].upper() == "GETCHAR"):
                self.call_getchar(self.__xml_code_root[i])

            elif (self.__xml_code_root[i].attrib['opcode'].upper() == "SETCHAR"):
                self.call_setchar(self.__xml_code_root[i])

            elif (self.__xml_code_root[i].attrib['opcode'].upper() == "TYPE"):
                self.call_type(self.__xml_code_root[i])

            elif (self.__xml_code_root[i].attrib['opcode'].upper() == "LABEL"):
                pass

            elif (self.__xml_code_root[i].attrib['opcode'].upper() == "JUMP"):
                i = self.call_jump(self.__xml_code_root[i])
                continue

            elif (self.__xml_code_root[i].attrib['opcode'].upper() == "JUMPIFEQ"):
                i = self.call_jumpifeq(self.__xml_code_root[i], i)
                continue

            elif (self.__xml_code_root[i].attrib['opcode'].upper() == "JUMPIFNEQ"):
                i = self.call_jumpifneq(self.__xml_code_root[i], i)
                continue

            elif (self.__xml_code_root[i].attrib['opcode'].upper() == "EXIT"):
                self.call_exit(self.__xml_code_root[i])

            elif (self.__xml_code_root[i].attrib['opcode'].upper() == "DPRINT"):
                self.call_dprint(self.__xml_code_root[i])

            elif (self.__xml_code_root[i].attrib['opcode'].upper() == "BREAK"):
                self.call_break(self.__xml_code_root[i])

            else:
                int_lib.err.error_handler(int_lib.err.BAD_XML_STRUCTURE)
            i = i + 1

    def call_move(self, instruction):
        self.check_arg_count(instruction, 2)
        self.check_types(instruction, '^var$', '^(string|var|nil|int|bool)$')

        # get value and type of <symb>, source argument
        if (instruction[1].attrib['type'] == "var"):
            src_var_value = self.get_var_value(instruction[1])
            src_var_type = self.get_var_type(instruction[1])
        else:
            src_var_value = instruction[1].text
            src_var_type = instruction[1].attrib['type']

        if (src_var_type == ""):
            int_lib.err.error_handler(int_lib.err.MISSING_VALUE)

        # check if var exists
        if (self.exists(instruction[0]) == None):
            int_lib.err.error_handler(int_lib.err.NOT_EXISTING_FRAME)
        elif (self.exists(instruction[0]) is False):
            int_lib.err.error_handler(int_lib.err.NOT_EXISTING_VARIABLE)


        # load value into right var in right frame
        frame = self.get_frame(instruction[0].text)
        if (frame == 0):  # global frame
            self.__global_frame.actualize([src_var_type, src_var_value], instruction[0].text[3:])
        elif (frame == 1):  # local frame
            self.__frame_stack.top().actualize([src_var_type, src_var_value], instruction[0].text[3:])
        else:  # temp frame
            self.__temp_frame.actualize([src_var_type, src_var_value], instruction[0].text[3:])

    def call_createframe(self, instruction):
        self.check_arg_count(instruction, 0)
        if (self.__temp_frame == None):
            self.__temp_frame = int_lib.hash_table.hash_table()
        else:
            self.__temp_frame.clear()

    def call_pushframe(self, instruction):
        self.check_arg_count(instruction, 0)
        if (self.__temp_frame == None):
            int_lib.err.error_handler(int_lib.err.NOT_EXISTING_FRAME)
        self.__frame_stack.push(self.__temp_frame)
        self.__temp_frame = None

    def call_popframe(self, instruction):
        self.check_arg_count(instruction, 0)
        if (self.__frame_stack.is_empty() == True):
            int_lib.err.error_handler(int_lib.err.NOT_EXISTING_FRAME)
        self.__temp_frame = self.__frame_stack.top()
        self.__frame_stack.pop()

    def call_defvar(self, instruction):
        self.check_arg_count(instruction, 1)
        self.check_types(instruction, '^var$')
        frame = self.get_frame(instruction[0].text)
        if (frame == 0):  # global frame
            if (self.__global_frame.search(instruction[0].text[3:])):
                int_lib.err.error_handler(int_lib.err.SEMANTICS_ERROR)
            self.__global_frame.insert(["", ""], instruction[0].text[3:])
        elif (frame == 1):  # local frame
            # check if frame exists
            if (not self.check_frame(check_lf=True)):
                int_lib.err.error_handler(int_lib.err.NOT_EXISTING_FRAME)
            # check if var not exists
            if (self.__frame_stack.top().search(instruction[0].text[3:])):
                int_lib.err.error_handler(int_lib.err.SEMANTICS_ERROR)
            self.__frame_stack.top().insert(["", ""], instruction[0].text[3:])
        else:  # temp frame
            # check if frame exists
            if (not self.check_frame(check_tf=True)):
                int_lib.err.error_handler(int_lib.err.NOT_EXISTING_FRAME)
            # check if var not exists
            if (self.__temp_frame.search(instruction[0].text[3:])):
                int_lib.err.error_handler(int_lib.err.SEMANTICS_ERROR)
            self.__temp_frame.insert(["", ""], instruction[0].text[3:])

    def call_call(self, instruction, index):
        self.check_arg_count(instruction, 1)
        self.check_types(instruction, '^label$')
        if (not self.__labels.search(instruction[0].text)):
            int_lib.err.error_handler(int_lib.err.SEMANTICS_ERROR)
        self.__call_stack.push(index + 1)
        return self.__labels.read(instruction[0].text)

    def call_return(self, instruction):
        self.check_arg_count(instruction, 0)
        if (self.__call_stack.is_empty()):
            int_lib.err.error_handler(int_lib.err.MISSING_VALUE)
        ret_index = self.__call_stack.top()
        self.__call_stack.pop()
        return ret_index

    def call_pushs(self, instruction):
        self.check_arg_count(instruction, 1)
        self.check_types(instruction, '^(string|var|nil|int|bool)$')
        # push argument of instruction to data stack
        if (instruction[0].attrib['type'] == "var"):
            var_value = self.get_var_value(instruction[0])
            if (self.get_var_type(instruction[0]) == ""):
                    int_lib.err.error_handler(int_lib.err.MISSING_VALUE)

            self.__data_stack.push([instruction[0].attrib['type'], var_value])
        else:
            self.__data_stack.push([instruction[0].attrib['type'], instruction[0].text])

    def call_pops(self, instruction):
        self.check_arg_count(instruction, 1)
        self.check_types(instruction, '^var$')
        if (self.__data_stack.is_empty()):
            int_lib.err.error_handler(int_lib.err.MISSING_VALUE)
        data = self.__data_stack.top()
        self.__data_stack.pop()

        # check if var exists
        if (self.exists(instruction[0]) == None):
            int_lib.err.error_handler(int_lib.err.NOT_EXISTING_FRAME)
        elif (self.exists(instruction[0]) is False):
            int_lib.err.error_handler(int_lib.err.NOT_EXISTING_VARIABLE)

        # load value into right var in right frame
        frame = self.get_frame(instruction[0].text)
        if (frame == 0):  # global frame
            self.__global_frame.actualize(data, instruction[0].text[3:])
        elif (frame == 1):  # local frame
            self.__frame_stack.top().actualize(data, instruction[0].text[3:])
        else:  # temp frame
            self.__temp_frame.actualize(data, instruction[0].text[3:])

    def call_add(self, instruction):
        self.check_arg_count(instruction, 3)
        self.check_types(instruction, '^var$', '^(var|int)$', '^(var|int)$')

        # check if var exists
        if (self.exists(instruction[0]) == None):
            int_lib.err.error_handler(int_lib.err.NOT_EXISTING_FRAME)
        elif (self.exists(instruction[0]) is False):
            int_lib.err.error_handler(int_lib.err.NOT_EXISTING_VARIABLE)

        if (instruction[1].attrib['type'] == "var"):
            num_1 = self.get_var_value(instruction[1])
        else:
            num_1 = instruction[1].text

        if (instruction[2].attrib['type'] == "var"):
            num_2 = self.get_var_value(instruction[2])
        else:
            num_2 = instruction[2].text

        if (num_1 == "" or num_2 == ""):
            int_lib.err.error_handler(int_lib.err.MISSING_VALUE)

        if (not re.match(r'^[-+]?[0-9]+$', num_1)):
            int_lib.err.error_handler(int_lib.err.SEMANTICS_ERROR)

        if (not re.match(r'^[-+]?[0-9]+$', num_2)):
            int_lib.err.error_handler(int_lib.err.SEMANTICS_ERROR)

        frame = self.get_frame(instruction[0].text)
        if (frame == 0):
            self.__global_frame.actualize(["int", str(int(num_1) + int(num_2))], instruction[0].text[3:])
        elif (frame == 1):
            self.__frame_stack.top().actualize(["int", str(int(num_1) + int(num_2))], instruction[0].text[3:])
        else:
            self.__temp_frame.actualize(["int", str(int(num_1) + int(num_2))], instruction[0].text[3:])

    def call_sub(self, instruction):
        self.check_arg_count(instruction, 3)
        self.check_types(instruction, '^var$', '^(var|int)$', '^(var|int)$')

        # check if var exists
        if (self.exists(instruction[0]) == None):
            int_lib.err.error_handler(int_lib.err.NOT_EXISTING_FRAME)
        elif (self.exists(instruction[0]) is False):
            int_lib.err.error_handler(int_lib.err.NOT_EXISTING_VARIABLE)

        if (instruction[1].attrib['type'] == "var"):
            num_1 = self.get_var_value(instruction[1])
        else:
            num_1 = instruction[1].text

        if (instruction[2].attrib['type'] == "var"):
            num_2 = self.get_var_value(instruction[2])
        else:
            num_2 = instruction[2].text

        if (num_1 == "" or num_2 == ""):
            int_lib.err.error_handler(int_lib.err.MISSING_VALUE)

        if (not re.match(r'^[-+]?[0-9]+$', num_1)):
            int_lib.err.error_handler(int_lib.err.SEMANTICS_ERROR)

        if (not re.match(r'^[-+]?[0-9]+$', num_2)):
            int_lib.err.error_handler(int_lib.err.SEMANTICS_ERROR)

        frame = self.get_frame(instruction[0].text)
        if (frame == 0):
            self.__global_frame.actualize(["int", str(int(num_1) - int(num_2))], instruction[0].text[3:])
        elif (frame == 1):
            self.__frame_stack.top().actualize(["int", str(int(num_1) - int(num_2))], instruction[0].text[3:])
        else:
            self.__temp_frame.actualize(["int", str(int(num_1) - int(num_2))], instruction[0].text[3:])

    def call_mul(self, instruction):
        self.check_arg_count(instruction, 3)
        self.check_types(instruction, '^var$', '^(var|int)$', '^(var|int)$')

        # check if var exists
        if (self.exists(instruction[0]) == None):
            int_lib.err.error_handler(int_lib.err.NOT_EXISTING_FRAME)
        elif (self.exists(instruction[0]) is False):
            int_lib.err.error_handler(int_lib.err.NOT_EXISTING_VARIABLE)

        if (instruction[1].attrib['type'] == "var"):
            num_1 = self.get_var_value(instruction[1])
        else:
            num_1 = instruction[1].text

        if (instruction[2].attrib['type'] == "var"):
            num_2 = self.get_var_value(instruction[2])
        else:
            num_2 = instruction[2].text

        if (num_1 == "" or num_2 == ""):
            int_lib.err.error_handler(int_lib.err.MISSING_VALUE)

        if (not re.match(r'^[-+]?[0-9]+$', num_1)):
            int_lib.err.error_handler(int_lib.err.SEMANTICS_ERROR)

        if (not re.match(r'^[-+]?[0-9]+$', num_2)):
            int_lib.err.error_handler(int_lib.err.SEMANTICS_ERROR)

        frame = self.get_frame(instruction[0].text)
        if (frame == 0):
            self.__global_frame.actualize(["int", str(int(num_1) * int(num_2))], instruction[0].text[3:])
        elif (frame == 1):
            self.__frame_stack.top().actualize(["int", str(int(num_1) * int(num_2))], instruction[0].text[3:])
        else:
            self.__temp_frame.actualize(["int", str(int(num_1) * int(num_2))], instruction[0].text[3:])

    def call_idiv(self, instruction):
        self.check_arg_count(instruction, 3)
        self.check_types(instruction, '^var$', '^(var|int)$', '^(var|int)$')

        # check if var exists
        if (self.exists(instruction[0]) == None):
            int_lib.err.error_handler(int_lib.err.NOT_EXISTING_FRAME)
        elif (self.exists(instruction[0]) is False):
            int_lib.err.error_handler(int_lib.err.NOT_EXISTING_VARIABLE)

        if (instruction[1].attrib['type'] == "var"):
            num_1 = self.get_var_value(instruction[1])
        else:
            num_1 = instruction[1].text

        if (instruction[2].attrib['type'] == "var"):
            num_2 = self.get_var_value(instruction[2])
        else:
            num_2 = instruction[2].text

        if (num_1 == "" or num_2 == ""):
            int_lib.err.error_handler(int_lib.err.MISSING_VALUE)

        if (int(num_2) == 0):
            int_lib.err.error_handler(int_lib.err.BAD_VALUE)

        if (not re.match(r'^[-+]?[0-9]+$', num_1)):
            int_lib.err.error_handler(int_lib.err.SEMANTICS_ERROR)

        if (not re.match(r'^[-+]?[0-9]+$', num_2)):
            int_lib.err.error_handler(int_lib.err.SEMANTICS_ERROR)

        frame = self.get_frame(instruction[0].text)
        if (frame == 0):
            self.__global_frame.actualize(["int", str(int(num_1) // int(num_2))], instruction[0].text[3:])
        elif (frame == 1):
            self.__frame_stack.top().actualize(["int", str(int(num_1) // int(num_2))], instruction[0].text[3:])
        else:
            self.__temp_frame.actualize(["int", str(int(num_1) // int(num_2))], instruction[0].text[3:])

    def call_lt(self, instruction):
        self.check_arg_count(instruction, 3)
        self.check_types(instruction, '^var$', '^(string|var|int|bool)$', '^(string|var|int|bool)$')

        # check if var exists
        if (self.exists(instruction[0]) == None):
            int_lib.err.error_handler(int_lib.err.NOT_EXISTING_FRAME)
        elif (self.exists(instruction[0]) is False):
            int_lib.err.error_handler(int_lib.err.NOT_EXISTING_VARIABLE)

        if (instruction[1].attrib['type'] == "var"):
            elem_1_value = self.get_var_value(instruction[1])
            elem_1_type = self.get_var_type(instruction[1])
        else:
            elem_1_value = instruction[1].text
            elem_1_type = instruction[1].attrib['type']

        if (instruction[2].attrib['type'] == "var"):
            elem_2_value = self.get_var_value(instruction[2])
            elem_2_type = self.get_var_type(instruction[2])
        else:
            elem_2_value = instruction[2].text
            elem_2_type = instruction[2].attrib['type']

        if (elem_1_value == "" or elem_2_value == ""):
            int_lib.err.error_handler(int_lib.err.MISSING_VALUE)

        if (elem_1_type != elem_2_type):
            int_lib.err.error_handler(int_lib.err.BAD_OPERAND_TYPES)

        result = None
        if (elem_1_type == "int"):
            if (int(elem_1_value) < int(elem_2_value)):
                result = "True"
            else:
                result = "False"
        elif (elem_1_type == "bool"):
            if (elem_1_value.upper() == "FALSE" and elem_2_value.upper() == "TRUE"):
                result = "True"
            else:
                result = "False"
        elif (elem_1_type == "string"):
            if (str(elem_1_value) < str(elem_2_value)):
                result = "True"
            else:
                result = "False"

        frame = self.get_frame(instruction[0].text)
        if (frame == 0):
            self.__global_frame.actualize(["bool", result], instruction[0].text[3:])
        elif (frame == 1):
            self.__frame_stack.top().actualize(["bool", result], instruction[0].text[3:])
        else:
            self.__temp_frame.actualize(["bool", result], instruction[0].text[3:])

    def call_gt(self, instruction):
        self.check_arg_count(instruction, 3)
        self.check_types(instruction, '^var$', '^(string|var|int|bool)$', '^(string|var|int|bool)$')

        # check if var exists
        if (self.exists(instruction[0]) == None):
            int_lib.err.error_handler(int_lib.err.NOT_EXISTING_FRAME)
        elif (self.exists(instruction[0]) is False):
            int_lib.err.error_handler(int_lib.err.NOT_EXISTING_VARIABLE)

        if (instruction[1].attrib['type'] == "var"):
            elem_1_value = self.get_var_value(instruction[1])
            elem_1_type = self.get_var_type(instruction[1])
        else:
            elem_1_value = instruction[1].text
            elem_1_type = instruction[1].attrib['type']

        if (instruction[2].attrib['type'] == "var"):
            elem_2_value = self.get_var_value(instruction[2])
            elem_2_type = self.get_var_type(instruction[2])
        else:
            elem_2_value = instruction[2].text
            elem_2_type = instruction[2].attrib['type']

        if (elem_1_value == "" or elem_2_value == ""):
            int_lib.err.error_handler(int_lib.err.MISSING_VALUE)

        if (elem_1_type != elem_2_type):
            int_lib.err.error_handler(int_lib.err.BAD_OPERAND_TYPES)

        result = None
        if (elem_1_type == "int"):
            if (int(elem_1_value) > int(elem_2_value)):
                result = "True"
            else:
                result = "False"
        elif (elem_1_type == "bool"):
            if (elem_1_value.upper() == "TRUE" and elem_2_value.upper() == "FALSE"):
                result = "True"
            else:
                result = "False"
        elif (elem_1_type == "string"):
            if (str(elem_1_value) > str(elem_2_value)):
                result = "True"
            else:
                result = "False"

        frame = self.get_frame(instruction[0].text)
        if (frame == 0):
            self.__global_frame.actualize(["bool", result], instruction[0].text[3:])
        elif (frame == 1):
            self.__frame_stack.top().actualize(["bool", result], instruction[0].text[3:])
        else:
            self.__temp_frame.actualize(["bool", result], instruction[0].text[3:])

    def call_eq(self, instruction):
        self.check_arg_count(instruction, 3)
        self.check_types(instruction, '^var$', '^(string|var|nil|int|bool)$', '^(string|var|nil|int|bool)$')

        # check if var exists
        if (self.exists(instruction[0]) == None):
            int_lib.err.error_handler(int_lib.err.NOT_EXISTING_FRAME)
        elif (self.exists(instruction[0]) is False):
            int_lib.err.error_handler(int_lib.err.NOT_EXISTING_VARIABLE)

        if (instruction[1].attrib['type'] == "var"):
            elem_1_value = self.get_var_value(instruction[1])
            elem_1_type = self.get_var_type(instruction[1])
        else:
            elem_1_value = instruction[1].text
            elem_1_type = instruction[1].attrib['type']

        if (instruction[2].attrib['type'] == "var"):
            elem_2_value = self.get_var_value(instruction[2])
            elem_2_type = self.get_var_type(instruction[2])
        else:
            elem_2_value = instruction[2].text
            elem_2_type = instruction[2].attrib['type']

        if (elem_1_value == "" or elem_2_value == ""):
            int_lib.err.error_handler(int_lib.err.MISSING_VALUE)

        if (elem_1_type != elem_2_type and elem_1_type != "nil" and elem_2_type != "nil"):
            int_lib.err.error_handler(int_lib.err.BAD_OPERAND_TYPES)

        result = None
        if (elem_1_type == "int"):
            if (elem_2_value == "nil"):
                result = "False"
            elif (int(elem_1_value) == int(elem_2_value)):
                result = "True"
            else:
                result = "False"
        elif (elem_1_type == "bool"):
            if (elem_2_value == "nil"):
                result = "False"
            elif ((elem_1_value.upper() == "FALSE" and elem_2_value.upper() == "FALSE") or (elem_1_value.upper() == "TRUE" and elem_2_value.upper() == "TRUE")):
                result = "True"
            else:
                result = "False"
        elif (elem_1_type == "string" or elem_1_type == "nil"):
            if (str(elem_1_value) == str(elem_2_value)):
                result = "True"
            else:
                result = "False"

        frame = self.get_frame(instruction[0].text)
        if (frame == 0):
            self.__global_frame.actualize(["bool", result], instruction[0].text[3:])
        elif (frame == 1):
            self.__frame_stack.top().actualize(["bool", result], instruction[0].text[3:])
        else:
            self.__temp_frame.actualize(["bool", result], instruction[0].text[3:])

    def call_and(self, instruction):
        self.check_arg_count(instruction, 3)
        self.check_types(instruction, '^var$', '^(var|bool)$', '(var|bool)$')

        # check if var exists
        if (self.exists(instruction[0]) == None):
            int_lib.err.error_handler(int_lib.err.NOT_EXISTING_FRAME)
        elif (self.exists(instruction[0]) is False):
            int_lib.err.error_handler(int_lib.err.NOT_EXISTING_VARIABLE)

        if (instruction[1].attrib['type'] == "var"):
            elem_1_value = self.get_var_value(instruction[1])
            elem_1_type = self.get_var_type(instruction[1])
        else:
            elem_1_value = instruction[1].text
            elem_1_type = instruction[1].attrib['type']

        if (instruction[2].attrib['type'] == "var"):
            elem_2_value = self.get_var_value(instruction[2])
            elem_2_type = self.get_var_type(instruction[2])
        else:
            elem_2_value = instruction[2].text
            elem_2_type = instruction[2].attrib['type']

        if (elem_1_value == "" or elem_2_value == ""):
            int_lib.err.error_handler(int_lib.err.MISSING_VALUE)

        if (elem_1_type != "bool" or elem_2_type != "bool"):
            int_lib.err.error_handler(int_lib.err.BAD_OPERAND_TYPES)

        if (elem_1_value.upper() == "TRUE" and elem_2_value.upper() == "TRUE"):
            result = "True"
        else:
            result = "False"

        frame = self.get_frame(instruction[0].text)
        if (frame == 0):
            self.__global_frame.actualize(["bool", result], instruction[0].text[3:])
        elif (frame == 1):
            self.__frame_stack.top().actualize(["bool", result], instruction[0].text[3:])
        else:
            self.__temp_frame.actualize(["bool", result], instruction[0].text[3:])

    def call_or(self, instruction):
        self.check_arg_count(instruction, 3)
        self.check_types(instruction, '^var$', '^(var|bool)$', '(var|bool)$')

        # check if var exists
        if (self.exists(instruction[0]) == None):
            int_lib.err.error_handler(int_lib.err.NOT_EXISTING_FRAME)
        elif (self.exists(instruction[0]) is False):
            int_lib.err.error_handler(int_lib.err.NOT_EXISTING_VARIABLE)

        if (instruction[1].attrib['type'] == "var"):
            elem_1_value = self.get_var_value(instruction[1])
            elem_1_type = self.get_var_type(instruction[1])
        else:
            elem_1_value = instruction[1].text
            elem_1_type = instruction[1].attrib['type']

        if (instruction[2].attrib['type'] == "var"):
            elem_2_value = self.get_var_value(instruction[2])
            elem_2_type = self.get_var_type(instruction[2])
        else:
            elem_2_value = instruction[2].text
            elem_2_type = instruction[2].attrib['type']

        if (elem_1_value == "" or elem_2_value == ""):
            int_lib.err.error_handler(int_lib.err.MISSING_VALUE)

        if (elem_1_type != "bool" or elem_2_type != "bool"):
            int_lib.err.error_handler(int_lib.err.BAD_OPERAND_TYPES)

        if (elem_1_value.upper() == "TRUE" or elem_2_value.upper() == "TRUE"):
            result = "True"
        else:
            result = "False"

        frame = self.get_frame(instruction[0].text)
        if (frame == 0):
            self.__global_frame.actualize(["bool", result], instruction[0].text[3:])
        elif (frame == 1):
            self.__frame_stack.top().actualize(["bool", result], instruction[0].text[3:])
        else:
            self.__temp_frame.actualize(["bool", result], instruction[0].text[3:])

    def call_not(self, instruction):
        self.check_arg_count(instruction, 2)
        self.check_types(instruction, '^var$', '^(bool|var)$')

        # check if var exists
        if (self.exists(instruction[0]) == None):
            int_lib.err.error_handler(int_lib.err.NOT_EXISTING_FRAME)
        elif (self.exists(instruction[0]) is False):
            int_lib.err.error_handler(int_lib.err.NOT_EXISTING_VARIABLE)

        if (instruction[1].attrib['type'] == "var"):
            elem_1_value = self.get_var_value(instruction[1])
            elem_1_type = self.get_var_type(instruction[1])
        else:
            elem_1_value = instruction[1].text
            elem_1_type = instruction[1].attrib['type']

        if (elem_1_value == ""):
            int_lib.err.error_handler(int_lib.err.MISSING_VALUE)

        if (elem_1_type != "bool"):
            int_lib.err.error_handler(int_lib.err.BAD_OPERAND_TYPES)

        if (elem_1_value.upper() == "FALSE"):
            result = "True"
        else:
            result = "False"

        frame = self.get_frame(instruction[0].text)
        if (frame == 0):
            self.__global_frame.actualize(["bool", result], instruction[0].text[3:])
        elif (frame == 1):
            self.__frame_stack.top().actualize(["bool", result], instruction[0].text[3:])
        else:
            self.__temp_frame.actualize(["bool", result], instruction[0].text[3:])

    def call_int2char(self, instruction):
        self.check_arg_count(instruction, 2)
        self.check_types(instruction, '^var$', '^(var|int)$')

        # check if var exists
        if (self.exists(instruction[0]) == None):
            int_lib.err.error_handler(int_lib.err.NOT_EXISTING_FRAME)
        elif (self.exists(instruction[0]) is False):
            int_lib.err.error_handler(int_lib.err.NOT_EXISTING_VARIABLE)

        if (instruction[1].attrib['type'] == "var"):
            if (self.get_var_type(instruction[1]) == ""):
                int_lib.err.error_handler(int_lib.err.MISSING_VALUE)
            if (self.get_var_type(instruction[1]) != "int"):
                int_lib.err.error_handler(int_lib.err.BAD_OPERAND_TYPES)
            src_value = self.get_var_value(instruction[1])
        else:
            if (not re.match(r'[-+]?[0-9]+', instruction[1].text)):
                int_lib.err.error_handler(int_lib.err.SEMANTICS_ERROR)
            src_value = instruction[1].text

        character = ""
        try:
            character = chr(int(src_value))
        except ValueError:
            int_lib.err.error_handler(int_lib.err.STRING_ERROR)

        # load value into right var in right frame
        frame = self.get_frame(instruction[0].text)
        if (frame == 0):  # global frame
            self.__global_frame.actualize(["string", character], instruction[0].text[3:])
        elif (frame == 1):  # local frame
            self.__frame_stack.top().actualize(["string", character], instruction[0].text[3:])
        else:  # temp frame
            self.__temp_frame.actualize(["string", character], instruction[0].text[3:])

    def call_stri2int(self, instruction):
        self.check_arg_count(instruction, 3)
        self.check_types(instruction, '^var$', '^(var|string)$', '^(var|int)$')

        # check if var exists
        if (self.exists(instruction[0]) == None):
            int_lib.err.error_handler(int_lib.err.NOT_EXISTING_FRAME)
        elif (self.exists(instruction[0]) is False):
            int_lib.err.error_handler(int_lib.err.NOT_EXISTING_VARIABLE)

        if (instruction[1].attrib['type'] == "var"):
            if (self.get_var_type(instruction[1]) == ""):
                int_lib.err.error_handler(int_lib.err.MISSING_VALUE)
            if (self.get_var_type(instruction[1]) != "string"):
                int_lib.err.error_handler(int_lib.err.BAD_OPERAND_TYPES)
            src_string = self.get_var_value(instruction[1])
        else:
            src_string = instruction[1].text

        if (instruction[2].attrib['type'] == "var"):
            if (self.get_var_type(instruction[2]) == ""):
                int_lib.err.error_handler(int_lib.err.MISSING_VALUE)
            if (self.get_var_type(instruction[2]) != "int"):
                int_lib.err.error_handler(int_lib.err.BAD_OPERAND_TYPES)
            src_index = self.get_var_value(instruction[2])
        else:
            src_index = instruction[2].text

        if (int(src_index) < 0 or int(src_index) >= len(src_string)):
            int_lib.err.error_handler(int_lib.err.STRING_ERROR)

        num = ""
        try:
            num = ord(str(src_string[int(src_index)]))
        except ValueError:
            int_lib.err.error_handler(int_lib.err.STRING_ERROR)

        # load value into right var in right frame
        frame = self.get_frame(instruction[0].text)
        if (frame == 0):  # global frame
            self.__global_frame.actualize(["int", num], instruction[0].text[3:])
        elif (frame == 1):  # local frame
            self.__frame_stack.top().actualize(["int", num], instruction[0].text[3:])
        else:  # temp frame
            self.__temp_frame.actualize(["int", num], instruction[0].text[3:])

    def call_read(self, instruction):
        self.check_arg_count(instruction, 2)
        self.check_types(instruction, '^var$', '^type$')

        # check if var exists
        if (self.exists(instruction[0]) == None):
            int_lib.err.error_handler(int_lib.err.NOT_EXISTING_FRAME)
        elif (self.exists(instruction[0]) is False):
            int_lib.err.error_handler(int_lib.err.NOT_EXISTING_VARIABLE)


        if (self.__input == None):
            input_line = input()
        else:
            try:
                input_line = self.__input[self.__input_line_index]
                if (input_line == None):
                    input_line = ""
                self.__input_line_index = self.__input_line_index + 1
            except EOFError and IndexError:
                input_line = None


        load_type = "nil"
        result = "nil"
        if (instruction[1].text == "bool"):
            load_type = "bool"
            if (input_line == None):
                load_type = "nil"
            elif (input_line.upper() == "TRUE"):
                result = "True"
            else:
                result = "False"
        elif (instruction[1].text == "int"):
            load_type = "int"
            if (re.match(r'^[-+]?[0-9]+$', input_line)):
                result = input_line
            else:
                load_type = "nil"
        elif (instruction[1].text == "string"):
            load_type = "string"
            if (input_line == None):
                load_type = "nil"
            else:
                result = input_line
        else:
            int_lib.err.error_handler(int_lib.err.SEMANTICS_ERROR)

        # load value into right var in right frame
        frame = self.get_frame(instruction[0].text)
        if (frame == 0):  # global frame
            self.__global_frame.actualize([load_type, result], instruction[0].text[3:])
        elif (frame == 1):  # local frame
            self.__frame_stack.top().actualize([load_type, result], instruction[0].text[3:])
        else:  # temp frame
            self.__temp_frame.actualize([load_type, result], instruction[0].text[3:])

    def call_write(self, instruction):
        self.check_arg_count(instruction, 1)
        self.check_types(instruction, '^(string|var|nil|int|bool)$')
        if (instruction[0].attrib['type'] == "nil"):
            print("", end='')
        elif (instruction[0].attrib['type'] == "bool"):
            if (instruction[0].text.upper() == "TRUE"):
                print("true", end='')
            else:
                print("false", end='')
        elif (instruction[0].attrib['type'] == "var"):
            value = self.get_var_value(instruction[0])
            type = self.get_var_type(instruction[0])
            if (type == "nil"):
                print("", end='')
            elif (type == "bool"):
                if (value.upper() == "TRUE"):
                    print("true", end='')
                else:
                    print("false", end='')
            elif (type == ""):
                int_lib.err.error_handler(int_lib.err.MISSING_VALUE)
            else:
                print(value, end='')
        else:
            print(instruction[0].text, end='')

    def call_concat(self, instruction):
        self.check_arg_count(instruction, 3)
        self.check_types(instruction, '^var$', '^(var|string)$', '^(var|string)$')

        # check if var exists
        if (self.exists(instruction[0]) == None):
            int_lib.err.error_handler(int_lib.err.NOT_EXISTING_FRAME)
        elif (self.exists(instruction[0]) is False):
            int_lib.err.error_handler(int_lib.err.NOT_EXISTING_VARIABLE)

        value_1 = ""
        value_2 = ""
        if (instruction[1].attrib['type'] == "var"):
            if (self.get_var_type(instruction[1]) == ""):
                int_lib.err.error_handler(int_lib.err.MISSING_VALUE)
            if (self.get_var_type(instruction[1]) != "string"):
                int_lib.err.error_handler(int_lib.err.BAD_OPERAND_TYPES)
            else:
                value_1 = self.get_var_value(instruction[1].text)
        else:
            value_1 = instruction[1].text

        if (instruction[2].attrib['type'] == "var"):
            if (self.get_var_type(instruction[2]) == ""):
                int_lib.err.error_handler(int_lib.err.MISSING_VALUE)
            if (self.get_var_type(instruction[2]) != "string"):
                int_lib.err.error_handler(int_lib.err.BAD_OPERAND_TYPES)
            else:
                value_2 = self.get_var_value(instruction[2].text)
        else:
            value_2 = instruction[2].text

        if (value_1 == None):
            value_1 = ""
        if (value_2 == None):
            value_2 = ""

        # load value into right var in right frame
        frame = self.get_frame(instruction[0].text)
        if (frame == 0):  # global frame
            self.__global_frame.actualize(["string", value_1 + value_2], instruction[0].text[3:])
        elif (frame == 1):  # local frame
            self.__frame_stack.top().actualize(["string", value_1 + value_2], instruction[0].text[3:])
        else:  # temp frame
            self.__temp_frame.actualize(["string", value_1 + value_2], instruction[0].text[3:])

    def call_strlen(self, instruction):
        self.check_arg_count(instruction, 2)
        self.check_types(instruction, '^var$', '^(string|var)$')

        # check if var exists
        if (self.exists(instruction[0]) == None):
            int_lib.err.error_handler(int_lib.err.NOT_EXISTING_FRAME)
        elif (self.exists(instruction[0]) is False):
            int_lib.err.error_handler(int_lib.err.NOT_EXISTING_VARIABLE)

        if (instruction[1].attrib['type'] == "var"):
            if (self.get_var_type(instruction[1]) == ""):
                int_lib.err.error_handler(int_lib.err.MISSING_VALUE)
            if (self.get_var_type(instruction[1]) != "string"):
                int_lib.err.error_handler(int_lib.err.BAD_OPERAND_TYPES)
            src_string = self.get_var_value(instruction[1])
        else:
            src_string = instruction[1].text
        if (src_string == None):
            src_string = ""

        frame = self.get_frame(instruction[0].text)
        if (frame == 0):
            self.__global_frame.actualize(["int", str(len(src_string))], instruction[0].text[3:])
        elif (frame == 1):
            self.__frame_stack.top().actualize(["int", str(len(src_string))], instruction[0].text[3:])
        else:
            self.__temp_frame.actualize(["int", str(len(src_string))], instruction[0].text[3:])

    def call_getchar(self, instruction):
        self.check_arg_count(instruction, 3)
        self.check_types(instruction, '^var$', '^(string|var)$', '^(var|int)$')

        # check if var exists
        if (self.exists(instruction[0]) == None):
            int_lib.err.error_handler(int_lib.err.NOT_EXISTING_FRAME)
        elif (self.exists(instruction[0]) is False):
            int_lib.err.error_handler(int_lib.err.NOT_EXISTING_VARIABLE)

        if (instruction[1].attrib['type'] == "var"):
            if (self.get_var_type(instruction[1]) == ""):
                int_lib.err.error_handler(int_lib.err.MISSING_VALUE)
            if (self.get_var_type(instruction[1]) != "string"):
                int_lib.err.error_handler(int_lib.err.BAD_OPERAND_TYPES)
            src_string = self.get_var_value(instruction[1])
        else:
            src_string = instruction[1].text

        if (instruction[2].attrib['type'] == "var"):
            if (self.get_var_type(instruction[2]) == ""):
                int_lib.err.error_handler(int_lib.err.MISSING_VALUE)
            if (self.get_var_type(instruction[2]) != "int"):
                int_lib.err.error_handler(int_lib.err.BAD_OPERAND_TYPES)
            src_index = self.get_var_value(instruction[2])
        else:
            src_index = instruction[2].text

        if (int(src_index) < 0 or int(src_index) >= len(src_string)):
            int_lib.err.error_handler(int_lib.err.STRING_ERROR)

        # load value into right var in right frame
        frame = self.get_frame(instruction[0].text)
        if (frame == 0):  # global frame
            self.__global_frame.actualize(["string", src_string[int(src_index)]], instruction[0].text[3:])
        elif (frame == 1):  # local frame
            self.__frame_stack.top().actualize(["string", src_string[int(src_index)]], instruction[0].text[3:])
        else:  # temp frame
            self.__temp_frame.actualize(["string", src_string[int(src_index)]], instruction[0].text[3:])

    def call_setchar(self, instruction):
        self.check_arg_count(instruction, 3)
        self.check_types(instruction, '^var$', '^(var|int)$', '^(string|var)$')

        # check if var exists and get value
        if (self.exists(instruction[0]) == None):
            int_lib.err.error_handler(int_lib.err.NOT_EXISTING_FRAME)
        elif (self.exists(instruction[0]) is False):
            int_lib.err.error_handler(int_lib.err.NOT_EXISTING_VARIABLE)
        dest_var_string = self.get_var_value(instruction[0])

        if (self.get_var_type(instruction[0]) == ""):
            int_lib.err.error_handler(int_lib.err.MISSING_VALUE)
        if (self.get_var_type(instruction[0]) != "string"):
            int_lib.err.error_handler(int_lib.err.BAD_OPERAND_TYPES)


        if (instruction[1].attrib['type'] == "var"):
            if (self.get_var_type(instruction[1]) == ""):
                int_lib.err.error_handler(int_lib.err.MISSING_VALUE)
            if (self.get_var_type(instruction[1]) != "int"):
                int_lib.err.error_handler(int_lib.err.BAD_OPERAND_TYPES)
            src_index = self.get_var_value(instruction[1])
        else:
            src_index = instruction[1].text

        if (instruction[2].attrib['type'] == "var"):
            if (self.get_var_type(instruction[2]) == ""):
                int_lib.err.error_handler(int_lib.err.MISSING_VALUE)
            if (self.get_var_type(instruction[2]) != "string"):
                int_lib.err.error_handler(int_lib.err.BAD_OPERAND_TYPES)
            src_string = self.get_var_value(instruction[2])
        else:
            src_string = instruction[2].text
        if (src_string == None):
            src_string = ""

        if (len(src_string) <= 0):
            int_lib.err.error_handler(int_lib.err.STRING_ERROR)

        if (int(src_index) < 0 or int(src_index) >= len(dest_var_string)):
            int_lib.err.error_handler(int_lib.err.STRING_ERROR)

        dest_var_string = list(dest_var_string)
        dest_var_string[int(src_index)] = src_string[0]
        dest_var_string = ''.join(dest_var_string)

        # load value into right var in right frame
        frame = self.get_frame(instruction[0].text)
        if (frame == 0):  # global frame
            self.__global_frame.actualize(["string", dest_var_string], instruction[0].text[3:])
        elif (frame == 1):  # local frame
            self.__frame_stack.top().actualize(["string", dest_var_string], instruction[0].text[3:])
        else:  # temp frame
            self.__temp_frame.actualize(["string", dest_var_string], instruction[0].text[3:])

    def call_type(self, instruction):
        self.check_arg_count(instruction, 2)
        self.check_types(instruction, '^var$', '^(string|var|nil|int|bool)$')

        # check if var exists
        if (self.exists(instruction[0]) == None):
            int_lib.err.error_handler(int_lib.err.NOT_EXISTING_FRAME)
        elif (self.exists(instruction[0]) is False):
            int_lib.err.error_handler(int_lib.err.NOT_EXISTING_VARIABLE)

        if (instruction[1].attrib['type'] == "var"):
            type = self.get_var_type(instruction[1])
        else:
            type = instruction[1].attrib['type']


        frame = self.get_frame(instruction[0].text)
        if (frame == 0):
            self.__global_frame.actualize(["string", str(type)], instruction[0].text[3:])
        elif (frame == 1):
            self.__frame_stack.top().actualize(["string", str(type)], instruction[0].text[3:])
        else:
            self.__temp_frame.actualize(["string", str(type)], instruction[0].text[3:])

    def call_label(self, instruction, index):
        self.check_arg_count(instruction, 1)
        self.check_types(instruction, '^label$')
        if (self.__labels.search(instruction[0].text)):
            int_lib.err.error_handler(int_lib.err.SEMANTICS_ERROR)
        self.__labels.insert(index, instruction[0].text)

    def call_jump(self, instruction):
        self.check_arg_count(instruction, 1)
        self.check_types(instruction, '^label$')
        if (not self.__labels.search(instruction[0].text)):
            int_lib.err.error_handler(int_lib.err.SEMANTICS_ERROR)
        return self.__labels.read(instruction[0].text)

    def call_jumpifeq(self, instruction, index):
        index = index + 1
        self.check_arg_count(instruction, 3)
        self.check_types(instruction, '^label$', '^(string|var|nil|int|bool)$', '^(string|var|nil|int|bool)$')

        if (not self.__labels.search(instruction[0].text)):
            int_lib.err.error_handler(int_lib.err.SEMANTICS_ERROR)

        ret_index = self.__labels.read(instruction[0].text)

        if (instruction[1].attrib['type'] == "var"):
            elem_1_value = self.get_var_value(instruction[1])
            elem_1_type = self.get_var_type(instruction[1])
        else:
            elem_1_value = instruction[1].text
            elem_1_type = instruction[1].attrib['type']

        if (instruction[2].attrib['type'] == "var"):
            elem_2_value = self.get_var_value(instruction[2])
            elem_2_type = self.get_var_type(instruction[2])
        else:
            elem_2_value = instruction[2].text
            elem_2_type = instruction[2].attrib['type']

        if (elem_1_type == "" or elem_2_type == ""):
            int_lib.err.error_handler(int_lib.err.MISSING_VALUE)

        if (elem_1_type != elem_2_type and elem_1_type != "nil" and elem_2_type != "nil"):
            int_lib.err.error_handler(int_lib.err.BAD_OPERAND_TYPES)

        if (elem_1_type == "int"):
            if (elem_2_type == "nil"):
                return index
            if (int(elem_1_value) == int(elem_2_value)):
                return ret_index
            else:
                return index
        elif (elem_1_type == "bool"):
            if (elem_2_type == "nil"):
                return index
            if ((elem_1_value.upper() == "FALSE" and elem_2_value.upper() == "FALSE") or (elem_1_value.upper() == "TRUE" and elem_2_value.upper() == "TRUE")):
                return ret_index
            else:
                return index
        elif (elem_1_type == "string" or elem_1_type == "nil"):
            if (str(elem_1_value) == str(elem_2_value)):
                return ret_index
            else:
                return index
        else:
            int_lib.err.error_handler(int_lib.err.SEMANTICS_ERROR)

    def call_jumpifneq(self, instruction, index):
        index = index + 1
        self.check_arg_count(instruction, 3)
        self.check_types(instruction, '^label$', '^(string|var|nil|int|bool)$', '^(string|var|nil|int|bool)$')

        if (not self.__labels.search(instruction[0].text)):
            int_lib.err.error_handler(int_lib.err.SEMANTICS_ERROR)

        ret_index = self.__labels.read(instruction[0].text)

        if (instruction[1].attrib['type'] == "var"):
            elem_1_value = self.get_var_value(instruction[1])
            elem_1_type = self.get_var_type(instruction[1])
        else:
            elem_1_value = instruction[1].text
            elem_1_type = instruction[1].attrib['type']

        if (instruction[2].attrib['type'] == "var"):
            elem_2_value = self.get_var_value(instruction[2])
            elem_2_type = self.get_var_type(instruction[2])
        else:
            elem_2_value = instruction[2].text
            elem_2_type = instruction[2].attrib['type']

        if (elem_1_type == "" or elem_2_type == ""):
            int_lib.err.error_handler(int_lib.err.MISSING_VALUE)

        if (elem_1_type != elem_2_type and elem_1_type != "nil" and elem_2_type != "nil"):
            int_lib.err.error_handler(int_lib.err.BAD_OPERAND_TYPES)

        if (elem_1_type == "int"):
            if (elem_2_type == "nil"):
                return ret_index
            if (int(elem_1_value) == int(elem_2_value)):
                return index
            else:
                return ret_index
        elif (elem_1_type == "bool"):
            if (elem_2_type == "nil"):
                return ret_index
            if ((elem_1_value.upper() == "FALSE" and elem_2_value.upper() == "FALSE") or (elem_1_value.upper() == "TRUE" and elem_2_value.upper() == "TRUE")):
                return index
            else:
                return ret_index
        elif (elem_1_type == "string" or elem_1_type == "nil"):
            if (str(elem_1_value) == str(elem_2_value)):
                return index
            else:
                return ret_index
        else:
            int_lib.err.error_handler(int_lib.err.SEMANTICS_ERROR)

    def call_exit(self, instruction):
        self.check_arg_count(instruction, 1)
        self.check_types(instruction, '^(var|int)$')
        if (instruction[0].attrib['type'] == "var"):
            if (self.get_var_type(instruction[0]) != "int" and self.get_var_type(instruction[0]) != ""):
                int_lib.err.error_handler(int_lib.err.BAD_OPERAND_TYPES)
            if (self.get_var_type(instruction[0]) == ""):
                int_lib.err.error_handler(int_lib.err.MISSING_VALUE)
            data = self.get_var_value(instruction[0])
            if (not re.match(r'^0*[0-4]?[0-9]$', data)):
                int_lib.err.error_handler(int_lib.err.BAD_VALUE)
            if (int(data) < 0 or int(data) > 49):
                int_lib.err.error_handler(int_lib.err.BAD_VALUE)
            exit(int(data))

        else:
            data = instruction[0].text
            if (not re.match(r'^0*[0-4]?[0-9]$', data)):
                int_lib.err.error_handler(int_lib.err.BAD_VALUE)

            if (int(data) < 0 or int(data) > 49):
                int_lib.err.error_handler(int_lib.err.BAD_VALUE)
            exit(int(data))

    def call_dprint(self, instruction):
        self.check_arg_count(instruction, 1)
        self.check_types(instruction, '^(string|var|nil|int|bool)$')
        sys.stderr.write("============DPRINT============\n")
        if (instruction[0].attrib['type'] == "var"):
            data = self.get_var_value(instruction[0])
            sys.stderr.write(data + "\n")
        else:
            sys.stderr.write(instruction[0].text + "\n")
        sys.stderr.write("============DPRINT============\n")

    def call_break(self, instruction):
        self.check_arg_count(instruction, 0)
        sys.stderr.write("============BREAK============\n")
        sys.stderr.write("Interpret actual state:\n")
        sys.stderr.write("\tGlobal frame variables in format [type, value]:\n")
        for var in self.__global_frame.get_data():
            value = self.__global_frame.read(var)
            sys.stderr.write("\t\t" + str(var) + ": " + str(value) + "\n")

        sys.stderr.write("\tTemp frame variables in format [type, value]:\n")
        if (self.__temp_frame == None):
            sys.stderr.write("\t\tTemp frame not init!\n")
        else:
            for var in self.__temp_frame.get_data():
                value = self.__temp_frame.read(var)
                if (value == None):
                    value = "None"
                sys.stderr.write("\t\t" + str(var) + ": " + str(value) +"\n")

        sys.stderr.write("\tLocal frame variables in format [type, value]:\n")
        if (self.__frame_stack.top() == None):
            sys.stderr.write("\t\tLocal frame not init!\n")
        else:
            for var in self.__frame_stack.top().get_data():
                value = self.__frame_stack.top().read(var)
                if (value == None):
                    value = "None"
                sys.stderr.write("\t\t" + str(var) + ": " + str(value) + "\n")

        sys.stderr.write("\tData stack items in format [type, value]:\n")
        if (self.__data_stack.is_empty()):
            sys.stderr.write("\t\tData stack is empty!\n")
        else:
            for data in self.__data_stack.get_data():
                sys.stderr.write("\t\t" + str(data) + "\n")

        sys.stderr.write("\tDefined labels:\n")
        if (not self.__labels.get_data()):
            sys.stderr.write("\t\tNo label loaded!\n")
        else:
            for data in self.__labels.get_data():
                sys.stderr.write("\t\t" + str(data) + ": " + str(self.__labels.read(data)) + "\n")

        sys.stderr.write("============BREAK============\n")
