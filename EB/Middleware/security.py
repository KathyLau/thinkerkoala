import jwt
from Context.Context import Context
from time import time

_context = Context()


def hash_password(pwd):
    global _context
    h = jwt.encode(pwd, key=_context.get_context("JWT_SECRET"))
    h = str(h)
    return h

'''
def generate_token(uni):
    token = {
        "uni": uni,
        "timestamp": time()
    }
    if uni == 'dff9':
        token['role'] = 'admin'
    else:
        token['role'] = 'student'
    h = jwt.encode(token, key=_context.get_context("JWT_SECRET"))

    return h
'''


def generate_token(info):
    info["timestamp"] = time()
    email = info["email"]

    if email == "dff9@columbia.edu":
        info["role"] = "admin"
    else:
        info["role"] = "student"

    info["created"] = str(info["created"])

    h = jwt.encode(info, key=_context.get_context("JWT_SECRET"))
    h = str(h)
    return h


def authorize(url, method, path_params, token):
    #have to check if this is a protected method
    #based on the url, the verb, and the identity, decide whether that meets the rules
    #you can hardcode. if this, then that

    #check if the header exists
    #not all methods require authentication
    #if this is the url, them go check if the email is correct, otherwise don't worry about it
    #the only protected url is customerinfo/email
    #url = /api/customer_info
    #path = {"email": "dff9@columbia.edu"}

    if url:

        if url != "api/users/*" or method == "GET":
            return True
        if url == "api/users/*" and path_params["email"] == "dff9@columbia.edu":
            info = jwt.decode(token.split(' ')[1].encode("utf-8"), key = _context.get_context("JWT_SECRET"))
            # lambda can do anything
            msg = info.get('msg', None)
            if msg is not None and msg == "Lambda says hi":
                return True

            role = info.get('role', None)
            if role is None:
                return False
            if url != "api/users/*" and (method == "PUT" or method == "DELETE"):
                return role == "admin"
            return role == "admin" or role == "student"

