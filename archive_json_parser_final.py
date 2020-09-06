import re
import enum


class JsonKey:
	def __init__(self, data):
		self.data = data
		super().__init__()

class JsonValueType(enum.Enum):
	String = enum.auto()
	Boolen = enum.auto()
	Number = enum.auto()

class JsonValue:
	def __init__(self, value_type, data):
		self.data = data
		self.value_type = value_type
		super().__init__()

class Json:
	# key: JsonKey
	# value: JsonValue
	def __init__(self, key, value):
		self.key = key
		self.value = value
		super().__init__()


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
		# self.pos += 1

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
	
	def int_boolen_analyze(self, value):
		# print(value)
		value = value.replace(' ', '')#
		# value.strip()#
		if value == 'true':
			return JsonValue(JsonValueType.Boolen, True)
		elif value == 'false':
			return JsonValue(JsonValueType.Boolen, False)
		else:
			integer = re.match(r'([-0-9]+)', value)
			return JsonValue(JsonValueType.Number, int(integer.group(1)))
	
	def consume_whilespace(self):
		while self.is_eof() == False:
			if self.get_char() == ' ':
				self.consume_char()
				continue
			else:
				break

	def parallel_values(self):
		# def parallel_continue(self):
		# 	self.consume_whilespace()
		# 	if self.get_char() == ',':
		# 		self.consume_char()

		p_values = []
		assert(self.get_char() == '['); self.consume_char()
		# ["hello", true, 10903909, {"key": "value"}]

		while self.is_eof() == False:
			self.consume_whilespace()
			if self.get_char() == '"':
				# str
				self.consume_char()# "
				p_values.append(JsonValue(JsonValueType.String, self.go_to('"'))) # value
				self.consume_char()# "

				# [same script]
				self.consume_whilespace()
				if self.get_char() == ',':
					self.consume_char()
					continue
				elif self.get_char() == ']':
					self.consume_char()
					return p_values


			elif self.get_char() in  ['-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
				# int
				pass
			elif self.get_char() in ['t', 'f']:
				# boolen
				pass
			elif self.get_char() in '{':
				# dict
				pass
			# elif self.get_char() == ']':
			# 	self.consume_char()
			# 	return p_values
			else:
				raise SyntaxError('{ "key" : Unknown-Object }')




	def analyze_value(self):
		j_values = []
		assert(self.get_char() == ':'); self.consume_char()
		self.consume_whilespace()

		while self.is_eof() == False:
			if self.get_char() in ['-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 't', 'f']:
				# int or bool
				v_ = self.consume_while([' ', '}'])
				value = self.int_boolen_analyze(v_); self.consume_char()
				return value

			elif self.get_char() == '"':
				# str
				self.consume_char()
				value = self.go_to('"'); self.consume_char()
				return value

			elif self.get_char() == '{':
				# j in j
				return self.parse()
			elif self.get_char() == '[':
				# list
				pass
			else:
				raise SyntaxError('{ "key": Unknown-Object }')

			# if (self.get_char() in ['-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 't', 'f']):
			# 	# true or false or -123456789
			# 	v_ = self.consume_while([' ', '}'])
			# 	# print()
			# 	value = self.int_boolen_analyze(v_); self.consume_char()
			# 	# if self.get_char() == ',':
			# 	# 	self.consume_char()
			# 	# 	print(self.parse_())
			# 	return value
			# elif self.get_char() == '{':
			# 	return self.parse()
			# elif self.get_char() == '"':
			# 	_ = self.go_to('"'); self.consume_char()
			# 	value = self.go_to('"'); self.consume_char()
			# 	# if self.get_char() == ',':
			# 	# 	self.consume_char()
			# 	# 	print(self.parse_())
			# 	return JsonValue(JsonValueType.String, value)
			# else:
			# 	# print(self.get_char())
			# 	ValueError('Unkn')


	def analyze_key(self):
		# analyze key step
		# assert(self.get_char() == '"'); self.consume_char()
		maybe_space = self.go_to('"')
		assert(self.get_char() == '"');
		self.consume_char()

		key = self.go_to('"')
		return JsonKey(key)
	
	def parse_(self):
		json_dom = []
		while self.is_eof() == False:
			key = self.analyze_key()
			self.go_to(':')
			value = self.analyze_value()
			json_dom.append(Json(key, value))
			# print(json_dom)
			if self.get_char() == ',':
				self.consume_char()
				print(self.parse_())
		return json_dom

	
	def parse(self):
		# json in json があり得るので、key解析と、value解析は分けたよ。key解析は分けなくてもよかった気がするよ。
		# dom = []
		assert(self.get_char() == '{'); self.consume_char()
		return self.parse_()
		# # print(self.get_char())
		# key = self.analyze_key()
		# # print(key)
		# self.go_to(':')
		# value = self.analyze_value()
		# # print(f'key: {key}, value: {value}')
		# # return (key, value)
		# return Json(key, value)