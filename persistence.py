import logging

from sqlite_orm.database import Database
from sqlite_orm.field import BooleanField, IntegerField, TextField
from sqlite_orm.table import BaseTable


class ImageRecord(BaseTable):
    __table_name__ = 'images'

    md5 = TextField(primary_key=True)
    name = TextField(not_null=True)
