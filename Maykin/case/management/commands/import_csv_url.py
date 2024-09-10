import os
import csv
import requests
from django.core.management.base import BaseCommand
from case.models import Stad, Hotel

class Command(BaseCommand):
    help = 'Importeer steden en hotels uit CSV-bestanden van externe links'

    # URLs en authenticatiegegevens
    city_url = 'http://rebecca.maykinmedia.nl/djangocase/city.csv'
    hotel_url = 'http://rebecca.maykinmedia.nl/djangocase/hotel.csv'
    username = 'python-demo'
    password = 'claw30_bumps'

    def download_csv(self, url):
        """
        Helper-functie om een CSV-bestand te downloaden van een externe URL.
        """
        try:
            with requests.Session() as s:
                # Stuurt de username en password mee met het request
                download = s.get(url, auth=(self.username, self.password), timeout=30)

                # Checkt of de request succesvol was
                if download.status_code == 200:
                    decoded_content = download.content.decode('utf-8')
                    cr = csv.reader(decoded_content.splitlines(), delimiter=';', quotechar='"')  # Gebruik ; als delimiter en " als quotechar
                    return list(cr)  # Geef de CSV-inhoud terug als lijst van rijen
                else:
                    self.stdout.write(self.style.ERROR(f"Failed to download CSV from {url}. Status code: {download.status_code}"))
        except requests.exceptions.Timeout:
            self.stdout.write(self.style.ERROR(f"The request to {url} timed out."))
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f"An error occurred while fetching {url}: {e}"))

        return None

    def handle(self, *args, **kwargs):
        # Download en verwerk city.csv
        self.stdout.write('Downloading city.csv...')
        city_data = self.download_csv(self.city_url)
        if city_data:
            stad_code_to_name = {}
            for row in city_data:
                # Logt de inhoud van elke rij voor debugging
                self.stdout.write(f"Processing row: {row}")
                
                # Controleert of de rij minimaal 2 kolommen heeft
                if len(row) < 2:
                    self.stdout.write(self.style.WARNING(f"Skipping invalid row (not enough columns): {row}"))
                    continue
                
                stad_code = row[0].strip()  # Stadscode in de eerste kolom
                stad_naam = row[1].strip()  # Stadsnaam in de tweede kolom
                stad_code_to_name[stad_code] = stad_naam
                Stad.objects.get_or_create(naam=stad_naam)  # Sla de volledige stad naam op

        # Download en verwerkt hotel.csv
        self.stdout.write('Downloading hotel.csv...')
        hotel_data = self.download_csv(self.hotel_url)
        if hotel_data:
            for row in hotel_data:
                # Logt de inhoud van elke rij voor debugging
                self.stdout.write(f"Processing row: {row}")
                
                # Controleert of de rij minimaal 3 kolommen heeft
                if len(row) < 3:
                    self.stdout.write(self.style.WARNING(f"Skipping invalid row (not enough columns): {row}"))
                    continue
                
                stad_code = row[0].strip()  # Stadscode in de eerste kolom
                hotel_naam = row[2].strip()  # Hotelnaam in de derde kolom

                # Zoekt de volledige naam van de stad met behulp van de stadscode
                stad_naam = stad_code_to_name.get(stad_code)
                if stad_naam:
                    stad = Stad.objects.get(naam=stad_naam)  # Zoek op stad naam
                    Hotel.objects.get_or_create(naam=hotel_naam, stad=stad)
                else:
                    self.stdout.write(self.style.ERROR(f"Stadscode {stad_code} komt niet overeen met een bekende stad."))

        self.stdout.write(self.style.SUCCESS('Data import afgerond'))
