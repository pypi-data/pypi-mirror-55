import getpass

def say_hello():
    username = getpass.getuser()
    print(f'Hello {username}, by Vedic !!!')

say_hello()