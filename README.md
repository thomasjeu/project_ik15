# Webprogrammeren 2019-2020 groep 15, StudySpot
​
*Jochem van Eerden, Thomas Dodeman, Iris Bakker, Hugo Hoenderboom*
​
## Samenvatting
Het doel van onze webapplicatie is het mogelijk maken om studieplekken te delen en te ontdekken.
De vraag naar studieplekken onder studenten is groot, maar het vinden van een goede studieplek is lastig.
​
## Screenshots van de webapplicatie
De screenshots van de webapplicatie staan in een aparte docs map.

## Features
1. Een gebruiker kan zich registreren of inloggen met zijn gebruikersnaam en wachtwoord.
    * Wachtwoorden zonder cijfer worden geweigerd
    * Inloggen zonder geldig gebruikersnaam/wachtwoord wordt geweigerd
    * Door middel van JavaScript wordt er bij inloggen live weergegeven of de gebruikersnaam wel bestaat, zo niet dan werkt de inlogknop niet
    * Op de zelfde manier wordt er met JavaScript bij register gecontroleerd of de username niet al bestaat, of het wachtwoord voldoet aan de eisen en of het wachtwoord en de bevestiging overeenkomen
    * Er staat een stukje tekst over wat de website doet, met een link naar de about pagina voor meer informatie

2. Een gebruiker kan de profielen van andere gebruikers en zichzelf zien.
    * Een profielpagina bestaat uit een gebruikersnaam, profielfoto, gebruikersbeschrijving, geposte StudySpots van de gebruiker en een lijst van volgers/volgend
    * De namen in de volgers/volgend lijst zijn klikbaar en verwijzen naar de profielpagina van die gebruiker
    * De gebruiker maakt deze gegevens zelf, door het in settings aan te passen
    * De gebruiker maakt de posts zelf door deze te uploaden en posten
    * De profielfoto wordt opgehaald via een path in de database die verwijst naar een foto opgeslagen in de static folder
    * De titel en de hoeveelheid likes die een post heeft worden opgehaald uit de database

3. Een gebruiker kan meer informatie over een post opvragen door op de post op het profiel te klikken.
    * De gebruiker geeft een post een titel, beschrijving en adres mee
    * Deze informatie wordt uit de database gehaald en weergeven bij opvraag van meer informatie
    * De gebruikersnaam van de uploader wordt ook klikbaar weergegeven en verwijst naar de profielpagina van de gebruiker
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

10. De kaart die weergeven wordt bij 'meer informatie' is gemaakt met een Google Maps API.
    * De rode pin in de kaart is de locatie die een gebruiker heeft opgegeven tijdens het uploaden van de post.
    * Het is mogelijk om rond te navigeren op de kaart en Google Streetview te gebruiken

11. Gebruikers kunnen naar een favorieten pagina, waar al hun favoriete posts zijn opgeslagen.
    * Deze worden als een fotocollage weergegeven en zijn klikbaar, ze verwijzen naar de meer informatie pagina van de post
    * Een post heeft een maximum van 50 favorieten, daarna is de post alleen nog zichtbaar op de favorietenpagina ( niet in discover, profile en following)
         *Dit zodat een plek niet té vol zit en het niet meer lekker rustig is
    * Een gebruiker kan maximaal 20 posts favorieten, daarna moet de gebruiker iets onfavorieten om weer iets nieuws te kunnen favorieten
         *Gebruikers worden zo actief gestimuleerd posts te onfavorieten, waardoor de blokkade op posts die 50 favorieten hebben weer weg gaat. Hiermee is de post weer beschikbaar voor andere gebruikers (want favorieten is nu <50)

12. Er bestaat ook een volgend pagina waar de posts van gebruikers die jij volgt staan
    * De posts worden weergegeven als een fotocollage en zijn klikbaar, ze verwijzen naar de meer informatie pagina van de post

13. De about pagina geeft de gebruiker extra informatie over het gebruik en nut van de website
    * Er staat beschreven wat het doel van de website is
    * Er wordt een korte gebruiksaanwijzing gegeven voor de website

14. Het hamburgermenu die het mogelijk maakt snel tussen pagina's te navigeren en de titel van de website die altijd bovenin de pagina staat
    * Het menu schuift open als links bovenin de pagina op menu wordt geklikt
    * Het menu kan weer gesloten worden als er naast het menu op de pagina wordt geklikt of als er op de sluit menu optie in het menu wordt geklikt
    * Als er op 'StudySpot' bovenin de pagina wordt geklikt wordt de gebruiker doorverwezen naar de homepage, dit is de eigen profiel pagina of de login pagina als de gebruiker nog niet is ingelogd



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

## Link Youtube Productvideo
* https://youtu.be/BHWAHeSHBg0


## Databronnen:
    * Google Maps API : [https://developers.google.com/maps/documentation/javascript/tutorial?hl=nl](https://developers.google.com/maps/documentation/javascript/tutorial?hl=nl)
    * Google Geocoding API : [https://developers.google.com/maps/documentation/javascript/geocoding](https://developers.google.com/maps/documentation/javascript/geocoding)

## Externe componenten:
    * Bootstrap
    * Slack
