# Ustalenie obrazu zrodlowego
FROM ubuntu:latest
# Ustalenie autora kontenera
LABEL maintainer="Antoni Rylke <arylke1@stu.vistula.edu.pl>"
# Wystawienie portu HTTP
EXPOSE 80/tcp
# Ustalenie katalogu roboczego
WORKDIR /docker
# Utworzenie folderow w katalogu roboczym
RUN mkdir -p /static
RUN mkdir -p /templates
# Skopiowanie plikow do katalogu roboczego
# Zgodnie z lista w pliku .dockerignore
COPY . .
# Instalacja i aktualizacja pakietow
RUN apt-get update
RUN apt-get install python3 -y
RUN apt-get install python3-venv -y
RUN apt-get install python3-pip -y
RUN apt-get upgrade -y
RUN apt-get clean
#Utworzenie i uruchomienie srodowiska wirtualnego
ENV VIRTUAL_ENV=/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
#Instalacja bibliotek Python
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt
# Uruchomienie serwera
CMD [ "python", "main.py" ]