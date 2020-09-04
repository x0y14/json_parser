from json_parser_v2 import *


parser = Parser(
	raw='''{ "this is key" : "this is value" }'''
)
result = parser.parse()
print(vars(result))