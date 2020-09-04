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
	
	def go_to_char(self, char):
		# 指定した文字まで吹っ飛ぶ、そこまでで得た文字を返す。ex) raw=hello, go_to_char("o"): return -> "hell"
		consumed = ''
		# self.pos += 1

		while self.is_eof() == False:
			if self.get_char() == char:
				return consumed
			else:
				c_ = self.consume_char()
				# print(f'[go_to_char]: in while: consumed: {c_} (pos: {self.pos - 1}), now: {self.pos}')
				consumed += c_
	
	def find_char(self, char):
		# こっから先にcharがあるのか確認するよ。
		# jsonがでっかい場合すんごく時間がかかるので、絶対いけない方法だと思うけど、これ以外、思いつかないよ。(><;)
		consumed = ''
		# self.pos += 1
		reset = 0

		while self.is_eof() == False:
			if self.get_char() == char:
				self.pos -= reset
				return True
			else:
				c_ = self.consume_char()
				reset += 1
				# print(f'[go_to_char]: in while: consumed: {c_} (pos: {self.pos - 1}), now: {self.pos}')
				consumed += c_
		self.pos -= reset
		return False
	
	def int_boolen_analyze(self, value):
		# print(value)
		value = value.replace(' ', '')#
		# value.strip()#
		if value == 'true':
			return JsonValue(JsonValueType.Boolen, True)
		elif value == 'false':
			return JsonValue(JsonValueType.Boolen, False)
		else:
			integer = re.match(r'([0-9]+)', value)
			return JsonValue(JsonValueType.Number, int(integer.group(1)))
	
	def analyze_value(self):
		# assert(self.get_char() == '{'); self.consume_char()
		assert(self.get_char() == ':'); self.consume_char()
		# print(self.find_char('{'))
		if self.find_char('{') == False:
			# dose not have child
			if self.find_char('"') == False:
				# # int or boolen
				# print('not str')
				v_ = self.go_to_char('}')
				value = self.int_boolen_analyze(v_)
				return value
			else:
				# str
				_ = self.go_to_char('"'); self.consume_char()
				value = self.go_to_char('"')
				# print('trash: ',_,', value:', value)
				return JsonValue(JsonValueType.String, value)
		else:
			maybe_space = self.go_to_char('{')
			return self.parse()


	def analyze_key(self):
		# analyze key step
		# assert(self.get_char() == '"'); self.consume_char()
		maybe_space = self.go_to_char('"')
		assert(self.get_char() == '"');
		self.consume_char()

		key = self.go_to_char('"')
		return JsonKey(key)

	
	def parse(self):
		# json in json があり得るので、key解析と、value解析は分けたよ。key解析は分けなくてもよかった気がするよ。
		# dom = []
		assert(self.get_char() == '{'); self.consume_char()
		# print(self.get_char())
		key = self.analyze_key()
		# print(key)
		self.go_to_char(':')
		value = self.analyze_value()
		# print(f'key: {key}, value: {value}')
		# return (key, value)
		return Json(key, value)