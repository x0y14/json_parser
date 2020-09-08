# import enum
from modules.string_converter import StringConverter

# class JsonKey:
# 	def __init__(self, data):
# 		self.data = data
# 		super().__init__()

# class JsonValueType(enum.Enum):
# 	String = enum.auto()
# 	Boolen = enum.auto()
# 	Int = enum.auto()
# 	Float = enum.auto()
# 	List = enum.auto()
# 	Json = enum.auto()

# class JsonKapsel:
# 	def __init__(self, data):
# 		self.data = data
# 		super().__init__()

# class JsonValue:
# 	def __init__(self, value_type, data):
# 		self.data = data
# 		self.value_type = value_type
# 		super().__init__()

# class Json:
# 	def __init__(self, key, value):
# 		self.key = key
# 		self.value = value
# 		super().__init__()


class Parser:
	def __init__(self, raw):
		self.raw = raw
		self.pos = 0
		super().__init__()
	
	def is_eof(self) -> bool:
		return len(self.raw) <= self.pos
	
	def get_char(self) -> str:
		# 現在地の文字を取得、動かない
		return self.raw[self.pos]
	
	def consume_char(self) -> str:
		c_ = self.raw[self.pos]
		self.pos += 1
		return c_
	
	def go_to(self, char):
		# 指定した文字まで吹っ飛ぶ、そこまでで得た文字を返す。ex) raw=hello, go_to("o"): return -> "hell"
		consumed = ''

		while self.is_eof() == False:
			if self.get_char() == char:
				return consumed
			else:
				c_ = self.consume_char()
				# print(f'[go_to]: in while: consumed: {c_} (pos: {self.pos - 1}), now: {self.pos}')
				consumed += c_
	
	def consume_while(self, chars=[]):
		s = ''
		while self.is_eof() == False:
			if self.get_char() in chars:
				return s
			else:
				s += self.consume_char()

	def consume_whilespace(self):
		while self.is_eof() == False:
			if self.get_char() == ' ':
				self.consume_char()
				continue
			else:
				return 0
	
	def find_value(self):
		value_end = [',', ' ', '}', ']']
		self.consume_whilespace()

		# int
		if self.get_char() in ['-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
			data = self.consume_while(value_end)
			int_data, is_float = StringConverter(data).convert()

			self.consume_whilespace()
			if is_float:
				# return JsonValue(JsonValueType.Float, int_data)
				return int_data

			# return JsonValue(JsonValueType.Int, int_data)
			return int_data

		# str
		elif self.get_char()  == '"':
			self.consume_char()
			data = self.go_to('"')
			self.consume_char()
			# return JsonValue(JsonValueType.String, data)
			# print(data)
			return data
		
		# boolen
		elif self.get_char() in ['t', 'f']:
			data = self.consume_while(value_end)
			if data == 'true':
				self.consume_char()
				# return JsonValue(JsonValueType.Boolen, True)
				return True

			elif data == 'false':
				self.consume_char()
				# return JsonValue(JsonValueType.Boolen, False)
				return False

			else:
				raise SyntaxError('Unknown Object')
		
		elif self.get_char() == '{':
			data = self.parse()
			# return JsonValue(JsonValueType.Json, data)
			# print(data)
			return data

		elif self.get_char() == '[':
			values = []
			self.consume_char()
			while self.is_eof() == False:
				v = self.find_value()
				values.append(v)
				if self.get_char() in [',', '"', "}"]:
					self.consume_char()
					continue
				elif self.get_char() == ']':
					self.consume_char()
					# return JsonValue(JsonValueType.List, values)
					# print(values)
					return values
				else:
					raise SyntaxError(f'[Pannic]: {self.get_char()}')
		else:
			raise SyntaxError(f'[Pannic]: {self.get_char()}')
	
	# def kapsel_check(self, list_):
	# 	# pass
	# 	n = 0
	# 	for i in list_:
	# 		print(i)
	# 		n += 1
	# 	print(n)
	# 	if n == 1:
	# 		return list_[0]
	# 	else:
	# 		list_

	def parse(self):
		result = {}
		while self.is_eof() == False:
			# print(result)

			if self.get_char() == '{':
				self.consume_char()

			# find `key`
			self.consume_whilespace()
			assert(self.get_char() == '"'); self.consume_char()# hit and go next
			key = self.go_to('"'); self.consume_char()# hit and go next

			# find `:`
			self.consume_whilespace()
			assert(self.get_char() == ':')# hit
			self.consume_char()

			# find `value`
			value = self.find_value()

			# self.consume_char()
			self.consume_whilespace()
			# result.append(Json(JsonKey(key), value))
			# result.append({key: value})
			result[key] = value

			if self.get_char() == '}':
				self.consume_char()# 忘れがち, Noneが出てきたらだいたいこれし忘れ。
				# print(result)
				# return self.kapsel_check(result)
				return result
				# return JsonKapsel(result)
				# return Json(JsonValueType.List, result)

			elif self.get_char() == ',':
				self.consume_char()
				continue

