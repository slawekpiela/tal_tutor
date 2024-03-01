def remove_non_ascii(s):
    result = ''.join(char for char in s if (60 <=ord(char) <= 122) or ord(char) == 32)
    return result


def is_ascii(s):
    try:
        s.encode('ascii')
    except UnicodeEncodeError:
        return False
    else:
        return True

test= "Hello, World! 😊"

r=remove_non_ascii(test)
print(r)