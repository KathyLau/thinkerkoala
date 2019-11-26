from abc import ABC, abstractmethod
from Context.Context import Context
from DataAccess.DataObject import UsersRDB as UsersRDB
from werkzeug.security import generate_password_hash, check_password_hash

# The base classes would not be IN the project. They would be in a separate included package.
# They would also do some things.

class ServiceException(Exception):

    unknown_error   =   9001
    missing_field   =   9002
    bad_data        =   9003

    def __init__(self, code=unknown_error, msg="Oh Dear!"):
        self.code = code
        self.msg = msg


class BaseService():

    missing_field   =   2001

    def __init__(self):
        pass


class UsersService(BaseService):

    required_create_fields = ['last_name', 'first_name', 'email', 'password']

    def __init__(self, ctx=None):

        if ctx is None:
            ctx = Context.get_default_context()

        self._ctx = ctx

    @classmethod
    def hash_password(cls, user_info):

        passwd = ''

        for field in UsersService.required_create_fields:
            val = user_info.get(field, None)
            if v is None:
                raise ServiceException(ServiceException.missing_field,
                                       "Missing field = " + field)

            if field == 'password':
               passwd = generate_password_hash(val)

        user_info['password'] = passwd

        return user_info

    def check_hash_password(cls, user_info, user_info_db):

        checked = False

        for field in UsersService.required_create_fields:
            val = user_info.get(field, None)
            val_db = user_info_db.get(field, None)
            if val_db is None:
                raise ServiceException(ServiceException.missing_field,
                                       "Missing field = " + field)

            if field == 'password':
               checked = check_password_hash(val_db, user_info['password'])

        return checked

    @classmethod
    def get_by_email(cls, email):

        result = UsersRDB.get_by_email(email)
        return result

    @classmethod
    def create_user(cls, user_info):

        for f in UsersService.required_create_fields:
            v = user_info.get(f, None)
            if v is None:
                raise ServiceException(ServiceException.missing_field,
                                       "Missing field = " + f)

            if f == 'email':
                if v.find('@') == -1:
                    raise ServiceException(ServiceException.bad_data,
                           "Email looks invalid: " + v)

        result = UsersRDB.create_user(user_info=user_info)

        return result

    @classmethod
    def update_user(self, email, new_values):
        result = UsersRDB.update_user(email, new_values)
        return result

    @classmethod
    def delete_by_email(cls, email):
        return UsersRDB.update_user(email=email, new_values={"status": "DELETED"})
