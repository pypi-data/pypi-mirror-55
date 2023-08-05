#coding: utf-8
### INFORMATION ### ------------------------------------------------------------
"""
kor_project by KoraKu (AKA Hugo Costa)

This module is for working with .kor files, here's the template for the file

         ________________________________________
       0 |*Author : <file author>               |
       1 |*Desc : <file bio>                    |
       2 |                                      |
       3 |#comment                              |
       4 |                                      |
       5 |var : <name> -> <type> -> <value>     |
       6 |                                      |
       7 |list : <name> -> <type> -> <value>    |
       8 |                                      |
       9 |                                      |
      10 |                                      |
      11 |                                      |
      12 |                                      |
      13 |______________________________________|


As you can see the first to line are information about the file

comments are marked by '#' on the very first char of the line

to store number of string we use 'var' with the syntax showed
same for storing list, but with 'list' instead of 'var'

how to use ?

    1)
    import kor

    2) create your kor file object
    file = kor.Kor(file_path="<file_path.kor>")

    3) now you can use the methode on your file, for instance you can add a author
    file.add_author(author=<auhtor name>)

    and you can see wath the author is with 'get_author'

    file.get_author()



    see exemple .py to see how encode and decode custom line type


"""

### Class ### ------------------------------------------------------------
class NotKorFile(Exception):
    pass

