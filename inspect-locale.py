import locale

print(locale.getlocale())
print(locale.setlocale(locale.LC_ALL, "C"))
print(repr(locale.strxfrm("A")))
print(repr(locale.strxfrm("a")))
print(repr(locale.strxfrm("Apple")))
print(repr(locale.strxfrm("apple")))
print(locale.setlocale(locale.LC_ALL, "en_US.UTF-8"))
print(repr(locale.strxfrm("A")))
print(repr(locale.strxfrm("a")))
print(repr(locale.strxfrm("Apple")))
print(repr(locale.strxfrm("apple")))