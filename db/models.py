from peewee import *
import datetime

from bot.dop_func import get_hex_string
from settings import admins

db = SqliteDatabase('library.db')


def db_init() -> None:
    db.connect()
    db.create_tables([Author, Genre, Parallel, Book, Book_info, Book_movement, Staff, Klass, Student], safe=True)
    if Parallel.select().count() == 0:
        for i in range(1, 12):
            Parallel.create(name=i)
        Parallel.create(name='Общая')


class Base(Model):
    class Meta:
        database = db


class Author(Base):
    fio = CharField()


class Genre(Base):
    name = CharField()


class Parallel(Base):
    name = CharField()


class Book_info(Base):
    author = ForeignKeyField(Author, backref='books')
    genre = ForeignKeyField(Genre, backref='books')
    name = CharField()
    parallel = ForeignKeyField(Parallel, backref='books')

    def count(self):
        # books_all = self.books.select().count()
        # books_free = self.books.select().where(Book.free == True).count()
        books_all = Book.select().where(Book.book == self).count()
        books_free = Book.select().where(Book.book == self, Book.free == True).count()
        return f'{books_free} из {books_all}'


class Staff(Base):
    fio = CharField()
    tg_id = CharField(null=True)


class Klass(Base):
    name = CharField()
    parallel = ForeignKeyField(Parallel, backref='klasses')


class Student(Base):
    fio = CharField()
    tg_id = CharField(default='')
    klass = ForeignKeyField(Klass, backref='students')
    invite_code = CharField(default=get_hex_string)


class Book(Base):
    book = ForeignKeyField(Book_info, backref="books")
    free = BooleanField(default=True)
    arrival_date = DateTimeField(default=datetime.datetime.now)


class Book_movement(Base):
    book = ForeignKeyField(Book, backref="books")
    student = ForeignKeyField(Student, backref="books")
    staff = ForeignKeyField(Staff, backref="books", null=True)
    issue_date = DateTimeField(default=datetime.datetime.now)
    is_return = BooleanField(default=False)
