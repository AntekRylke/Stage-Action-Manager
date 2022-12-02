# Import bibliotek ogólnego przeznaczenia
import json
import datetime
import csv
# Import bibliotek do wykonywania zapytań HTTP
import webbrowser
import requests
# Import bibliotek do wystawienia serwera HTTP
from flask import Flask, render_template, request, redirect

# Deklaracja funkcji prostego zapytania HTTP
def send_request(*args, **kwargs):
   response = requests.get(*args, **kwargs)
   json_response = json.loads(response.text)
   #json_response = response.json()
   # Otwórz odebrany json w przeglądarce w celu debugowania
   #webbrowser.open_new_tab(*args)
   return

# Odczytaj do zmiennej (zagnieżdżony dict) dane urządzeń klienckich z pliku
def read_csv(path: str) -> dict:
   with open(path, mode='rt', newline='') as csv_file:
      return {key: valute for key, valute in enumerate(csv.DictReader(csv_file))}

# Dodaj nową linię do plikiu
#def append_csv(path: str, new_client: str[]):
#   with open(path, mode='a', newline='') as csv_file:
#      return {}



# Zapisz dane urządzeń klienckich w pliku
def write_csv(path: str, client_data):
   with open(path, mode='w', newline="") as csv_file:
      writer = csv.DictWriter(csv_file, fieldnames=client_data[1].keys())
      writer.writeheader()
      for row in client_data:
         writer.writerow(client_data[row])
      
client_data = (read_csv('client_data.csv'))
write_csv("client_data.csv", client_data)
#print(client_data[0]["type"])
#print(client_data[1].keys())
##print(len(client_data))

# Inicjalizacja serwera
server = Flask(__name__)

# Obsługa strony głównej
@server.route('/', methods=['GET', 'POST'])
def index():
   now = datetime.datetime.now()
   timeString = now.strftime("%Y-%m-%d %H:%M")
   templateData = {
      'title' : 'Obsługa zdarzeń scenicznych',
      'client_data' : client_data,
      'time': timeString
      }
      
   if request.method == 'POST':
      if request.form.get('gotowy') == "Gotowy?":
         try:
            send_request("http://192.168.1.51/lcd", params={'params': 0})
         except:
            return "Błąd połączenia!", 502
      if request.form.get('akcja') == "Akcja!":
         try:
            send_request("http://192.168.1.51/lcd", params={'params': 1})
         except:
            return "Błąd połączenia!", 502
      if request.form.get('Dodaj nowego klienta') == "Dodaj nowego klienta":
         redirect('/newclient')
   return render_template('index.html', **templateData)

# Obsługa wprowadzania nowych urządzeń klienckich
@server.route('/newclient', methods=['GET', 'POST'])
def newclient():
   now = datetime.datetime.now()
   timeString = now.strftime("%Y-%m-%d %H:%M")
   client_number = len(client_data)
   templateData = {
      'title' : 'Dodawanie nowych urządzeń',
      'client_data' : client_data,
      'client_number' : client_number
      }

   newclient = []
   newclient.append("3")
   print(repr(client_number))
      
   if request.method == 'POST':
      if request.form.get('dodaj') == "Dodaj":
         # inicjalizacja zmiennej, przechowującej informacje o nowym urządzeniu klienckim
         newclient = []
         newclient.append("3")
         print(repr(client_number))
         #newclient.append(str(len(client_data)))
         #newclient("client_data.csv", )
         #client_data[]["ID"] = len(client_data)
         #client_data[len(client_data)]["name"] = request.form.get('name')
         #client_data[len(client_data)]["IP"] = request.form.get('IP_1') # POPRAWIĆ!!!
         #client_data[len(client_data)]["type"] = request.form.get('dropdown')
         print(newclient)
         write_csv("client_data.csv", client_data)
         pass
      
      redirect('/newclient')
   return render_template('newclient.html', **templateData)

if __name__ == "__main__":
   server.run(host='0.0.0.0', port=80, debug=True)

   # Wykonaj testowe połączenie z klientami
for row in client_data:
   try:
      send_request("http://" + client_data[row]["IP"] + "/lcd", params={'params': 2})
   except:
      print("Nie udalo sie nawiazac polaczenia z " + client_data[row]["name"] + " pod adresem " + client_data[row]["IP"])
      pass   
