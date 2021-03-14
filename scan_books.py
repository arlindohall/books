
import json
import requests
import sys

from properties import get_title

OUTPUT_FILE = 'content/blobs.txt'

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
            )

            try:
                result = result.json()
            except json.decoder.JSONDecodeError:
                result = {}

            result = result.get('items', [])
            if not result:
                return {}
            else:
                return result[0]

        return self.__fetch_safe(go, self.google_host)

    def fetch_loc_class(self, scanned_id):
        def go():
            result = requests.get(
                f'{self.protocol}://{self.loc_host}{self.loc_path}?all=true&fo=json&q={scanned_id}'
            )

            try:
                result = result.json()
            except json.decoder.JSONDecodeError:
                result = {}

            return result

        return self.__fetch_safe(go, self.loc_host)

def produce_book_blob(scan):
    google_result = BookClient().fetch_google(scan)
    loc_result = BookClient().fetch_loc_class(scan)

    return {
        'scanned-id': scan,
        'google': google_result,
        'loc': loc_result,
    }

def read_all_blobs():
    with open(OUTPUT_FILE, 'r') as blobs:
        lines = blobs.readlines()
        return [json.loads(s) for s in lines]

def complete(content):
    with open(OUTPUT_FILE, 'w') as blobs:
        lines = [json.dumps(c) + '\n' for c in content]
        blobs.writelines(lines)

blobs = read_all_blobs()
ids = [blob.get('scanned-id') for blob in blobs]

identifier = 'placeholder'
while identifier:
    try:
        identifier = input()
    except EOFError:
        complete(blobs)
        sys.stderr.flush()
        exit(0)

    if identifier in ids:
        sys.stderr.write(f'Already found identifier in blobs file id={identifier}\n')
        continue
    else:
        book_blob = produce_book_blob(identifier)
        blobs.append(book_blob)
        ids.append(identifier)
        sys.stderr.write(f'Wrote blob for book ({get_title(book_blob["google"])})\n')