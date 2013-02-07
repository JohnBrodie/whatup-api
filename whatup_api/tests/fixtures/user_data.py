"""Fixtures for User model"""
from datetime import datetime
from fixture import DataSet


class UserData(DataSet):

    class Default:
        created_at = datetime(2001, 10, 10)
        modified_at = datetime(2001, 10, 11)
        name = 'Ayush Sobti'
        alias = 'xbonez'
        bio = 'Little is known about Ayush. He is an enigma.'
        is_deleted = False
        email = 'enigma@ayush.me'
        openid = 'openidkey'

    class SpecifiesNone:
        name = 'John Doe'
        email = 'anita.hoare@gmail.com'
