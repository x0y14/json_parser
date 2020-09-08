from json_parser import *

parser = Parser(
	raw='''{ "its key" : [12, 34, 56, { "inList": "Hi" }, ["hello", "hi", "good night"]], "sec": "909090"}'''
)
result = parser.parse()
print(result)