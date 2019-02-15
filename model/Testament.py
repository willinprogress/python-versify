import util
from model.Book import Book
from model.Chapter import Chapter


class Testament:
    def __init__(self, name, damn_id, type, version):
        self.name = name
        self.damn_id = damn_id
        self.type = type
        self.version = version

    def __repr__(self) -> str:
        return super().__repr__()


    def get_books(self):
        book_list = []
        url = util.Dbt.Dbt.get_api_url("/library/book", {"dam_id": self.damn_id})
        books = util.Dbt.Dbt.get_request(url)

        for book in books:
            b = Book(self,
                     book['book_name'],
                     book['book_id'],
                     book['book_order'])
            list_chapters = book['chapters'].split(',')
            for c in list_chapters:
                b.chapters.append(Chapter(b, c))
            book_list.append(b)

        return book_list