#   Copyright (C) 2018  Jacopo Cascioli
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.
# -*- coding: utf-8 -*-
from peewee import (IntegerField, IntegrityError, Model, SQL, SqliteDatabase)

from playhouse import db_url
from playhouse.pool import PooledPostgresqlExtDatabase as PooledPostrgres

from .Database import db


class Base(Model):

    __slots__ = ()

    conversions = {
        'AutoField': 'number',
        'BigIntegerField': 'number',
        'BooleanField': 'number',
        'CharField': 'text',
        'DateField': 'date',
        'DateTimeField': 'datetime',
        'DecimalField': 'number',
        'DoubleField': 'number',
        'FloatField': 'number',
        'ForeignKeyField': 'number',
        'IntegerField': 'number',
        'TextField': 'text',
        'UUIDField': 'text'
    }

    class Meta:
        database = db

    @classmethod
    def get_columns(cls):
        """
        Produces a list of columns for the current model.
        """
        columns = []
        for name, column in cls._meta.fields.items():
            column_type = cls.conversions[column.__class__.__name__]
            columns.append({'name': name, 'type': column_type})
        return columns

    @staticmethod
    def db_instance(url, connections, timeout, **kwargs):
        """
        Create the correct database instance from the url
        """
        dictionary = db_url.parse(url)
        name = dictionary.pop('database')
        if url.startswith('postgres'):
            return PooledPostrgres(name, max_connections=connections,
                                   stale_timeout=timeout, **dictionary)
        return SqliteDatabase(name, **kwargs)

    @classmethod
    def init_db(cls, url, connections, timeout, **kwargs):
        """
        Initialize the database with the instance
        """
        db.initialize(cls.db_instance(url, connections, timeout, **kwargs))

    @classmethod
    def filter(cls, key, value, operator):
        """
        Adds a filter to the current query
        """
        column = getattr(cls, key)
        if isinstance(value, list):
            return cls.q.where(column.in_(value))
        if operator == '!':
            return cls.q.where(column != value)
        elif operator == '>':
            return cls.q.where(column > value)
        elif operator == '<':
            return cls.q.where(column < value)
        elif operator == '~':
            return cls.q.where(column.startswith(value))
        return cls.q.where(column == value)

    @staticmethod
    def cast(value):
        if value == 'true':
            return True
        elif value == 'false':
            return False
        elif value == 'null':
            return None
        return value

    @classmethod
    def query(cls, key, value):
        """
        Builds a select query
        """
        if hasattr(cls, key) is False:
            return None
        operator = None
        if value[0] in ['!', '>', '<', '~']:
            operator = value[0]
            value = value[1:]
        cls.q = cls.filter(key, cls.cast(value), operator)

    @classmethod
    def write(cls, **kwargs):
        try:
            with db.atomic():
                return cls.create(**kwargs)
        except IntegrityError:
            return None
        except ValueError:
            return None

    def update_item(self, data):
        for key, value in data.items():
            setattr(self, key, value)
        return self.save()

    def edit(self, data):
        try:
            with db.atomic():
                return self.update_item(data)
        except IntegrityError:
            return None

    group = IntegerField(default=1, constraints=[SQL('DEFAULT 1')])
    owner_permission = IntegerField(default=3, constraints=[SQL('DEFAULT 3')])
    group_permission = IntegerField(default=0, constraints=[SQL('DEFAULT 0')])
    others_permission = IntegerField(default=0, constraints=[SQL('DEFAULT 0')])
