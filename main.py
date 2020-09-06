from json_parser_final import *


parser = Parser(
	raw='''{ "this is key" : "this is value" }'''
)
result = parser.parse()
print(vars(result))