class Kor:
    def __init__(self, file_path):
        self.file_path = file_path
        if not self.file_path.endswith(".kor"):
            raise NotKorFile("The file is not a '.kor' file")

    #Managing the file options
    def add_author(self, author):
        """
        used to add an author to the file
        """
        with open(self.file_path, mode="r", encoding='utf-8') as file:
            file_content = file.readlines()


        try:
            if not file_content[0].startswith("*Author :"):
                file_content.insert(0, f"*Author : {author}\n")
            else:
                del file_content[0]
                file_content.insert(0, f"*Author : {author}\n")
        except:
            file_content.insert(0, f"*Author : {author}\n")

        self.write(file_content)

    def add_desc(self, desc):
        """
        used to add a description to the file

        """
        with open(self.file_path, mode="r", encoding='utf-8') as file:
            file_content = file.readlines()

        try:
            if not file_content[1].startswith("*Desc : "):
                file_content.insert(1, f"*Desc : {desc}\n")
            else:
                del file_content[1]
                file_content.insert(1, f"*Desc : {desc}\n")

        except:
            file_content.insert(1, f"*Desc : {desc}\n")

        self.write(file_content)

    def get_author(self):
        """
        returns the author of the file
        """
        with open(self.file_path, "r", encoding='utf-8') as file:
            try:
                author = file.readline()
                return author[10:-1]
            except:
                return None

    def get_desc(self):
        """
        the description of the file

        """
        with open(self.file_path, "r", encoding='utf-8') as file:
            try:
                desc = file.readline()
                desc = file.readline()
                return desc[8:-1]
            except:
                return None

    def reset(self):
        """
        use to reset the content of your file

        """
        f = open(self.file_path, "w+")
        f.close()



    # Encoding ------------------------------------------------------------
    def encode(self, line_type, line, name, value, value_type, custom_encoding=None, custom_line_type=None, custom_value_type=None, override=False):
        """
        use to encode data to your file

        avalable line type :
            - var
            - comment
            - list

        line : the line number
        name : name for var ad list
        value : content of the line
        value_type = num or str
        """
        #checks
        if line_type == "comment":
            return self.write(self.encode_comment(line=line, value=value))

        elif line_type == "var":
            if not override:
                if self.search(line_type='var', name=name)[0]:
                    return None

            if not value_type in ["num", "str"]:
                return None
            else:
                return self.write(content=self.encode_var(line=line, name=name, value=value, value_type=value_type))

        elif line_type == "list":
            if not self.search(line_type='list', name=name)[0]:
                if not value_type in ["num", "str"]:
                    return None
                else:
                    return self.write(self.encode_list(line=line, name=name, value=value, value_type=value_type))

        elif line_type == "custom":
            self.write(self.encode_custom(line=line, name=name, value=value,custom_encoding=custom_encoding, custom_value_type=custom_value_type, custom_line_type=custom_line_type))

        else:

            return None


    def encode_comment(self, line, value):
        """
        internal method to encode comments

        """
        file_content = self.read()

        try: file_content[line]

        except:
            line_number = len(file_content)
            for x in range((line-line_number)):
                file_content.append("\n")

            file_content.insert(line, f"#{value}")
        else:
            del file_content[line]
            file_content.insert(line, f"#{value}")

        return file_content


    def encode_var(self, line, name, value, value_type):
        """
        internal method to encode var

        """
        file_content = self.read()

        try:
            file_content[line]

        except:
            line_number = len(file_content)
            for x in range((line - line_number)):
                file_content.append("\n")

            file_content.insert(line, f"var : {name} -> {value_type} -> {value}\n")
        else:
            del file_content[line]
            file_content.insert(line, f"var : {name} -> {value_type} -> {value}\n")

        return file_content

    def encode_list(self, line, name, value, value_type):
        """
        internal method to encode list

        """
        file_content = self.read()

        try:
            file_content[line]

        except:
            line_number = len(file_content)
            for x in range((line - line_number)):
                file_content.append("\n")

            value_to_insert = ""

            for element in value:
                value_to_insert += f"{element},"

            file_content.insert(line, f"list : {name} -> {value_type} -> {value_to_insert[:-1]}\n")
        else:
            del file_content[line]
            value_to_insert = ""

            for element in value:
                value_to_insert += f"{element},"

            file_content.insert(line, f"list : {name} -> {value_type} -> {value_to_insert[:-1]}\n")

        return file_content

    # Decoding ------------------------------------------------------------
    def decode(self, custom_line_type=None, custom_decoding=None, custom_separator=None):
        """
        return a list with all the line of the file, ready to use in python script

        """
        file_content = self.read()

        file_output = []

        for line in file_content:
            if line.startswith("var : "):
                file_output.append(self.decode_var(line=line))

            elif line.startswith("list : "):
                file_output.append(self.decode_list(line=line))

            elif line.startswith("#"):
                file_output.append(line[1:])

            elif custom_line_type:
                if line.startswith(custom_line_type):
                    file_output.append(self.decode_custom(line=line, custom_line_type=custom_line_type, custom_decoding=custom_decoding, custom_separator=custom_separator))


        return file_output

    def decode_var(self, line) -> tuple:
        """
        internal method to decode var

        """
        line_args = list(line[6:].split(" -> "))

        if line_args[1] == "num":
            value = int(line_args[2][:-1])

        else:
            value = str(line_args[2][:-1])

        return line_args[0], value


    def decode_list(self, line) -> tuple:
        """
        internal method to decode list

        """
        line_args = list(line[7:-1].split(" -> "))

        print(line_args)

        list_args = list(line_args[2].split(','))

        f_list_args = []

        if line_args[1] == "num":
            for element in list_args:
                f_list_args.append(int(element))
        else:
            f_list_args = list_args

        return line_args[0], f_list_args

    #Write and read ------------------------------------------------------------
    def write(self, content):
        """
        used to write directly to the file

        """
        with open(self.file_path, mode="w", encoding='utf-8') as file:
            for line in content:
                file.write(line)

    def read(self):
        """
        return a list of the non-process lines

        """
        with open(self.file_path, "r", encoding="utf-8") as file:
            return file.readlines()

    def delete(self, line):
        """
        delete a specific line ine the file

        """
        with open(self.file_path, "r", encoding='utf-8') as file:
            file_content = file.readlines()

        del file_content[line]

        self.reset()

        self.write(file_content)

    # Searching ------------------------------------------------------------
    def search(self, line_type, name) -> list:
        """
        search if a var or list with the same name already exist, return a list with True, the var/list name and var/list line

        """
        with open(self.file_path, "r", encoding='utf-8') as file:
            line_list = file.readlines()

        list_list = []
        var_list = []

        for line in range(len(line_list)):
            if line_list[line].startswith("var : "):
                var_name = list(line_list[line][6:].split(" ->"))

                var_list.append([line, var_name[0]])

            elif line_list[line].startswith("list : "):
                list_name = list(line_list[line][7:].split(" ->"))

                list_list.append([line, list_name[0]])

        if line_type == "var":
            for line in var_list:
                if name in line:
                    return [True, name, line[0]]

        elif line_type == "list":
            for line in list_list:
                if name in line:
                    return [True, name, line[0]]

        return [False, None, None]

    # Custom ------------------------------------------------------------

    def encode_custom(self, line, name, custom_line_type, value, custom_value_type, custom_encoding):
        """
        used to encode custom line type

        """
        file_content = self.read()

        try:
            file_content[line]

        except:
            line_number = len(file_content)
            for x in range((line - line_number)):
                file_content.append("\n")

            file_content.insert(line, custom_encoding(line_type=custom_line_type, name=name, value=value, value_type=custom_value_type))
        else:
            del file_content[line]
            file_content.insert(line, custom_encoding(line_type=custom_line_type, name=name, value=value, value_type=custom_value_type))

        return file_content

    def decode_custom(self, line, custom_line_type, custom_decoding, custom_separator):
        """
        used to decode custom line type

        """
        to_crop = len(custom_line_type)+3

        line_args = list(line[to_crop:].split(" -> "))
        value_args = list(line_args[2].split(custom_separator))

        value = custom_decoding(value_args)

        return line_args[0], value
