
import json
import requests
import sys

from properties import get_title

class BookClient:
    def __init__(self):
        self.protocol = 'https'

        self.google_host = 'www.googleapis.com'
        self.google_path = '/books/v1/volumes'

        self.loc_host = 'www.loc.gov'
        self.loc_path = '/search'

    def __fetch_safe(self, method, host):
        try:
            sys.stderr.write(f'Fetching data from host={host}\n')
            return method()
        except requests.RequestException:
            sys.stderr.write(f'Exception while fetching data from host={host}')

    def fetch_google(self, scanned_id):
        def go():
            result = requests.get(
                f'{self.protocol}://{self.google_host}{self.google_path}?q={scanned_id}'
            ).json()

            if 'items' not in result or not result['items']:
                return {}
            else:
                return result['items'][0]

        return self.__fetch_safe(go, self.google_host)

    def fetch_loc_class(self, scanned_id):
        def go():
            return requests.get(
                f'{self.protocol}://{self.loc_host}{self.loc_path}?all=true&fo=json&q={scanned_id}'
            ).json()

        return self.__fetch_safe(go, self.loc_host)

def produce_book_blob(scan):
    google_result = BookClient().fetch_google(scan)
    loc_result = BookClient().fetch_loc_class(scan)

    return {
        'scanned-id': scan,
        'google': google_result,
        'loc': loc_result,
    }

identifier = 'placeholder'
while identifier:
    try:
        identifier = input()
    except EOFError:
        sys.stderr.flush()
        exit(0)
    book_blob = produce_book_blob(identifier)
    print(json.dumps(book_blob))
    sys.stderr.write(f'Wrote blob for book ({get_title(book_blob["google"])})\n')