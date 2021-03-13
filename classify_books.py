
import json
import sys

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
        self.gbooks_href = get_gbooks_href(google_result)
        self.title = get_title(google_result)
        self.subtitle = get_subtitle(google_result)
        self.all_authors = get_authors(google_result)
        self.categories = get_categories(google_result)

        self.set_shelf_id()

    def set_loc_props(self, loc_result):
        self.loc_number = get_loc_number(loc_result)
        self.loc_href = get_loc_href(loc_result)

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


def get_isbn(google_result, matcher):
    v_inf = google_result.get('volumeInfo', {})
    ids = v_inf.get('industryIdentifiers', [])
    isbn = filter(matcher, ids)
    isbn = ids and ids.pop()
    isbn = isbn and isbn.get('identifier', '')

    return isbn

def get_isbn_13(google_result):
    def is_isbn_13(id_map):
        return id_map.get('type', '') == 'ISBN_13'

    return get_isbn(google_result, is_isbn_13)

def get_isbn_10(google_result):
    def is_isbn_10(id_map):
        return id_map.get('type', '') == 'ISBN_10'

    return get_isbn(google_result, is_isbn_10)

def get_gbooks_id(google_result):
    return google_result.get('id', '')

def get_gbooks_href(google_result):
    return google_result.get('selfLink', '')

def get_title(google_result):
    v_inf = google_result.get('volumeInfo', {})
    return v_inf.get('title', '')

def get_subtitle(google_result):
    v_inf = google_result.get('volumeInfo', {})
    return v_inf.get('subtitle', '')

def get_authors(google_result):
    v_inf = google_result.get('volumeInfo', {})
    return v_inf.get('authors', [])

def get_categories(google_result):
    v_inf = google_result.get('volumeInfo', {})
    return v_inf.get('categories', [])

def get_loc_number(loc_result):
    res = loc_result.get('results', [])
    if not res:
        return ''
    else:
        res = res[0]
    return res.get('shelf_id')

def get_loc_href(loc_result):
    def deep_get_values(d):
        res = []
        for value in d.values():
            if isinstance(value, dict):
                res.extend(deep_get_values(value))
            else:
                res.append(value)
        return res

    aka = loc_result.get('aka', [])
    if aka:
        return aka[0]

    values = deep_get_values(loc_result)
    for value in values:
        s = str(value)
        if s.startswith('http') and ('loc.gov' in s):
            return s

    return ''

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
        sys.stderr.flush()
        exit(0)
    blob = json.loads(line)
    book = to_book(blob)
    csv = book.to_csv()
    print(csv)
    sys.stderr.write(f'{csv}\n')
