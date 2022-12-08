# Import bibliotek ogólnego przeznaczenia
import json
import datetime

# Import bibliotek do wykonywania zapytań HTTP
import webbrowser
import requests
# Import bibliotek do wystawienia serwera HTTP
from flask import Flask, render_template, request, redirect, flash
# Import biblioteki z własnymi funkcjami operującymi na plikach .CSV
from csv_operations import *

# Deklaracja funkcji zapytania HTTP
def send_request(*args, **kwargs):
   response = requests.get(*args, **kwargs)
   json_response = json.loads(response.text)
   # Otwórz odebrany json w przeglądarce w celu debugowania
   #webbrowser.open_new_tab(*args)
   return

# Pobranie danych urządzeń klienckich z pliku
client_data = read_csv('client_data.csv')

# Inicjalizacja serwera
server = Flask(__name__)
server.config.from_pyfile('server_config.py')

# Obsługa strony głównej
@server.route('/', methods=['GET', 'POST'])
def index():
   now = datetime.datetime.now()
   timeString = now.strftime("%Y-%m-%d %H:%M")
   client_data = read_csv("client_data.csv")
   templateData = {
      'title' : 'Obsługa zdarzeń scenicznych',
      'client_data' : client_data,
      'time': timeString
      }

   if request.method == 'POST':
      if request.form.get('Dodaj lub skasuj klienta') == "dodaj lub skasuj klienta":
         redirect('/newclient')
   return render_template('index.html', **templateData)

@server.route('/akcja', methods=['GET', 'POST'])
def akcja():
   ip = request.args.get('ip')
   try:
      send_request("http://" + ip + "/lcd", params={'params': 1})
   except:
      return redirect('/connection_error')
   return index()

@server.route('/gotowy', methods=['GET', 'POST'])
def gotowy():
   ip = request.args.get('ip')
   try:
      send_request("http://" + ip + "/lcd", params={'params': 0})
   except:
      return redirect('/connection_error')
   return index()

# Błąd połączenia z urządzeniem klienckim
@server.route('/connection_error', methods=['GET', 'POST'])
def connection_error():
   templateData = {
      'title' : 'Obsługa zdarzeń scenicznych'}
   return render_template('connection_error.html', **templateData)

# Usuń urządzenie
@server.route('/deleteclient', methods=['POST'])
def deleteclient():
   id = int(request.args.get('id'))
   delete_csv("client_data.csv", id)
   update_id("client_data.csv")
   client_data = read_csv('client_data.csv')
   return redirect("/newclient")

# Obsługa wprowadzania nowych urządzeń klienckich
@server.route('/newclient', methods=['GET', 'POST'])
def newclient():
   now = datetime.datetime.utcnow()
   client_data = read_csv('client_data.csv')
   timeString = now.strftime("%Y-%m-%d %H:%M")
   client_number = len(client_data)
   templateData = {
      'title' : 'Dodawanie nowych urządzeń',
      'client_data' : client_data,
      'client_number' : client_number
      }

   if request.method == 'POST':
      if request.form.get('dodaj') == "Dodaj":
         # Przechowanie informacji z pól formularza
         form_data = request.form
         # Utworzenie zmiennej, przechowującej informacje o nowym urządzeniu klienckim
         try:
            newclient = [
               str(len(client_data)),
               '.'.join([request.form.get(f'IP_{num + 1}') for num in range(4)]),
               request.form.get('name'),
               request.form.get('type')
            ]
         except:
            return form_data, 500
         # Sprawdź poprawność wprowadzonych danych
         # UWAGA! funkcje check_client zwracają:
         # False, gdy wartości są prawidłowe,
         # String, gdy wykryto błąd
         # Jeśli dane są niepoprawne, wyświetl wiadomość
         if message := check_client_ip(newclient[1]): # := przypisz do zmiennej
            flash(message)
         if message := check_client_name(newclient[2]):
            flash(message)
         if message := check_client_type(newclient[3]):
            flash(message)
         else:
             append_csv('client_data.csv', newclient)
         return redirect("/newclient")

   return render_template('newclient.html', **templateData)

if __name__ == "__main__":
   server.run(host='0.0.0.0', port=80, debug=True)
   client_data = read_csv('client_data.csv')

   # Wykonaj testowe połączenie z klientami
   for row in client_data:
      try:
         send_request(
             "http://" + client_data[row]["IP"] + "/lcd", params={'params': 2})
      except:
         print("Nie udalo sie nawiazac polaczenia z " +
               client_data[row]["name"] + " pod adresem " + client_data[row]["IP"])
