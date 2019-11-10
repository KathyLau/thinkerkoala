import jwt

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