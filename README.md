# Theseus en de Minotaurus

Om het spelletje Theseus en de Minotaurus te implementeren, zetten we een client- en een server-component op.
Voor de client-component maken we gebruik van JavaScript (we willen dit spelletje in de browser kunnen spelen) en voor de server-component maken we gebruik van Python.

## Introductie

Theseus en de Minotaurus is een logische puzzel die bestaat uit een doolhof in de vorm van een rechthoekig rooster.
Rondom het rooster staan muren en ook tussen aangrenzende vakjes kan er een muur staan die verhindert om van het ene naar het andere vakje te stappen.
Als speler neem je de rol aan van Theseus — koning van Athena — die de uitgang van het doolhof moet zien te bereiken.
Daarbij wordt Theseus opgejaagd door de Minotaurus, die twee stappen zet voor elke stap die Theseus zet.
Dit is bijvoorbeeld de beginopstelling van de eerste puzzel, waarbij de positie van de uitgang wordt aangeduid door het woord "EXIT", de positie van Theseus door een blauwe cirkel en de positie van de Minotaurus door een rode cirkel.
In dit filmpje zie je meteen ook hoe een puzzel typisch opgelost wordt:

https://github.ugent.be/storage/user/1827/files/5afbba0e-e48b-44d5-acb0-cac1c969ab13

Hoewel de Minotaurus sneller is dan Theseus, zijn zijn beweging compleet voorspelbaar en vaak inefficiënt: ze worden bepaald door te kijken of de Minotaurus dichter bij Theseus kan komen door horizontaal te bewegen, en vervolgens te kijken of hij dichter kan komen door verticaal te bewegen.
Als geen van beide bewegingen hem dichter bij Theseus zouden brengen, dan slaat de Minotaurus zijn beurt over. 
Ook Theseus mag zijn beurt overslaan.

## Opgave

Jullie opdracht bestaat er nu uit van dit spelletje te implementeren.
Je moet zowel een implementatie voor de server als de client voorzien.
De server beschikt over een lijst van puzzels (*levels*) en de locaties van Theseus, de Minotaurus en alle muren.
De client moet correct communiceren met de server en de puzzels zichtbaar voorstellen en ervoor zorgen dat de speler met het spel kan interageren.
Lees verder in dit document voor meer informatie over hoe de server en de client specifiek moeten geïmplementeerd worden.

