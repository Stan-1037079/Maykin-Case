from django.test import TestCase
from django.core.management import call_command
from unittest.mock import patch
from io import StringIO
from case.models import Stad, Hotel

class ImportCSVURLTest(TestCase):

    @patch('requests.Session.get')
    def test_city_and_hotel_csv_import(self, mock_get):
        """
        Test het importeren van steden en hotels uit de CSV-bestanden.
        """
        # Mockt de response van het city.csv
        mock_city_csv = StringIO('AMS;"Amsterdam"\nANT;"Antwerpen"\nATH;"Athene"\nBAK;"Bangkok"\nBAR;"Barcelona"\nBER;"Berlijn"')
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = mock_city_csv.getvalue().encode('utf-8')

        # Voert het management command uit
        call_command('import_csv_url')

        # Controleert of de steden correct zijn geïmporteerd
        self.assertEqual(Stad.objects.count(), 6)
        self.assertTrue(Stad.objects.filter(naam="Amsterdam").exists())
        self.assertTrue(Stad.objects.filter(naam="Antwerpen").exists())
        self.assertTrue(Stad.objects.filter(naam="Athene").exists())
        self.assertTrue(Stad.objects.filter(naam="Bangkok").exists())
        self.assertTrue(Stad.objects.filter(naam="Barcelona").exists())
        self.assertTrue(Stad.objects.filter(naam="Berlijn").exists())

        # Voeg hotels toe voor deze steden
        mock_hotel_csv = StringIO('AMS;"AMS01";"Ibis Amsterdam Airport"\nANT;"ANT01";"Express by Holiday Inn"\nATH;"ATH01";"Evripides"\nBAK;"BAK01";"Narai"\nBAR;"BAR01";"Rialto"\nBER;"BER01";"Quality City-East"')
        mock_get.return_value.content = mock_hotel_csv.getvalue().encode('utf-8')

        # Voert het management command opnieuw uit voor hotels
        call_command('import_csv_url')

        # Controleert of de hotels correct zijn geïmporteerd
        self.assertEqual(Hotel.objects.count(), 6)
        self.assertTrue(Hotel.objects.filter(naam="Ibis Amsterdam Airport").exists())
        self.assertTrue(Hotel.objects.filter(naam="Express by Holiday Inn").exists())
        self.assertTrue(Hotel.objects.filter(naam="Evripides").exists())
        self.assertTrue(Hotel.objects.filter(naam="Narai").exists())
        self.assertTrue(Hotel.objects.filter(naam="Rialto").exists())
        self.assertTrue(Hotel.objects.filter(naam="Quality City-East").exists())

    @patch('requests.Session.get')
    def test_invalid_city_csv(self, mock_get):
        """
        Test wat er gebeurt als het city.csv-bestand een ongeldig formaat heeft.
        """
        # Mockt een onjuist CSV-bestand
        mock_invalid_city_csv = StringIO('InvalidData')
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = mock_invalid_city_csv.getvalue().encode('utf-8')

        # Voert het management command uit
        with self.assertLogs('django', level='DEBUG') as log:
            call_command('import_csv_url')

        # Controleert of er geen steden zijn geïmporteerd
        self.assertEqual(Stad.objects.count(), 0)
        self.assertIn('Skipping invalid row', log.output[0])

    