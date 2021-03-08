# Books!

I made this script to scan in my books by ISBN and create a csv database of them sorted by some kind of unique ID that I haven't decided on yet.

## Using it

I run the following command to scan in a bunch of books and append them to my existing list:

```
source env/bin/activate.fish
pip install -r requirements.txt
python scan_books.py > output.csv
```
