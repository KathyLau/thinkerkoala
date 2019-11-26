import jwt
import hashlib
import json

from Context.Context import Context
from time import time

def hash_password(pwd):
    global _context
    h = jwt.encode(pwd, key=_context.get_context("JWT_SECRET"))
    return h

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

auth = {
    ("/api/user/<email>", "GET"),
    ("/api/user/<email>", "PUT"),
    ("/api/user/<email>", "DELETE"),
}

def authorize(url, method, token):
    key = (str(url), str(method))
    if key not in auth:
        return True
    try:
        info = jwt.decode(token.split(' ')[1].encode("utf-8"), key=_context.get_context("JWT_SECRET"))

        msg = info.get('msg', None)
        if msg is not None:
            return True

        role = info.get('role', None)
        if role is None:
            return False

        if key == ("/api/user/<email>", "PUT") \
                or key == ("/api/user/<email>", "DELETE"):
            return role == "admin"

        return role == "admin" or role == "student"
    except:
        return False

