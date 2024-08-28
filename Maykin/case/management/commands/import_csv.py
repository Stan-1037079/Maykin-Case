import os
import csv
from django.core.management.base import BaseCommand
from case.models import Stad, Hotel

class Command(BaseCommand):
    help = 'Importeer steden en hotels uit CSV-bestanden'

    def handle(self, *args, **kwargs):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        data_dir = os.path.join(base_dir, 'data')

        # Maak een mapping van stadscodes naar stadnamen
        stad_code_to_name = {}

        # Open en lees city.csv om de stadcode-naar-naam mapping te maken
        try:
            with open(os.path.join(data_dir, 'city.csv'), newline='', encoding='utf-8') as stedenfile:
                reader = csv.reader(stedenfile, delimiter=';')
                for row in reader:
                    stad_code = row[0]  # Stadscode in de eerste kolom
                    stad_naam = row[1]  # Stadsnaam in de tweede kolom
                    stad_code_to_name[stad_code] = stad_naam
                    Stad.objects.get_or_create(naam=stad_naam)  # Sla de volledige stadnaam op
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('city.csv bestand niet gevonden!'))

        # Open en lees hotel.csv en gebruik de stadcode-naar-naam mapping om de stad te vinden
        try:
            with open(os.path.join(data_dir, 'hotel.csv'), newline='', encoding='utf-8') as hotelsfile:
                reader = csv.reader(hotelsfile, delimiter=';')
                for row in reader:
                    stad_code = row[0]  # Stadscode in de eerste kolom
                    hotel_naam = row[2]  # Hotelnaam in de derde kolom

                    # Zoek de volledige naam van de stad met behulp van de stadscode
                    stad_naam = stad_code_to_name.get(stad_code)
                    if stad_naam:
                        stad = Stad.objects.get(naam=stad_naam)  # Zoek op stadnaam
                        Hotel.objects.get_or_create(naam=hotel_naam, stad=stad)
                    else:
                        self.stdout.write(self.style.ERROR(f"Stadscode {stad_code} komt niet overeen met een bekende stad."))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('hotel.csv bestand niet gevonden!'))

        self.stdout.write(self.style.SUCCESS('Data import afgerond'))
