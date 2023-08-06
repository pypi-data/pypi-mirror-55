API stif / IDF mobilité -> faire une carte multi-objectif des temps de trajets pour nos futurs bureaux à Paris

Matin (5h / 11h) :
- Points départ : les adresses de chacun
- Point d'arrivée : toutes les gares / arrêts de bus 
Soir (16h / 20h) :
- Points départ : toutes les gares / arrêts de bus
- Point d'arrivée : les adresses de chacun

On ne cible que les gares / arrêts de bus car les trajets à pied pour relier n'importe quel autre point sont déterministes en temps et peuvent être calculés après coup ou à la volée.

APIs :
- iledefrance-mobilites
    - https://portal.api.iledefrance-mobilites.fr/fr/
    - https://eu.ftp.opendatasoft.com/stif/Documentation/API_Open_Service.pdf
- geoportail : https://www.geoportail.gouv.fr/actualites/service-de-calcul-disochrones-et-disodistances
- Google maps pour les trajets en voiture / 2 roues / vélo / à pied

À mettre sur github/gitlab

Rendre dispo sur une page web privée via Leaflet / googlmaps / framacartes
