
import requests

class Book:
    def __init__(self):
        self.title = None
        self.isbn = None
        self.genre = None
        self.categories = []
        self.lcn = None

    def to_csv(self) -> str:
        return ','.join([
            self.isbn,
            self.title,
            self.genre,
            self.categories[0],
            self.lcn,
        ])

class BookClient:
    def __init__(self):
        self.protocol = 'https'
        self.address = 'www.googleapis.com'
        self.path = '/books/v1/volumes'
    def fetch(self, isbn):
        return requests.get(
            f'{self.protocol}://{self.address}{self.path}?q={isbn}'
        )

def book_for_id(isbn):
    return BookClient().fetch(isbn)

id = '0465026567'
print(book_for_id(id))