from typing import Final

# CAVEAT: These constants rely on real api data.
# In case of deletion of 'Bistro Rudbeck' from the api they should be updated
RESTAURANT_ID: Final = {"valid": "rudbeck", "invalid": "dsdsdsd"}
VALID_RESTAURANT_TITLE: Final = "Bistro Rudbeck"
SAMPLE_DISH_NAME: Final = "Inga måltider serveras"

INVALID_RESTAURANT_ID: Final = "dsadasdasd"
RUDBECK_ID: Final = "rudbeck"
RUDBECK_DATA: Final = {
    "restaurant": {
        "location": "Uppsala",
        "map_url": "https://www.openstreetmap.org/#map=19/59.84518/17.63968",
        "menu": [
            {"dish": "Inga måltider serveras"},
            {"dish": "Inga måltider serveras"},
            {"dish": "Inga måltider serveras"},
            {"dish": "Inga måltider serveras"},
        ],
        "title": "Bistro Rudbeck",
        "url": "https://www.compass-group.se/MatDryck/Restauranger/uppsala/bistro-rudbeck/",
    }
}

ALL_RESTAURANTS: Final = {
    "restaurants": [
        {
            "campus": "Solna",
            "identifier": "glada",
            "menu_url": "http://www.dengladarestaurangen.se/#!meny/c30g",
            "name": "Den Glada Restaurangen",
            "osm": "http://www.openstreetmap.org/#map=19/59.35123/18.03006",
            "url": "http://www.dengladarestaurangen.se/",
        },
        {
            "campus": "Solna",
            "identifier": "haga",
            "menu_url": "http://orenib.se/haga_gk2.pdf",
            "name": "Haga gatukök",
            "osm": "https://www.openstreetmap.org/#map=19/59.34931/18.02095",
            "url": "http://orenib.se/haga_gk2.pdf",
        },
        {
            "campus": "Solna",
            "identifier": "hjulet",
            "menu_url": "http://www.restauranghjulet.se",
            "name": "Restaurang Hjulet",
            "osm": "https://www.openstreetmap.org/#map=19/59.34508/18.02423",
            "url": "http://www.restauranghjulet.se",
        },
        {
            "campus": "Solna",
            "identifier": "jons",
            "menu_url": "https://jonsjacob.gastrogate.com/lunch/",
            "name": "Jöns Jacob ",
            "osm": "https://www.openstreetmap.org/#map=19/59.34673/18.02465",
            "url": "http://gastrogate.com/restaurang/jonsjacob/",
        },
        {
            "campus": "Solna",
            "identifier": "jorpes",
            "menu_url": "https://restaurang-ns.ki.se/cafe-erik-jorpes/",
            "name": "Café Erik Jorpes",
            "osm": "https://www.openstreetmap.org/#map=19/59.34851/18.02721",
            "url": "https://restaurang-ns.ki.se/cafe-erik-jorpes/",
        },
        {
            "campus": "Solna",
            "identifier": "livet",
            "menu_url": "https://www.livetbrand.com/har-finns-livet/stockholm-solna/livet-restaurant-solna/",
            "name": "Livet [Restaurant]",
            "osm": "https://www.openstreetmap.org/#map=19/59.34853/18.02989",
            "url": "https://www.livetbrand.com/har-finns-livet/stockholm-solna/livet-restaurant-solna/",
        },
        {
            "campus": "Solna",
            "identifier": "svarta",
            "menu_url": "https://restaurang-ns.ki.se/svarta-rafven/",
            "name": "Svarta Räfven",
            "osm": "https://www.openstreetmap.org/#map=19/59.34851/18.02804",
            "url": "https://restaurang-ns.ki.se/svarta-rafven/",
        },
        {
            "campus": "Solna",
            "identifier": "nanna",
            "menu_url": "http://restaurang-ns.ki.se/restaurang-nanna-svartz/",
            "name": "Restaurang Nanna Svartz",
            "osm": "https://www.openstreetmap.org/#map=19/59.34848/18.02807",
            "url": "http://restaurang-ns.ki.se/restaurang-nanna-svartz/",
        },
        {
            "campus": "Uppsala",
            "identifier": "bikupan",
            "menu_url": "http://www.hors.se/restaurang/restaurang-bikupan/",
            "name": "Restaurang Bikupan",
            "osm": "https://www.openstreetmap.org/#map=18/59.84186/17.63407",
            "url": "http://www.hors.se/restaurang/restaurang-bikupan/",
        },
        {
            "campus": "Uppsala",
            "identifier": "dufva",
            "menu_url": "https://matfest.se/veckans-lunch/",
            "name": "Sven Dufva",
            "osm": "https://www.openstreetmap.org/#map=19/59.84298/17.64096",
            "url": "http://svendufva.se/",
        },
        {
            "campus": "Uppsala",
            "identifier": "hubben",
            "menu_url": "https://vasakronan.foodbycoor.se/hubben/restaurangen/restaurangens-meny",
            "name": "Restaurang Hubben",
            "osm": "https://www.openstreetmap.org/#map=18/59.84334/17.64074",
            "url": "https://vasakronan.foodbycoor.se/hubben",
        },
        {
            "campus": "Uppsala",
            "identifier": "rudbeck",
            "menu_url": "https://eurest.mashie.com/public/menu/restaurang+kannan/cb061efe?country=se",
            "name": "Bistro Rudbeck",
            "osm": "https://www.openstreetmap.org/#map=19/59.84518/17.63968",
            "url": "https://www.compass-group.se/MatDryck/Restauranger/uppsala/bistro-rudbeck/",
        },
        {
            "campus": "Uppsala",
            "identifier": "tallrik",
            "menu_url": "https://eurest.mashie.com/public/menu/viktoria+hotell+och+konferens/cdbcb148?country=se",
            "name": "Tallriket",
            "osm": "https://www.openstreetmap.org/#map=19/59.84248/17.64046",
            "url": "https://www.compass-group.se/MatDryck/Restauranger/uppsala/tallriket/",
        },
    ]
}
