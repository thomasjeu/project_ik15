# Webprogrammeren 2019-2020 groep 15, StudySpot
​
*Jochem van Eerden, Thomas Dodeman, Iris Bakker, Hugo Hoenderboom*
​
## Samenvatting
Het doel van onze webapplicatie is het mogelijk maken om studieplekken te delen en te ontdekken.
De vraag naar studieplekken onder studenten is groot, maar het vinden van een goede studieplek is lastig.
​
## Screenshot van de webapplicatie
SCREENSHOT APPLICATIE in aparte docs map
## Features
1. Een gebruiker kan zich registreren of inloggen met zijn gebruikersnaam en wachtwoord.
    * Wachtwoorden zonder cijfer worden geweigerd
    * Inloggen zonder geldig gebruikersnaam/wachtwoord wordt geweigerd
    * Door middel van JavaScript wordt er bij inloggen live weergegeven of de gebruikersnaam wel bestaat, zo niet dan werkt de inlogknop niet
    * Op de zelfde manier wordt er met JavaScript bij register gecontroleerd of de username niet al bestaat, of het wachtwoord voldoet aan de eisen en of het wachtwoord en de bevestiging overeenkomen

2. Een gebruiker kan de profielen van andere gebruikers en zichzelf zien.
    * Een profielpagina bestaat uit een gebruikersnaam, profielfoto, gebruikersbeschrijving, geposte StudySpots van de gebruiker en een lijst van volgers/volgend
    * De gebruiker maakt deze gegevens zelf, door het in settings aan te passen
    * De gebruiker maakt de posts zelf door deze te uploaden en posten
    * De profielfoto wordt opgehaald via een path in de database die verwijst naar een foto opgeslagen in de static folder
    * De titel en de hoeveelheid likes die een post heeft worden opgehaald uit de database

3. Een gebruiker kan meer informatie over een post opvragen door op de post op het profiel te klikken.
    * De gebruiker geeft een post een titel, beschrijving en adres mee
    * Deze informatie wordt uit de database gehaald en weergeven bij opvraag van meer informatie
    * Het adres wat de gebruiker heeft meegegeven, wordt automatisch weergeven in een kaart van Google Maps met gebruik van een Google API

4. Een gebruiker heeft de mogelijkheid een andere gebruiker te volgen of te ontvolgen.
    * Dit gebeurt door een toevoeging in de volgers database
    * De volgers/volgend lijst op de profielpagina wordt na deze actie direct aangepast

5. Een gebruiker kan zijn gebruikersnaam, wachtwoord, profielfoto en beschrijving aanpassen in de settings pagina.
    * De gegevens worden aangepast in de database
    * De aangepaste gegevens zijn direct zichtbaar op de profielpagina
    * Wanneer de profielfoto wordt gewijzigt wordt de path in de database aangepast en wordt de oude foto verwijderd uit de static folder

6. Een gebruiker kan foto's van een studieplek uploaden.
    * Hier geeft de gebruiker een foto, titel, beschrijving en adres mee
    * Deze gegevens worden allen opgeslagen in de uploads database samen met de path naar de foto in de static folder
    * De upload slaagt alleen als alle velden zijn ingevuld
    * De naam van de foto mag nog niet bestaan in de static folder zodat er geen conflicten ontstaan bij het ophalen van de foto

7. Als een gebruiker niet tevreden is over een post, kan de gebruiker die de post heeft geupload deze post weer verwijderen.
    * De upload wordt gewist uit de uploads database
    * De image wordt verwijderd uit de static folder

8. Verkenpagina waarop nieuwe StudySpots(locaties) te ontdekken zijn die andere gebruikers hebben geupload.
    * Dit gebeurt door een random post uit de uploads database te kiezen
    * De hoeveelheid likes die een post heeft wordt opgehaald uit de likes database

9. Deze StudySpots kan een gebruiker liken/unliken, favorieten/onfavorieten, of afwijzen waarop er een nieuwe locatie wordt weergeven.
    * Wanneer er geliked of gefavoriet wordt worden deze opgeslagen in de daarvoor bestemde databases
    * Waneer de gebruiker kiest voor volgende post wordt er weer een random post ingeladen

10. De kaart die weergeven wordt bij 'meer informatie' is gemaakt met een google maps API.
    * De rode pin in de kaart is de locatie die een gebruiker heeft opgegeven tijdens het uploaden van de post.

11. Gebruikers kunnen naar een favorieten pagina, waar al hun favoriete posts zijn opgeslagen.

12. Op de favorieten pagina is ook de mogelijkheid om meer informatie over de favoriete posts op te vragen, door op de post te klikken.


​
## Minimum viable product
Gebruikers kunnen publiekelijk foto’s posten met begeleidende tekst. Alle gebruikers kunnen elkaar “volgen” en zo de foto’s bekijken en liken. De locatie van een foto wordt weergeven in een kaart met een GoogleMaps API.
​
## Onderdelen van het project en wie grofweg aan welk onderdeel heeft gewerkt

Registratie en login/logout --> Thomas
Weergave profielen gebruikers --> Iris, Jochem, Thomas, Hugo
Instellingen pagina --> Jochem, Thomas, Iris
Upload pagina --> Jochem, Thomas, Iris

Discover pagina --> Iris, Jochem, Thomas, Hugo
Informatie pagina --> Iris, Jochem, Thomas

Like functie --> Iris, Jochem
Favorieten functie --> Thomas

Favorieten weergave --> Hugo, Thomas
Layout --> Hugo

Google Maps API --> Iris, Jochem
Followers and Following --> Jochem, Iris, Hugo

## Wegwijzer door de repository
* De map " doc/ " bevat een screenshot van de webapplicatie StudySpot.

* De map " static/ " bevat 2 andere mappen met hier in afbeeldingen.
    * In de map " posts/ " staan de afbeeldingen van studieplekken die gebruikers uploaden
    * In de map "profile/ " staan de afbeeldingen die gebruikers uploaden als profielfoto

* De map " templates/ " bestaat uit alle HTML bestanden die gebruikt zijn in het project.
    * In de volgende HTML bestanden staan functies

* In het bestand "admin.db" staat de database. Hierin slaan wij informatie op die nodig is voor de webapplicatie StudySpot.
* In het bestand "application.py" staan alle python functies die gebruikt worden in de webapplicatie.
* In het bestand "helpers.py" staan python functies die "application.py" ondersteunen. Dit maakt application.py overzichtelijker.


## Databronnen:
    * API : [https://developers.google.com/maps/documentation/javascript/tutorial?hl=nl](https://developers.google.com/maps/documentation/javascript/tutorial?hl=nl)
## Externe componenten:
    * Bootstrap
    * Slack