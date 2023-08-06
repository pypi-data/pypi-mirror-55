#coding: utf-8

### Imports ### ------------------------------------------------------------
import kor.kor_file as k
import kor.errors as e

### Class ### ------------------------------------------------------------
    ### VAR ### ------------------------------------------------------------
class Var:
    """
    Represent your var-type lines
    """
    possible_value_type = ["num", "str", "bool"]

    def __init__(self, name, value, value_type):
        """
        :param name: Name of your line
        :param value: content of your line
        :param value_type: type of content
        """
        #var : {name} -> {value_type} -> {value}\n"
        self.name = name
        self.value = value

        if not value_type in self.possible_value_type:
            raise e.InvalidValueType(f"'{value_type}' is not a valid value type")
        else:
            self.value_type = value_type


    def __repr__(self):
        return f"Var object : name={self.name}, value={self.value}, value_type={self.value_type}"

    def __eq__(self, other):
        if self.name == other.name and self.value_type == other.value_type:
            return True
        else:
            return False

    def __ne__(self, other):
        if self.__eq__(other):
            return False
        else:
            return True

    #Encoding ------------------------------------------------------------
    def encode(self, line, file, override=False): #TODO : Add 'override' to changelog
        """
        Encode your var to the specified file

        :param line: line where your var should be encoded
        :param file: the file where the var should be encoded
        :param override: True = delete the existing line and replace it with the new one                False=Do not delete the existing line, add it after the existing line
        """
        if not override:
            file_content_decoded = file.decode()

            for line_file in file_content_decoded:
                if self == line_file[1]:
                    return None

        file_content = k.Kor.read(file)

        try:
            file_content[line]

        except:
            line_number = len(file_content)
            for x in range((line - line_number)):
                file_content.append("\n")

            file_content.insert(line, f"var : {self.name} -> {self.value_type} -> {self.value}\n")
        else:
            del file_content[line]
            file_content.insert(line, f"var : {self.name} -> {self.value_type} -> {self.value}\n")

        k.Kor.write(file, content=file_content)



    ### LIST ### ------------------------------------------------------------
class List:
    """
    Represent your list-type lines
    """
    possible_value_type = ["num", "str", "bool"]

    def __init__(self, name, value, value_type):
        self.name = name
        self.value = value

        if not value_type in self.possible_value_type:
            raise e.InvalidValueType(f"'{value_type}' is not a valid value type")
        else:
            self.value_type = value_type


    def __repr__(self):
        return f"List object name={self.name}, value={self.value}, value_type={self.value_type}"

    def __eq__(self, other):
        if self.name == other.name and self.value_type == other.value_type:
            return True
        else:
            return False

    def __ne__(self, other):
        if self.__eq__(other):
            return False
        else:
            return True

    #Encoding ------------------------------------------------------------
    def encode(self, line, file, override=False):#TODO : Same as Var.encode()
        """
                Encode your list to the specified file

                :param line: line where your list should be encoded
                :param file: the file where the var should be encoded
                :param override: True = delete the existing line and replace it with the new one                False=Do not delete the existing line, add it after the existing line
                """
        if not override:
            file_content_decoded = file.decode()

            for line_file in file_content_decoded:
                if self == line_file[1]:
                    return None

        file_content = k.Kor.read(file)

        try:
            file_content[line]

        except:
            line_number = len(file_content)
            for x in range((line - line_number)):
                file_content.append("\n")

            value_to_insert = ""

            for element in self.value:
                value_to_insert += f"{element},"

            file_content.insert(line, f"list : {self.name} -> {self.value_type} -> {value_to_insert[:-1]}\n")
        else:
            del file_content[line]
            value_to_insert = ""

            for element in self.value:
                value_to_insert += f"{element},"

            file_content.insert(line, f"list : {self.name} -> {self.value_type} -> {value_to_insert[:-1]}\n")

        k.Kor.write(file,file_content)

    ###CUSTOM ###------------------------------------------------------------
class CustomLines:
    """
    Represent your custom type lines

    """
    def __init__(self, name, value, custom_encoding, custom_value_type, custom_separator, custom_line_type):
        """
        :param name: Name of the line
        :param value: content of the line
        :param custom_encoding: function to properly encode your custom type
        :param custom_value_type:
        :param custom_separator: every thing but '->'
        :param custom_line_type:
        """
        self.name = name
        self.value = value
        self.custom_encoding = custom_encoding
        self.custom_value_type = custom_value_type
        self.custom_separator = custom_separator
        self.custom_line_type = custom_line_type

    def __repr__(self):
        return f"List object name={self.name}, value={self.value}, value_type={self.custom_encoding}"

    def __eq__(self, other):
        if self.name == other.name and self.custom_encoding == other.custom_encoding:
            return True
        else:
            return False

    def __ne__(self, other):
        if self.__eq__(other):
            return False
        else:
            return True

    # Encoding ------------------------------------------------------------
    def encode(self, line, file, override=False):
        """
                Encode your custom type to the specified file

                :param line: line where your custom type should be encoded
                :param file: the file where the var should be encoded
                :param override: True = delete the existing line and replace it with the new one                False=Do not delete the existing line, add it after the existing line
                """
        if not override:
            file_content_decoded = file.decode()

            for line_file in file_content_decoded:
                if self == line_file[1]:
                    return None


        file_content = k.Kor.read(file)

        try:
            file_content[line]

        except:
            line_number = len(file_content)
            for x in range((line - line_number)):
                file_content.append("\n")

            file_content.insert(line, self.custom_encoding(self.custom_line_type, self.name, self.value, self.custom_value_type, self.custom_separator))
        else:
            del file_content[line]
            file_content.insert(line, self.custom_encoding(self.custom_line_type, self.name, self.value, self.custom_value_type, self.custom_separator))

        k.Kor.write(file,file_content)