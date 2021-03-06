import DataAccess.DataAdaptor as data_adaptor
from abc import ABC, abstractmethod
import pymysql.err

database = "e6156"

class DataException(Exception):

    unknown_error   =   1001
    duplicate_key   =   1002

    def __init__(self, code=unknown_error, msg="Something awful happened."):
        self.code = code
        self.msg = msg

class BaseDataObject(ABC):

    def __init__(self):
        pass

    @classmethod
    @abstractmethod
    def create_instance(cls, data):
        pass


class UsersRDB(BaseDataObject):

    def __init__(self, ctx):
        super().__init__()

        self._ctx = ctx

    @classmethod
    def get_by_email(cls, email):

        sql = "select * from " + database + ".users where email=%s and status <> 'DELETED'"
        res, data = data_adaptor.run_q(sql=sql, args=(email), fetch=True)
        if data is not None and len(data) > 0:
            result = data[0]
        else:
            result = None

        return result

    '''
    @classmethod
    def delete_by_email(cls, email):

        sql = "delete from thinkerkoala.users where email=%s"
        res, data = data_adaptor.run_q(sql=sql, args=(email), fetch=True)
        return res
    '''

    @classmethod
    def get_users(cls, params, fields):
        sql, args = data_adaptor.create_select(table_name="users", template=params, fields=fields)
        res, data = data_adaptor.run_q(sql, args)
        if data is not None and len(data) > 0:
            return data
        else:
            return None


    db_connect_info = {"host": "koala2.cfgzz918oyef.us-east-1.rds.amazonaws.com", "user": "root", "password": "dbuserdbuser", "db": database,
                       "port": 3306}

    @classmethod
    def create_user(cls, user_info):

        result = None

        try:
            sql, args = data_adaptor.create_insert(table_name="users", row=user_info)
            res, data = data_adaptor.run_q(sql, args)
            if res != 1:
                result = None
            else:
                result = user_info['id']
        except pymysql.err.IntegrityError as ie:
            if ie.args[0] == 1062:
                raise (DataException(DataException.duplicate_key))
            else:
                raise DataException()
        except Exception as e:
            raise DataException()

        return result

    @classmethod
    def update_user(cls, email, new_values):
        result = None

        # this makes sure we don't update a value marked as 'DELETED'. get_by_email()
        user_info = UsersRDB.get_by_email(email)
        if not user_info:
            return "No such user exists, homie."

        try:
            sql, args = data_adaptor.create_update(table_name="users", new_values=new_values, template={"email": email})
            res, data = data_adaptor.run_q(sql, args)
            if res != 1:
                result = None
            else:
                result = user_info['id']
        except pymysql.err.IntegrityError as ie:
            if ie.args[0] == 1062:
                raise (DataException(DataException.duplicate_key))
            else:
                raise DataException()
        except Exception as e:
            raise DataException()

        return result


