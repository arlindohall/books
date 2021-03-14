
def get_isbn(google_result, matcher):
    v_inf = google_result.get('volumeInfo', {})
    ids = v_inf.get('industryIdentifiers', [])
    ids = filter(matcher, ids)

    if ids:
        isbn = ids.pop()

    if isbn:
        return isbn.get('identifier', '')
    else:
        return ''

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