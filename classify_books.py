
import json

from properties import (
    get_isbn,
    get_isbn_13,
    get_isbn_10,
    get_gbooks_id,
    get_gbooks_href,
    get_title,
    get_subtitle,
    get_authors,
    get_categories,
    get_loc_number,
    get_loc_href,
)

def columns():
    return ','.join([
        'scanned_id',
        'shelf_id',
        'isbn_13',
        'isbn_10',
        'gbooks_id',
        'gbooks_href',
        'title',
        'subtitle',
        'author',
        'all_authors',
        'category',
        'all_categories',
        'loc_number',
        'loc_href',
    ])

class Book:
    def __init__(self, scanned_id):
        self.scanned_id = scanned_id
        self.shelf_id = ''
        self.isbn_13 = ''
        self.isbn_10 = ''
        self.gbooks_id = ''
        self.gbooks_href = ''
        self.title = ''
        self.subtitle = ''
        self.all_authors = []
        self.categories = []
        self.loc_number = ''
        self.loc_href = ''

    def set_shelf_id(self):
        self.category = ''
        if self.categories:
            self.category = self.categories[0]

        self.author = ''
        if self.all_authors:
            self.author = self.all_authors[0]

        id_parts = [
            self.category.replace(' ', '')[:4],
            self.author.replace(' ', '')[:6],
            self.title.replace(' ', '')[:10],
            self.scanned_id,
        ]
        self.shelf_id = '-'.join(id_parts)

    def set_google_props(self, google_result):
        self.isbn_13 = get_isbn_13(google_result)
        self.isbn_10 = get_isbn_10(google_result)
        self.gbooks_id = get_gbooks_id(google_result)
        self.gbooks_href = get_gbooks_href(self.scanned_id)
        self.title = get_title(google_result)
        self.subtitle = get_subtitle(google_result)
        self.all_authors = get_authors(google_result)
        self.categories = get_categories(google_result)

        self.set_shelf_id()

    def set_loc_props(self, loc_result):
        self.loc_number = get_loc_number(loc_result)
        self.loc_href = get_loc_href(self.scanned_id)

    def to_csv(self) -> str:
        def escape(string):
            # Escape all double quotes as quad quotes and wrap in double quotes
            return '"' + string.replace("\"", "\"\"") + '"'

        if not self.shelf_id:
            self.set_shelf_id()

        fields = [
            self.scanned_id,
            self.shelf_id,
            self.isbn_13,
            self.isbn_10,
            self.gbooks_id,
            self.gbooks_href,
            self.title,
            self.subtitle,
            self.author,
            ';'.join(self.all_authors),
            self.category,
            ';'.join(self.categories),
            self.loc_number,
            self.loc_href,
        ]
        return ','.join(map(escape, fields))


def to_book(blob):
    google_result = blob['google']
    loc_result = blob['loc']

    book = Book(blob['scanned-id'])
    book.set_google_props(google_result)
    book.set_loc_props(loc_result)

    return book

print(columns())

line = 'placeholder'
while line:
    try:
        line = input()
    except EOFError:
        exit(0)
    blob = json.loads(line)
    book = to_book(blob)
    csv = book.to_csv()
    print(csv)
