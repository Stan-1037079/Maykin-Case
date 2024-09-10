import csv
import requests

city_url = 'http://rebecca.maykinmedia.nl/djangocase/city.csv'
username = 'python-demo'
password = 'claw30_bumps'

try:
    with requests.Session() as s:
        # Stuurt de username en password mee met het request doormiddel van de auth parameter
        download = s.get(city_url, auth=(username, password), timeout=30)

        # Checkt of de request succesvol was
        if download.status_code == 200:
            decoded_content = download.content.decode('utf-8')

            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            my_list = list(cr)

            for row in my_list:
                print(row)
        else:
            print(f"Failed to download CSV. Status code: {download.status_code}")
except requests.exceptions.Timeout:
    print("The request timed out. Try increasing the timeout or check your connection.")
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
