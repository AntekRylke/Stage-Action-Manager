import csv # Obsługa plików CSV
import re # Obsługa wyrażeń regularnych
import socket # Do odczytu lokalnego adresu IP 

# Ustalenie nazw parametrów identyfikujących urządzenia klienckie
client_fieldnames = ['ID', 'IP', 'name', 'type']

# Funkcje sprawdzające poprawność parametrów klienta
def check_client(ip: str, name: str, type: str):
   if not(check_client_ip(ip) and not
   check_client_name(name) and not check_client_type(type)):
      return "Błąd w danych nowego klienta!"
   else:
      return False

def check_client_name(name: str):
   if name == "":
      return "Nazwa klienta nie może być pusta"
   client_data = read_csv("client_data.csv")
   for row in client_data:
      if name in client_data[row].values():
         return "Nazwa klienta istnieje już w bazie"
      else:
         continue
   return False

def check_client_ip(ip: str):
   # Wyrażenie regularne do którego przyrównujemy adres IP
   reg = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
   if(re.search(reg, ip)):
      pass # Przechodzimy do sprawdzenia, czy adres się nie dubluje z innym klientem w bazie
   else:
      return "Wprowadzony adres IP jest nieprawidłowy"
   client_data = read_csv("client_data.csv")
   for row in client_data:
      if ip in client_data[row].values():
         return "Wprowadzony adres IP istnieje już w bazie, wybierz inny"
      else:
         continue 
   # Sprawdzamy, czy wprowadzony adres IP pokrywa się z adresem serwera
   s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   s.connect(("8.8.8.8", 80))
   if (ip == s.getsockname()[0]):
      s.close
      return "Wprowadzony adres IP jest identyczny z adresem serwera, wybierz inny"
   else:
      s.close
      return False

def check_client_type(type: str):
   if(type == "Sygnalizator") or (type == "Elektrozamek") or (type == "Przekazniki"):
      return False
   else:
      return "Typ klienta jest nieprawidłowy"

# Odczytaj do zmiennej (zagnieżdżony dict) dane urządzeń klienckich z pliku
def read_csv(path: str) -> dict:
   with open(path, mode='r', newline='') as csv_file:
      return {key: valute for key, valute in enumerate(csv.DictReader(csv_file))}

# Skasuj linię z pliku
def delete_csv(path: str, row_to_delete: int):
   client_data = read_csv(path)
   with open(path, mode='w', newline="") as csv_file:
      writer = csv.DictWriter(csv_file, fieldnames=client_fieldnames)
      writer.writeheader()
      for row in client_data:
         if row != row_to_delete:
            writer.writerow(client_data[row])

# Zaktualizuj ID
def update_id(path):
   client_data = read_csv(path)
   for row in client_data:
      client_data[row]["ID"] = row
   write_csv(path, client_data)

# Dodaj nową linię do pliku
def append_csv(path: str, new_client):
   client_data = read_csv(path)
   client_data[len(client_data)] = dict(zip(client_fieldnames, new_client))
   write_csv(path, client_data)

# Zapisz dane urządzeń klienckich w pliku
def write_csv(path: str, client_data):
   with open(path, mode='w', newline="") as csv_file:
      writer = csv.DictWriter(csv_file, fieldnames=client_fieldnames)
      writer.writeheader()
      for row in client_data:
         writer.writerow(client_data[row])
