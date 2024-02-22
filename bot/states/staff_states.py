from aiogram.fsm.state import StatesGroup, State


class Content_add(StatesGroup):
    author_add = State()
    author_search = State()
    author_edit = State()
    genre_add = State()
    genre_search = State()
    genre_edit = State()
    klass_add = State()
    klass_search = State()
    klass_edit_name = State()
    klass_edit_parallel = State()
    student_add = State()
    student_search_by_fio = State()
    student_edit_fio = State()
    student_edit_klass = State()
    book_add = State()
    book_add2 = State()
    book_add3 = State()
    book_search = State()
    book_search_await_book_name = State()
    book_search_await_author = State()
    book_search_result = State()
    book_instance_count = State()
    await_books_qr_codes = State()
    qr_search = State()


