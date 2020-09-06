from string_converter import StringConverter

assert(10000 == StringConverter('10000').convert())
assert(1.5 == StringConverter('1.5').convert())
assert(-30.1 == StringConverter('-30.1').convert())
assert(-3000 == StringConverter('-3000').convert() == int("-3000"))