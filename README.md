# Projectvoorstel webprogrammeren groep 15
​
*Jochem, Thomas, Iris, Hugo*
​
## Samenvatting
Het doel van onze webapplicatie is het mogelijk maken om studieplekken te delen en te ontdekken.
De vraag naar studieplekken onder studenten is groot, maar het vinden van een goede studieplek is lastig.
​
## Schetsen
![Schets1](/webik/project_ik15/WhatsApp Image 2020-01-14 at 15.21.04 (1).jpeg)
![Schets2](/webik/project_ik15/WhatsApp Image 2020-01-14 at 15.21.04 (2).jpeg)
![Schets3](/webik/project_ik15/WhatsApp Image 2020-01-14 at 15.21.04 (3).jpeg)
![Schets4](/webik/project_ik15/WhatsApp Image 2020-01-14 at 15.21.04.jpeg)
​
## Features
1. Een kaart in de applicatie
2. Verkenpagina waarop nieuwe locaties te ontdekken zijn door middel van swipen naar links of rechts
3. Gebruikers kunnen andere gebruikers volgen
4. Gebruikers kunnen studieplekken ‘liken’
5. Een favorieten pagina voor gebruikers
6. Gebruikers worden gewaarschuwd wanneer een nieuwe studieplek in de buurt is
7. Gebruikers kunnen naar een ‘trending’ pagina
8. Gebruikers kunnen een reactie achter laten bij een studieplek
9. Studieplek wordt verborgen voor een bepaalde tijd wanneer het een nog te bepalen aantal likes heeft gekregen
​
## Minimum viable product
Gebruikers kunnen publiekelijk foto’s posten met begeleidende tekst. Alle gebruikers kunnen elkaar “volgen” en zo de foto’s bekijken en liken. Gebruikers kunnen in plaats van een eigen foto bekijken ook foto's van random gebruikers zien.
​
## Afhankelijkheden
* Databronnen:
    * API : [http://api.giphy.com](http://api.giphy.com)
* Externe componenten:
    * Bootstrap
    * Slack
* Concurrerende, bestaande websites:
    * N.V.T.
* Moeilijkste delen applicatie:
    * Profiel pagina veel werk
    * Informatie pagina, combineren met database
    * Ontdekken moeilijk, veel werk
## Models and helpers
    * Apology: geeft een foutmelding aan user als er iets mis is gegaan of verkeerd is ingevuld
    * Login required: zorgt dat een user is ingelogd om functies uit te voeren
## Controllers : scherm ja of nee en request type
    * Register JA/POST
    * Log in JA/POST
    * Log out NEE/POST
    * Profile JA/GET
    * Upload JA/POST
    * Display_photo JA/GET
    * Discovery JA/POST
    * Favorites JA/POST
    * Settings JA/POST
    * Following JA/GET
    * Check(username) NEE/GET
    *Apology JA/GET
## Plugins and Frameworks
    * SQL : [https://docs.microsoft.com/en-us/sql/sql-server/?view=sql-server-ver15](https://docs.microsoft.com/en-us/sql/sql-server/?view=sql-server-ver15)
    * Flask [http://flask.palletsprojects.com/en/1.1.x/](http://flask.palletsprojects.com/en/1.1.x/)
    * Werkzeug [https://werkzeug.palletsprojects.com/en/0.15.x/](https://werkzeug.palletsprojects.com/en/0.15.x/)
    * Bootstrap [https://getbootstrap.com/](https://getbootstrap.com/)