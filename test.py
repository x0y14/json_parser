from json_parser import *


# result = Parser(
# 	raw='''{ "this is key" : -500 }'''
# 	).parse()

# for r in result:
# 	print(r.key.data)
# 	print(r.value.data)



# result = Parser(
# 	raw='''{ "its key" : "its value" }'''
# 	).parse()
# print('result: ', vars(result[0]))

# result = Parser(
# 	raw='''{ "its key" : true }'''
# 	).parse()
# print('result: ', vars(result[0]))



# result = Parser(
# 	raw='''{ "its key" : { "inJson" : "Hello" } }'''
# 	).parse()
# print('result: ', vars(result[0]))



# result = Parser(
# 	raw='''{ "its key" : [12, 34, 56] }'''
# 	).parse()
# print('result: ', vars(result[0]))



# result = Parser(
# 	raw='''{ "its key" : [12, 34, 56, { "inList": "Hi" }, ["hello", "hi", "good night"]] }'''
# 	).parse()

# for r in result:
# 	print(f'=== [{r.key.data}] ===')
# 	# print(r.value.data)
# 	for l in r.value.data:
# 		# print(type(l))
# 		if type(l) is JsonValue:
# 			print(f'\t- {l.data}')
# 		elif type(l) is Json:



# result = Parser(
# 	raw='''{ "its key" : "hi", "sec": 2}'''
# 	).parse()
# print('result: ', vars(result[0]))

