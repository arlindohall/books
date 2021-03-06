
import requests

def columns():
    return ','.join(
        'scanned_id',
        'isbn_13',
        'isbn_10',
        'gbooks_id',
        'title',
        'author',
        'category',
        'loc_number',
    )

class Book:
    def __init__(self, scanned_id):
        self.scanned_id = scanned_id
        self.isbn_13 = ''
        self.isbn_10 = ''
        self.gbooks_id = ''
        self.title = ''
        self.author = ''
        self.categories = []
        self.loc_number = ''

    def to_csv(self) -> str:
        category = ''
        if self.categories:
            category = self.categories[0]
        return ','.join([
            self.scanned_id,
            self.isbn_13,
            self.isbn_10,
            self.gbooks_id,
            self.title,
            self.author,
            category,
            self.loc_number,
        ])

class BookClient:
    def __init__(self):
        self.protocol = 'https'

        self.google_address = 'www.googleapis.com'
        self.google_path = '/books/v1/volumes'

        self.loc_address = 'www.loc.gov'
        self.loc_path = '/search'

    def fetch_google(self, scanned_id):
        result = requests.get(
            f'{self.protocol}://{self.google_address}{self.google_path}?q={scanned_id}'
        ).json()

        book = Book(scanned_id)
        if not result['items']:
            return book
        else:
            best_match = result['items'][0]

        book.isbn_13 = get_isbn13(best_match)
        book.isbn_10 = get_isbn10(best_match)
        book.gbooks_id = get_gbooks_id(best_match)
        book.title = get_title(best_match)
        book.author = get_author(best_match)
        book.categories = get_categories(best_match)

        return book

    def fetch_lc_class(self, scanned_id):
        result = requests.get(
            f'{self.protocol}://{self.loc_address}{self.loc_path}?fo=json&q={scanned_id}'
        ).json()

        return get_loc_classification(result)

def get_isbn13(google_result):
    def is_isbn_13(id_map):
        return id_map.get('type', '') == 'ISBN_13'
    v_inf = google_result.get('volumeInfo', {})
    ids = v_inf.get('industryIdentifiers', [])
    isbn = filter(is_isbn_13, ids)
    isbn = ids and ids.pop()
    print(isbn)
    isbn = isbn and isbn.get('identifier', '')

    return isbn

def get_isbn10(google_result):
    return ''

def get_gbooks_id(google_result):
    return ''

def get_title(google_result):
    return ''

def get_author(google_result):
    return ''

def get_categories(google_result):
    return ''

def get_loc_classification(loc_result):
    return ''

def book_for_id(isbn):
    book = BookClient().fetch_google(isbn)
    book.loc_number = BookClient().fetch_lc_class(isbn)
    return book

id = input()
print(book_for_id(id).to_csv())