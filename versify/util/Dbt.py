import random
import configparser
import requests
from requests import RequestException, ConnectTimeout, Timeout
from requests.exceptions import ProxyError, HTTPError

from versify.model.Book import Book
from versify.model.Chapter import Chapter
from versify.model.Testament import Testament
from versify.model.Verse import Verse
from versify.model.Version import Version


def get_config(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    return config


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

    def __init__(self, config_path):
        self.config = get_config(config_path)
        self.base_url = "https://dbt.io"
        self.dbt_version = "2"
        self.retry_delay = 5000
        self.max_attemps = 3
        self.language = self.config.get("dbt", "lang")
        self.dbt_key = self.config.get("dbt", "key")
        self.osis_codes = self.get_osis_code()

    @staticmethod
    def book_equals(book_name1, book_name2):
        book_name1 = book_name1.replace("IIIième ", "3").replace("IIième ", "2").replace("Iier ", "1")
        book_name2 = book_name2.replace("IIIième ", "3").replace("IIième ", "2").replace("Iier ", "1")

        return book_name1.lower().strip() == book_name2.lower().strip()

    def get_request(self, url, attempt=0):
        try:
            return requests.get(url=url).json()
        except (RequestException, HTTPError, ProxyError, Timeout, ConnectTimeout):
            if attempt < self.max_attemps:
                return self.get_request(url, attempt + 1)

        return None

    def get_api_url(self, path, params):
        url = "{}{}?v={}&key={}".format(self.base_url, path, self.dbt_version, self.dbt_key)
        for key, value in params.items():
            url += "{}&{}={}".format(url, key, value)
        return url

    def get_osis_code(self):
        result = {}
        url = self.get_api_url("/library/bookname", {"language_code": self.language})
        data = self.get_request(url)

        for item in data:
            for k, v in item.items():
                result[k] = v.replace("IIIième ", "3").replace("IIième ", "2").replace("Iier ", "1")

        return result.values()

    def find_chapter(self, version, book, chapter_number):
        book = self.normalize_book(book)
        bk = self.find_book(version, book)
        return Chapter(bk, chapter_number)

    def find_book(self, vers, book_name):
        version = self.find_version(vers)

        for t in version.testaments:
            url = self.get_api_url("/library/book", {"dam_id": t.damn_id})

            books = self.get_request(url)

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

    def find_version(self, version_param):
        url = self.get_api_url("/library/volume", {"language_family_code": self.language, "media": "text"})
        testaments = self.get_request(url)
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

    def get_neighbord(self, book_name):
        board = {}
        for osis_code in self.osis_codes:
            board[osis_code] = levenshtein_distance(osis_code, book_name)
        code = min(board, key=board.get)
        #
        if board[code] <= 3:
            return code
        else:
            return None

    def normalize_book(self, book):
        book = book.strip()

        find_code = False
        for osis_code in self.osis_codes:
            if Dbt.book_equals(osis_code, book):
                find_code = True

        if not find_code:
            old_book = book
            book = self.get_neighbord(book)

        if book is None:
            print("Book '{}' doesn't exist in OSIS Code list."
                  " Please get on this list : {}".format(old_book, self.osis_codes))
            return None
        return book

    def find_verse(self, version, book, chapter_number, verse_number):
        book = self.normalize_book(book)
        if book is not None:
            ch = self.find_chapter(version, book, chapter_number)
            url = self.get_api_url("/text/verse", {
                "dam_id": ch.book.testament.damn_id,
                "book_id": ch.book.code,
                "chapter_id": ch.chapter_number,
                "verse_start": verse_number
            })

            verses = self.get_request(url)
            for verse in verses:
                return Verse(ch,
                             verse['verse_id'],
                             verse['verse_text'].strip())

        return None

    def get_random_verse(self, version):
        version_obj = Version(version, version)
        testaments = version_obj.get_testaments(self)
        select_testament = random.choice(testaments)
        books = select_testament.get_books(self)
        select_book = random.choice(books)
        chapters = select_book.get_chapters()
        select_chapter = random.choice(chapters)
        verses = select_chapter.get_verses(self)
        select_verse = random.choice(verses)

        return select_verse
