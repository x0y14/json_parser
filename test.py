from json_parser_v2 import *


parser = Parser(
	raw='''{ "this is key" : "this is value" }'''
)
result = parser.parse()
assert(result.key.data == 'this is key')
assert(result.value.value_type == JsonValueType.String)
assert(result.value.data == 'this is value')
print('test_String: passed')


parser = Parser(
	raw='''{ "this is key" : 1234 }'''
)
result = parser.parse()
assert(result.key.data == 'this is key')
assert(result.value.value_type == JsonValueType.Number)
assert(result.value.data == 1234)
print('test_Number: passed')


parser = Parser(
	raw='''{ "this is key" : true }'''
)
result = parser.parse()
assert(result.key.data == 'this is key')
assert(result.value.value_type == JsonValueType.Boolen)
assert(result.value.data == True)
print('test_Boolen: passed')


parser = Parser(
	raw='''{ "this is key" : { "second": 2 } }'''
)
result = parser.parse()
assert(result.key.data == 'this is key')
assert(result.value.key.data == 'second')
assert(result.value.value.value_type == JsonValueType.Number)
assert(result.value.value.data == 2)
print('test_inJson: passed')