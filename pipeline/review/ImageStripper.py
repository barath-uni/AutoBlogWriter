import urllib.request
from urllib3.util.url import parse_url
from os.path import splitext
from pathlib import Path

def get_ext(url):
    """Return the filename extension from url, or ''."""
    parsed = parse_url(url)
    print(parsed.path)
    file_name, ext = splitext(parsed.path)
    return ext
    # return ext  # or ext[1:] if you don't want the leading '.'

# The urlparse module (urllib.parse in Python 3) provides tools for working with URLs. Although it doesn't provide a way to extract the file extension from a URL, it's possible to do so by combining it with os.path.splitext:

def download_image(image_url, location):
    urllib.request.urlretrieve(image_url, Path(f"{location}{get_ext(image_url)}"))
    return get_ext(image_url)
# get_ext("https://m.media-amazon.com/images/I/51Po1SCgSGL._SX425_.jpg")
# download_image("https://m.media-amazon.com/images/I/51Po1SCgSGL._SX425_.jpg", Path("images/", "Symphony Ice Cube 27"))