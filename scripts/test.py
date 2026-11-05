s = "stri:val"

key, sep, value = s.partition("_")

if not sep:
    print(key, value)
else:
    print(key, sep, value)

print(value)