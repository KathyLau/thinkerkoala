#import EB.Utils.security as security

from EB.CustomerInfo.Users import UsersService as us

c = us()


def f():
    return "Cool"


c.somf = f

print(c.somf())




def t1():

    pw = "booboo"
    h_pw = security.encode_password(pw)
    print("Hashed PW = ", h_pw)


def t2():

    h_pw = \
    b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwYXNzd29yZCI6ImJvb2JvbyJ9.GkmRQfk7KwQDhPKdO-JhNkc0fb54ZNhwu6-g1lYwZAg'

    result = security.check_password("booboo2", h_pw)
    print("Password check result = ", result)


#t1()
#t2()