// Biblioteki do komunikacji sieciowej
#include <Ethernet.h>
#include "libraries/aREST/aREST.h"
#include "libraries/Watchdog/wdt.h"
// Biblioteka do komunikacji z wyświetlaczem LCD
#include <Wire.h>

int i2c_address = 0x30; // Adres układu sterującego wyświetlaczem na szynie I2C (0x30 - 42 dziesiętnie)
int lcd_control(String command); // Deklaracja funkcji udostępnionej przez REST API
// Inicjalizacja zmiennych do komunikacji sieciowej
EthernetClient client;
EthernetServer server(80);
aREST rest = aREST();
byte mac[] = { 0x90, 0xA2, 0xDA, 0x10, 0xCC, 0x57 };
byte ip[] = { 192, 168, 1, 51 };
byte dns[] = { 192, 168, 1, 50 }; // DNS obsługiwany przez serwer
byte subnet_mask[] { 255, 255, 255, 0 };
// Inicjalizacja zmiennych serwera HTTP
int HTTP_port = 80;
String request_type = "GET";
string host_name = "/sygnalizator";
String IP_address = "";
String REST_zapytanie = "?value1=26&value2=70";

void setup() {
  // Inicjalizacja wyjść GPIO sterujących opcjonalnym modułem przekaźbnikowym
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
  // Inicjalizacja wyjścia GPIO sterującego zasilaniem wyświetlacza
  pinMode(5, OUTPUT);
  // Inicjalizacja wyjścia GPIO dla diody statusu komunikacji
  pinMode(4, OUTPUT);
  Serial.begin(9600); // Inicjalizacja komunikacji szeregowej
  // Nawiąż połączenie z siecią
  Ethernet.begin(mac, ip, router, dns, subnet_mask);
  // Ustalenie funkcji do udostępnienia przez REST API
  rest.function("lcd", lcd_control);
  // Inicjalizacja serwera do odbioru komunikatów REST API
  rest.set_id("001"); // ID
  rest.set_name("sygnalizator_1"); // Nazwa

  // Jeśli połączenie zostało ustanowione, wyświetl wiadomość powitalną
    digitalWrite(5, HIGH); // Uruchom zasilanie wyświetlacza
    Wire.begin(); // Inicjalizacja biblioteki Wire
    delay(100); // Odczekaj 100ms na ustanowienie komunikacji
    Wire.beginTransmission(i2c_address); // Rozpocznij transmisję I2C
    Wire.write(0x2); // Tryb znaków w wyświetlaczu
    Wire.write("Sygnalizator gotowy"); // Wiadomość powitalna
    Wire.endTransmission(); // Koniec transmisji I2C
    delay(10000); // Czas na odczytanie wiadomości);
    Serial.println(Ethernet.localIP());// Wyślij do konsoli otrzymany adres IP
    // Koniec wiadomości powitalnej
  digitalWrite(5, LOW); // Wyłącz wyświetlacz

  wdt_enable(WDTO_8S); // Uruchom watchdog w razie zawieszenia się mikrokontrolera
  rest.set_status_led(4);

}

void loop()
{
  // Nasłuchuj klientów
  client = server.available();
  rest.handle(client);
  wdt_reset();
}
// Funkcja udostępniona przez REST API
    int lcd_control(String command)
  {
    int state = command.toInt(); // Zmienna z otrzymanym poleceniem
    digitalWrite(5,1); // Uruchom wyświetlacz
    Wire.begin();
    delay(100);
    Wire.beginTransmission(i2c_address);
    Wire.write(0x2);
    Wire.write(32);
    // Polecenie Gotowy
    if (state == 0)
    {
      Wire.write("Gotowy?");
      Serial.println ("Otrzymano polecenie GOTOWOSC");// Wyślij potwierdzenie otrzymania polecenia
    }
    // Polecenie Akcja
    else if (state == 1)
    {
      Wire.write("Akcja!");
      Serial.println ("Otrzymano polecenie AKCJA");// Wyślij potwierdzenie otrzymania polecenia
    }
    // Sygnał kontrolny z serwera
    else if (state == 2)
    {
      Wire.write("Serwer gotowy");
      Serial.println ("Aplikacja serwera zostala uruchomiona");// Wyślij potwierdzenie otrzymania polecenia
    }
    // Zamknięcie przekaźnika
    else if (16 >= state > 10)
    {
      int relay_pin = state - 10; // Styk GPIO przekaznika
      digitalWrite(relay_pin, 1);
      Serial.println ("Zamknieto przekaznik " + relay_pin);// Wyślij potwierdzenie otrzymania polecenia
    }
     // Otwarcie przekaźnika
    else if (26 >= state > 20)
    {
      int relay_pin = state - 20;
      digitalWrite(relay_pin, 0);
      Serial.println ("Otwarto przekaznik " + relay_pin);// Wyślij potwierdzenie otrzymania polecenia
    }
    Wire.endTransmission();
    delay(3000);
    digitalWrite(5,0); // Wyłącz wyświetlacz
    return 1;
  }
