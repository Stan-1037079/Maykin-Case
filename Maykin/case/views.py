from django.shortcuts import render
from .models import Stad, Hotel

def home(request):
    # View voor de homepagina. Deze view behandelt de zoekfunctionaliteit voor hotels 
    # en zorgt ervoor dat de achtergrondafbeelding verandert op basis van de geselecteerde stad.
    # Haalt alle steden op voor de dropdown bar.
    # Filtert de hotels op basis van de geselecteerde stad.
    steden = Stad.objects.all()
    geselecteerde_stad = request.GET.get('stad')

    # Standaard achtergrond wanneer er geen stad is geselecteerd
    achtergrond_afbeelding = "hotel.jpg"  

    # Als er een stad is geselecteerd in de dropdown bar wordt de bijbehorende achtergrondafbeelding gebruikt
    if geselecteerde_stad:
        stad_obj = Stad.objects.filter(naam=geselecteerde_stad).first()
        if stad_obj and stad_obj.achtergrond_afbeelding:  # Als er een afbeelding is ingesteld voor de stad
            achtergrond_afbeelding = stad_obj.achtergrond_afbeelding

    # Filtert hotels op basis van de geselecteerde stad
    hotels = Hotel.objects.filter(stad__naam=geselecteerde_stad) if geselecteerde_stad else None

    return render(request, 'home.html', {
        'steden': steden,
        'hotels': hotels,
        'geselecteerde_stad': geselecteerde_stad,
        'achtergrond_afbeelding': achtergrond_afbeelding,  # Geef de achtergrondafbeelding door aan de template
    })
