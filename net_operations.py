import requests # Biblioteka do wysyłania zapytań HTTP
import json # Biblioteka do odczytania potwierzenia w formacie json

# Deklaracja funkcji zapytania HTTP
def send_request(*args, **kwargs):
   response = requests.get(*args, **kwargs)
   json_response = json.loads(response.text)
   return