#coding: utf-8

### Imports ### ------------------------------------------------------------
from itertools import count
import kor.value_type as v
import kor.errors as e

### Class ### ------------------------------------------------------------
class Kor:
	"""
	The main class that will represent your .kor file

	list of method :

				#Managing the file

					add_author(author)
					add_desc(desc)

					get_author()
					get_desc()

					reset()

				#Comments

					encode_comment(line, value)

				#Decoding

					decode(custom_line_type:list=None, custom_decoding:list=None, custom_separator:list=None)
					*some other method that are made to be used by 'encode()'*

				#Write and read

					write(content)
					read()

					delete(line, replace_blank=True)
	"""
	_instances_count = count(0)

	def __init__(self, file_path):
		"""
		:param file_path: path to your .kor file
		"""
		self.file_path = file_path

		if not self.file_path.endswith(".kor"):
			raise e.NotKorFile("The file is not a '.kor' file")

		self.id = next(self._instances_count)


	def __repr__(self):#TODO : Add to changelog
		return f"Kor file at '{self.file_path}'"

	def __eq__(self, other):#TODO : Add to changelog
		if self.file_path == other:
			return True
		else:
			return False

	def __ne__(self, other):#TODO : Add to changelog
		if self.file_path == other.file_path:
			return False
		else:
			return True

	#Managing the file options
	def add_author(self, author):
		"""
		use to add an author to your file
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
		use to add a description to your file

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
		returns the description of the file

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
		resets your file (=erase every thing)

		"""
		f = open(self.file_path, "w+")
		f.close()

	# Comments ------------------------------------------------------------
	def encode_comment(self, line, value):
		"""
		Add comment to you file
		:param line: the line of your comment
		:param value: the content of the comment
		:return:
		"""

		file_content = self.read()

		try: file_content[line]

		except:
			line_number = len(file_content)
			for x in range((line-line_number)):
				file_content.append("\n")

			file_content.insert(line, f"#{value}\n")
		else:
			del file_content[line]
			file_content.insert(line, f"#{value}\n")

		self.write(file_content)

	# Decoding ------------------------------------------------------------
	def decode(self, custom_line_type:list=None, custom_decoding:list=None, custom_separator:list=None):
		"""
		returns a list of all the line object (see 'value_type.py") in the file

		:param custom_line_type: list of all your custom line type			|
		:param custom_decoding:	list of all your custom decoding functions	|---> Put all of these in the right order :
		:param custom_separator: list of all your custom separators			|		custom_line_type = ['custom1", 'custom2', ...]
																					custom_decoding = ['custom1', 'custom2", ...]
																					custom_separators = ['custom1', 'custom2', ...
		"""
		file_content = self.read()

		file_output = []

		for line in file_content:
			if line.startswith("var : "):
				file_output.append(self._decode_var(line=line))

			elif line.startswith("list : "):
				file_output.append(self._decode_list(line=line))

			elif line.startswith("#"):
				file_output.append(line[1:])

			elif custom_line_type:
				for x in range(len(custom_line_type)):
					if line.startswith(custom_line_type[x]):
						file_output.append(self._decode_custom(line=line, line_type=custom_line_type[x], decoding=custom_decoding[x], separator=custom_separator[x]))


		return file_output

	def _decode_var(self, line):
		"""
		internal method to decode var
		Recommend to not use

		"""
		line_args = list(line[6:].split(" -> "))

		if line_args[1] == "num":
			value = v.Var(name=line_args[0], value=int(line_args[2]), value_type=line_args[1])

		elif line_args[1] == "bool":
			if line_args[2][:-1] == "True":
				the_bool = True
			else:
				the_bool = False

			value = v.Var(name=line_args[0], value=the_bool, value_type=line_args[1])
		else:
			value = v.Var(name=line_args[0], value=f"'{line_args[2][:-1]}'", value_type=line_args[1])

		return value


	def _decode_list(self, line):
		"""
		internal method to decode list
		Recommend to not use

		"""
		line_args = list(line[7:-1].split(" -> "))

		list_args = list(line_args[2].split(','))

		f_list_args = []

		if line_args[1] == "num":
			for element in list_args:
				f_list_args.append(int(element))

			value = v.List(name=line_args[0], value=f_list_args, value_type=line_args[1])

		elif line_args[1] == "bool":
			for element in list_args:
				if element == "True" or element == "True\n":
					f_list_args.append(True)
				else:
					f_list_args.append(False)

			value = v.List(name=line_args[0], value=f_list_args, value_type=line_args[1])

		else:
			for element in list_args:
				f_list_args.append(element)

			value = v.List(name=line_args[0], value=f_list_args, value_type=line_args[1])

		return value

	def _decode_custom(self, line, line_type, decoding, separator):
		"""
		used to decode custom line type
		Recommend to not use
		"""
		value_type_len = len(line_type)+3

		line_args = list(line[value_type_len:-1].split(" -> "))

		value_args = list(line_args[2].split(separator))

		value = decoding(value_args)

		return value

	#Write and read ------------------------------------------------------------
	def write(self, content:list):
		"""
		used to write directly to the file
		:param content: a list of all the line to write to the file

		"""
		with open(self.file_path, mode="w", encoding='utf-8') as file:
			for line in content:
				file.write(line)

	def read(self):
		"""
		return a list of the raw lines (as you can see theme in the .kor file)

		"""
		with open(self.file_path, "r", encoding="utf-8") as file:
			return file.readlines()

	def delete(self, line, replace_blank = True):
		"""
		Delete a line in the file

		:param line: the line that you want to delete
		:param replace_blank: True = Replace with blank line			False = not replace with blank line
		"""
		file_content = self.read()

		del file_content[line]

		if replace_blank:
			file_content.insert(line, "\n")


		self.reset()

		self.write(file_content)