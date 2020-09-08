from json_parser import *


assert(
	Parser(raw='''{ "num" : -500 }''').parse() == {'num': -500})

assert(
	Parser(raw='''{"hello" : "world" }''').parse() == {'hello': 'world'})

assert(
	Parser(raw='''{ "bool" : true}''').parse() == {'bool': True})

assert(
	Parser(raw='''{ "bool" : false }''').parse() == {'bool': False})

assert(
	Parser(raw='''{ "list" : [0, "zero", true] }''').parse() == {'list': [0, 'zero', True]})

assert(
	Parser(raw='''{ "dict" : {"d2": 2} }''').parse() == {'dict': {'d2': 2}})

assert(
	Parser(raw='''{ "one" : 1, "two": 2 }''').parse() == {'one': 1, 'two': 2})

assert(
	Parser(raw='''{ "www" : [0, {"kkk": true}, {"haha": {"h1": "haha"}}] }''').parse() == {"www": [0, {"kkk": True}, {"haha": {"h1": "haha"}}] })