We zullen overal gebruikmaken van [JSON-objecten](https://www.json.org/json-en.html) om informatie tussen de server en de client uit te wisselen.
Dit is een schematische voorstelling van de eerste puzzel:

![minotaur_level_1](https://github.ugent.be/storage/user/1827/files/f6bca91d-cdba-4e28-a283-dac2ef07bf5a)

Afgaande op dit screenshot kunnen we de eerste puzzzel als volgt voorstellen als JSON-object:

```json
{
    "tiles": [
        { "x": 0, "y": 0, "left": true, "right": false, "top": true, "bottom": false },
        { "x": 1, "y": 0, "left": false, "right": false, "top": true, "bottom": false },
        { "x": 2, "y": 0, "left": false, "right": true, "top": true, "bottom": false },

        { "x": 0, "y": 1, "left": true, "right": false, "top": false, "bottom": false },
        { "x": 1, "y": 1, "left": false, "right": true, "top": true, "bottom": true },
        { "x": 2, "y": 1, "left": false, "right": false, "top": false, "bottom": false },
        { "x": 3, "y": 1, "left": false, "right": false, "top": true, "bottom": true },

        { "x": 0, "y": 2, "left": true, "right": false, "top": false, "bottom": true },
        { "x": 1, "y": 2, "left": false, "right": false, "top": false, "bottom": true },
        { "x": 2, "y": 2, "left": false, "right": true, "top": false, "bottom": true }
    ],

    "theseus": {
        "x": 1,
        "y": 0
    },

    "minotaur": {
        "x": 1,
        "y": 2
    },

    "exit": {
        "x": 3,
        "y": 1
    }
}
```

Concreet beschikt dit object over de volgende eigenschappen:

* `tiles`: Een lijst met daarin een beschrijving van elke tegel. Deze tegels worden op hun beurt ook weer voorgesteld door een JSON-object met de volgende eigenschappen:
  * `x`: De rij waarop deze tegel zich bevindt. (`int`)
  * `y`: De kolom waarop deze tegel zich bevindt. (`int`)
  * `left`: Is de linkerzijde van deze tegel een muur? (`boolean`)
  * `right`: Is de rechterzijde van deze tegel een muur? (`boolean`)
  * `bottom`: Is de onderzijde van deze tegel een muur? (`boolean`)
  * `top`: Is de bovenzijde van deze tegel een muur? (`boolean`)
* `theseus`: Geeft de positie van Theseus (de speler) in het rooster aan.
* `minotaur`: Geeft de positie van de Minotaurus in het rooster aan.
* `exit`: Geeft de positie aan van de uitgang in het rooster aan.

# Server

De server is verantwoordelijk voor het beheren van de puzzels en biedt een aantal API-endpoints aan waarmee de client-component nieuwe puzzels kan opvragen, alsook de hoogste score voor elke puzzel.
Voor de server-component van het spelletje maken we gebruik van Python en het [Flask-framework](https://flask.palletsprojects.com/).
Om jullie al een beetje op weg te zetten, hebben we reeds een deel van de configuratie van de Flask-server voorzien en moeten jullie vertrekken vanaf het bestandje `server.py` dat je kan terugvinden in deze repository.

## Flask

Flask is een webframework voor Python dat het mogelijk maakt om heel eenvoudige REST API's te implementeren.
Gevraagd wordt om te vertrekken vanaf het volgende `server.py` bestandje waarin we de route-afhandeling reeds geconfigureerd hebben.
De signatuur van elke functie is reeds aanwezig en dienen jullie verder aan te vullen.
Het is natuurlijk ook toegestaan van extra hulp-functies toe te voegen als je die graag wil gebruiken.

### Installeren van Flask

Om gebruik te kunnen maken van Flask, zal je het framework eerst lokaal moeten installeren.
Dat kan door gebruik te maken van `pip` (dat meegeleverd wordt bij de installatie van Python).
Voer het volgende commando uit in de terminal om Flask te installeren:

```
pip3 install flask flask_cors
```

Controleer daarna dat je de meest recente versie van flask gebruikt door `flask --version` uit te voeren.
De meest recente versie op het moment van schrijven is 2.2.3.
Als jouw flask-installatie ouder is dan versie 2.2.3, dan kan je deze bijwerken door `pip3 install flask --upgrade` uit te voeren.

### Lokaal testen

Tijdens het ontwikkelen en implementeren van alle API-endpoints is het handig om alles lokaal te kunnen testen.
Je kan daartoe een Flask-server opstarten via de terminal en communiceren met je server op poort 5000 door het volgende commando uit te voeren:

```
flask --app server run --debug
```

Hierbij gaan we ervan uit dat het bestandje met je server-code `server.py` noemt (zoals dat in de opgave het geval is).

## API

De implementatie van jouw server moet de API-endpoints ondersteunen die hieronder opgelijst worden.
Let erop dat je de statuscodes respecteert die moeten teruggegeven worden en dat je waar nodig ook de gepaste foutafhandeling voorziet.

### GET `/levels`

Dit endpoint geeft een overzicht terug van alle gekende puzzels (*levels*) op deze server.
Voor elke oproep zal dit endpoint met HTTP statuscode `200` (OK) moeten reageren.

#### Voorbeeld:

**GET**
```
curl localhost:8080/levels
```

**Response (HTTP 200)**
```json
{
  "aantal_levels": 25
}
```

### GET `/level/{niveau}`

Dit endpoint kan gebruikt worden om de puzzel met het opgegeven `niveau` op te vragen.
Let erop dat je een `GET`-request gebruikt bij het oproepen van dit endpoint.

Wanneer alles succesvol verlopen is, zal dit endpoint het volgende JSON-object teruggeven en moet het endpoint reageren met HTTP statuscode `200` (OK).
Wanneer er een puzzel opgevraagd wordt die niet bestaat, dan moet dit endpoint reageren met statuscode `404` (not found) en een foutboodschap zoals in de onderstaande voorbeeldjes versturen.

#### Voorbeeld 1: opvragen van level 18

**GET**
```
curl localhost:8080/level/18
```

**Response (HTTP 200)**
```json
{
  "level": 13,
  "game": "xxx",
  "highscore": 12
}
```

#### Voorbeeld 2: opvragen van een onbestaand level 78

**GET**
```
curl localhost:8080/level/78
```

**Response (HTTP 404)**
```
{
  "foutboodschap": "Puzzel 78 bestaat niet."
}
```

### GET `/random_level`

Dit endpoint geeft een willekeurige puzzel terug vanop deze server en geeft steeds HTTP statuscode `200` (OK) terug.

#### Voorbeeld
**GET**
```
curl localhost:8080/random_level
```

**Response (HTTP 200)**
```json
{
  "level": 8,
  "game": {},
  "highscore": 17
}
```

### POST `/highscore/{niveau}`

Om de hoogste score voor een puzzel bij te werken, kan je het `/highscore` endpoint gebruiken.
Bedoeling hiervan is dat je de huidige score van de speler doorgeeft bij het succesvol beïndigen van het spel.
Als de score voor deze puzzel beter is dan de huidige hoogste score die de server tot nu toe heeft binnengekregen, dan zal de nieuwe hoogste score (*highscore*) aangepast worden en geeft de server de HTTP statuscode `200` (OK) terug.
Is de nieuwe score lager dan de hoogste score die de server reeds heeft binnengekregen, dan verandert er niets en geeft de server HTTP statuscode `304` (not modified) terug.

#### Voorbeeld 1: updaten van de hoogste score voor level 12

Op dit moment is de hoogste score voor puzzel 12 gelijk aan $10$.
De nieuwe hoogste score $6$ is kleiner dan $10$, dus moet de hoogste score aangepast worden (de hoogste score geeft namelijk aan in hoeveel stappen de gebruiker het spel heeft opgelost, hoe minder stappen, hoe beter).

**POST**
```
curl -X POST -H 'Content-Type: application/json' localhost:8080/highscore/12 -d '{"highscore": 6}'
```

**Response (HTTP 200)**
```
{
  "status": "Highscore succesvol bijgewerkt van 10 naar 6."
}
```

#### Voorbeeld 2: nieuwe hoogste score is niet beter dan de reeds gekende hoogste score

In dit voorbeeld probeert de gebruiker de hoogste score op de server voor level 12 bij te werken naar $10$.
De huidige hoogste score is echter $6$ en is dus al beter.
Dit betekent dat de server geen aanpassing maakt en HTTP statuscode `304` (not modified) gaat teruggeven.

**POST**
```
curl -X POST -H 'Content-Type: application/json' localhost:8080/highscore/12 -d '{"highscore": 10}'
```

**Response (HTTP 304)**
```
{
  "status": "Gekende highscore 6 voor dit level was reeds beter dan nieuwe highscore 10."
}
```

# Client

De client-component van het spelletje moet een HTML-webpagina zijn die gebruikmaakt van JavaScript om te communiceren met de server en om het spelletje interactief te maken.
Om het spel voor iedereen eenvoudig speelbaar te maken, hebben we reeds een aantal besturingen vastgelegd die door het spel gevolgd moeten worden:

* **pijltje omhoog**: De speler beweegt zich 1 vakje naar boven.
* **pijltje omlaag**: De speler beweegt zich 1 vakje naar beneden.
* **pijltje naar links**: De speler beweegt zich 1 vakje naar links.
* **pijltje naar rechts**: De speler beweegt zich 1 vakje naar rechts.
* **spatie**: De speler wacht een beurt. De Minotaurus gaat dus wel bewegen, de speler blijft staan waar die stond.
* **R**: Het spelbord wordt gereset en de speler kan opnieuw beginnen.
* **N**: Ga door naar de volgende puzzel.
* **P**: Keer terug naar de vorige puzzel.

## Gebruikersinterface

Bij een spelletje horen ook een aantal extra elementen die weergegeven moeten worden als deel van de grafische gebruikersinterface.
We verwachten minimaal de volgende zaken:

### Spelinformatie

* **Titel**: De titel van het spel moet ergens op de pagina duidelijk zichtbaar zijn.
* **Huidige score**: Het aantal stappen dat de speler tot op dit moment reeds heeft gezet.
* **Hoogste score**: Het kleinste aantal stappen waarmee een gebruiker dit level heeft kunnen oplossen tot hiertoe.
* **Puzzelnummer**: Ergens moet je ook aangeven welke puzzel de gebruiker op dit moment aan het oplossen is.
* **Besturingen**: De toetsen waarmee je het spel kan aansturen, moeten duidelijk aangegeven worden.

### Knoppen

Er moeten een aantal knoppen terug te vinden zijn waarmee elk van de volgende acties kan ondernomen worden.

* **Herstel**: Herstel het spel en start de huidige puzzel opnieuw.
* **Volgende level**: Ga door naar de volgende puzzel.
* **Vorige level**: Keer terug naar de vorige puzzel.

Onderstaande video toont een voorbeeldimplementatie van het spel:

https://github.ugent.be/storage/user/1827/files/a1b3f701-12be-416e-969f-72522bee055b

Jouw spelletje mag er helemaal anders uitzien, dit is enkel een voorbeeld van wat er mogelijk is.
Je moet je niet beperken tot de elementen die we hier hebben opgelijst. Je mag ook extra functionaliteit inbouwen en voorzien, maar dit wordt niet verwacht voor deze opgave.

## Foutafhandeling

Een aantal handelingen tijdens het spelen van het spel kunnen tot problemen leiden (bijvoorbeeld het opvragen van een puzzel die niet bestaat, een hoogste score bijwerken die eigenlijk slechter is dan de huidige hoogste score, enz.).
Om deze problemen te voorkomen, moet de server defensief handelen en telkens controleren of een bepaalde handeling geldig is vooraleer deze uit te voeren.

Zorg ervoor dat jouw implementatie van het spel deze problemen zoveel mogelijk vermijdt door enkel requests uit te voeren die geldig zijn (je kan immers aan de server vragen hoeveel puzzels er beschikbaar zijn en deze informatie gebruiken om enkel bestaande puzzels op te vragen).

### Instabiele internetverbinding

Tijdens het spelen van het spel kan het gebeuren dat de internetverbinding van een gebruiker wegvalt, waardoor netwerk-requests kunnen falen.
Zorg ervoor dat jouw implementatie hiermee rekening houdt en een gepaste foutboodschap aan de gebruiker toont wanneer een request niet uitgevoerd kon worden (zoals in onderstaande voorbeeldje).

<img width="1624" alt="Screenshot 2023-03-28 at 11 04 15" src="https://github.ugent.be/storage/user/1827/files/dbbbf783-21f3-4346-83d1-c705b26b3e62">

## Lokaal testen van de client

Om lokaal jouw implementatie van het spelletje te testen, moet je ervoor zorgen dat je server-implementatie draait op de achtergrond (hoe je dit moet doen, beschreven we reeds eerder) en moet je ook een tweede webserver opzetten waarmee je je webpagina kan hosten.
Je kan hiervoor een Python-server opstarten door het volgende commando uit te voeren in de map waar je HTML-bestand zich bevindt:

```
python3 -m http.server 8000
```

Als je nu je de URL [http://localhost:8000](http://localhost:8000) bezoekt, dan zou je jouw spelletje moeten kunnen spelen.
