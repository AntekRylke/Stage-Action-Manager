# Import biblioteki do wygenerowania losowego klucza sesji
import os

# Ustanowinie klucza sesji
SECRET_KEY = os.urandom(12).hex()
