"""Insta485 development configuration."""

import pathlib

# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'

# Secret key for encrypting cookies
SECRET_KEY = b'\xfd\xbck/T:\x02\xd9\x0e\xd5Ct0S\x10\xa1\xfd\x9e\xe95\xa93\xa9$'
SESSION_COOKIE_NAME = 'login'

# File Upload to var/uploads/
SEARCH_ROOT = pathlib.Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = SEARCH_ROOT/'var'/'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# Database file is var/insta485.sqlite3
DATABASE_FILENAME = SEARCH_ROOT/'var'/'insta485.sqlite3'

SEARCH_INDEX_SEGMENT_API_URLS = [
    "http://localhost:9000/api/v1/hits/",
    "http://localhost:9001/api/v1/hits/",
    "http://localhost:9002/api/v1/hits/",
]
