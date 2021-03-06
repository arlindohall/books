
import requests

class Book:
    def __init__(self):
        self.title = ''
        self.isbn = ''
        self.genre = ''
        self.categories = []
        self.lcn = ''

    def to_csv(self) -> str:
        category = ''
        if self.categories:
            category = self.categories[0]
        return ','.join([
            self.isbn,
            self.title,
            self.genre,
            category,
            self.lcn,
        ])

class BookClient:
    def __init__(self):
        self.protocol = 'https'

        self.google_address = 'www.googleapis.com'
        self.google_path = '/books/v1/volumes'

        self.lc_address = 'www.loc.gov'
        self.lc_path = '/search'

    def fetch_google(self, isbn):
        result = requests.get(
            f'{self.protocol}://{self.google_address}{self.google_path}?q={isbn}'
        ).json()

        book = Book()
        if not result['items']:
            return book
        else:
            best_match = result['items'][0]

        book.isbn = isbn
        # book.title = result['']
        return book

    def fetch_lc_class(self, isbn):
        result = requests.get(
            f'{self.protocol}://{self.lc_address}{self.lc_path}?fo=json&q={isbn}'
        ).json()

        return ''

def book_for_id(isbn):
    return BookClient().fetch_google(isbn)

id = input()
print(book_for_id(id).to_csv())