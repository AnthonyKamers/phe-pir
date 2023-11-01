from peewee import *

db = SqliteDatabase('db/search.db')


class Search(Model):
    result = IntegerField()

    class Meta:
        database = db


def create_table():
    db.connect()
    db.create_tables([Search])
    db.close()


def new_result(value):
    db.connect()
    result = Search(result=value)
    result.save()
    db.close()


def get_all():
    db.connect()
    searches = [search for search in Search.select()]
    db.close()

    return searches


def get_qtd():
    return Search.select().count()
