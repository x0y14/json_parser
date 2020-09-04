class JsonKey:
	def __init__(self, key):
		self.key = key
		super().__init__()

class JsonValue:
	def __init__(self, value_type, data):
		self.value_type = value_type
		self.data = data
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
				print(f'[go_to_char]: in while: consumed: {c_} (pos: {self.pos - 1}), now: {self.pos}')
				consumed += c_
	
	def read(self):
		assert(self.get_char() == '{'); self.consume_char()
		# {

		maybe_space = self.go_to_char('"'); print(maybe_space); self.consume_char()
		# { "
		key = self.go_to_char('"')
		# { "key"
		assert(self.get_char() == '"'); self.consume_char()

		maybe_space = self.go_to_char(':'); print(maybe_space); self.consume_char()
		# { "key" : 
		maybe_space = self.go_to_char('"'); print(maybe_space); self.consume_char()
		# { "key" : "
		value = self.go_to_char('"')
		# { "key" : "value"
		assert(self.get_char() == '"'); self.consume_char()
		maybe_space = self.go_to_char('}'); print(maybe_space); self.consume_char()

		# k = JsonKey(key)
		# v = JsonValue(str, value)
		# return Json(k, v)
		return (key, value)


def test():
	ps1 = Parser(
		raw='{"key": "value"}'
		)
	result = ps1.read()
	assert(result == ('key', 'value'))

	ps2 = Parser(
		raw='{ "key" : "value" }'
		)
	result = ps2.read()
	assert(result == ('key', 'value'))

	ps3 = Parser(
		raw='{            "key"      :                \t"value" }'
		)
	result = ps3.read()
	assert(result == ('key', 'value'))
	return True


def main():
	ps = Parser(
		raw='{"this is key": "this is value"}'
		)

	result = ps.read()
	print(result)

if __name__ == '__main__':
	main()