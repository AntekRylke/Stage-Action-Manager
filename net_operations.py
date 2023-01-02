# Import bibliotek do komunikacji sieciowej
import requests
import socket
import json
import struct

# Deklaracja funkcji zapytania HTTP
def send_request(*args, **kwargs):
   response = requests.get(*args, **kwargs)
   json_response = json.loads(response.text)
   # Otwórz odebrany json w przeglądarce w celu debugowania
   #webbrowser.open_new_tab(*args)
   return

# Deklaracja funkcji konwertujących adres ip do i z int
def ip_to_int(ip):
  octets = ip.split('.')
  ip_int = int(octets[0]) << 24 | int(octets[1]) << 16 | int(octets[2]) << 8 | int(octets[3])
  return ip_int

def int_to_ip(i):
  # Wyciągnięcie oktetów z adresu f formie int
  octet1 = (i & 0xff000000) >> 24
  octet2 = (i & 0x00ff0000) >> 16
  octet3 = (i & 0x0000ff00) >> 8
  octet4 = i & 0x000000ff

# Połączenie oktetów w string
  return str(octet1) + "." + str(octet2) + "." + str(octet3) + "." + str(octet4)
