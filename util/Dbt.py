import random

import requests

from model.Book import Book
from model.Chapter import Chapter
from model.Testament import Testament
from model.Verse import Verse
from model.Version import Version


def levenshtein_distance(a, b):
    """Return the Levenshtein edit distance between two strings *a* and *b*."""
    if a == b:
        return 0
    if len(a) < len(b):
        a, b = b, a
    if not a:
        return len(b)
    previous_row = range(len(b) + 1)
    for i, column1 in enumerate(a):
        current_row = [i + 1]
        for j, column2 in enumerate(b):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (column1 != column2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

class Dbt:
    base_url = "https://dbt.io";
    dbt_key = "e156ea7b4b70b7ffe7b7ca483715b3dc";
    dbt_version = "2"
    language = "FRN"
    retry_delay = 5000
    max_attemps = 3

    @staticmethod
    def book_equals(book_name1, book_name2):
        book_name1 = book_name1.replace("Iier ", "1")
        book_name1 = book_name1.replace("IIième ", "2")
        book_name1 = book_name1.replace("IIIième ", "3")

        book_name2 = book_name2.replace("Iier ", "1")
        book_name2 = book_name2.replace("IIième ", "2")
        book_name2 = book_name2.replace("IIIième ", "3")

        return book_name1.lower().strip() == book_name2.lower().strip()

    @staticmethod
    def get_request(url, attempt=0):
        try:
            return requests.get(url=url).json()
        except:
            if attempt < Dbt.max_attemps:
                return Dbt.get_request(url, attempt + 1)

        return None

    @staticmethod
    def get_api_url(path, params):
        url = "{}{}?v={}&key={}".format(Dbt.base_url, path, Dbt.dbt_version, Dbt.dbt_key)
        for key, value in params.items():
            url += "{}&{}={}".format(url, key, value)
        return url

    @staticmethod
    def get_osis_code():
        result = {}
        url = Dbt.get_api_url("/library/bookname", {"language_code": Dbt.language})
        data = Dbt.get_request(url)
        for item in data:
            for k, v in item.items():
                result[k] = v.replace("IIIième ", "3").replace("IIième ", "2").replace("Iier ", "1")

        return result

    @staticmethod
    def find_chapter(version, book, chapter_number):
        book = Dbt.normalize_book(book)
        bk = Dbt.find_book(version, book)
        return Chapter(bk, chapter_number)

    @staticmethod
    def find_book(vers, book_name):
        version = Dbt.find_version(vers)

        for t in version.testaments:
            url = Dbt.get_api_url("/library/book", {"dam_id": t.damn_id})

            books = Dbt.get_request(url)

            for book in books:
                if Dbt.book_equals(book['book_name'], book_name):
                    b = Book(t,
                             book['book_name'],
                             book['book_id'],
                             book['book_order'])
                    list_chapters = book['chapters'].split(',')
                    for c in list_chapters:
                        b.chapters.append(Chapter(b, c))

                    return b
        return None

    @staticmethod
    def find_version(version_param):
        url = Dbt.get_api_url("/library/volume", {"language_family_code": Dbt.language, "media": "text"})
        testaments = Dbt.get_request(url)
        version = None
        for testament in testaments:
            if version_param != testament["version_code"]:
                continue
            if version is None:
                version = Version(testament['version_name'], testament['version_code'])

            t = Testament(testament['volume_name'],
                          testament['dam_id'],
                          testament['collection_code'],
                          version)
            version.testaments.append(t)

        return version

    @staticmethod
    def get_neighbord(osis_codes, book_name):
        board = {}
        for osis_code in osis_codes:
            board[osis_code] = levenshtein_distance(osis_code, book_name)
        code = min(board, key=board.get)
        #
        if board[code] <= 3:
            return code
        else:
            return None

    @staticmethod
    def normalize_book(book):
        book = book.strip()
        osis_codes = Dbt.get_osis_code().values()

        find_code = False
        for osis_code in osis_codes:
            if Dbt.book_equals(osis_code, book):
                find_code = True

        if not find_code:
            old_book = book
            book = Dbt.get_neighbord(osis_codes, book)

        if book is None:
            print(
                "Book '{}' doesn't exist in OSIS Code list. Please get on this list : {}".format(old_book, osis_codes))
            return None
        return book

    @staticmethod
    def find_verse(version, book, chapter_number, verse_number):
        book = Dbt.normalize_book(book)
        if book is not None:
            ch = Dbt.find_chapter(version, book, chapter_number)
            url = Dbt.get_api_url("/text/verse", {
                "dam_id": ch.book.testament.damn_id,
                "book_id": ch.book.code,
                "chapter_id": ch.chapter_number,
                "verse_start": verse_number
            })

            verses = Dbt.get_request(url)
            for verse in verses:
                return Verse(ch,
                             verse['verse_id'],
                             verse['verse_text'].strip())

        return None

    @staticmethod
    def get_random_verse(version):
        version_obj = Version(version, version)
        testaments = version_obj.get_testaments()
        select_testament = random.choice(testaments)
        books = select_testament.get_books()
        select_book = random.choice(books)
        chapters = select_book.get_chapters()
        select_chapter = random.choice(chapters)
        verses = select_chapter.get_verses()
        select_verse = random.choice(verses)

        return select_verse
