from typing import Final

URL: Final = "http://104.197.45.242/restaurant"

# CAVEAT: These constants rely on real api data.
# In case of deletion of 'Bistro Rudbeck' from the api they should be updated
RESTAURANT_ID: Final = {"valid": "rudbeck", "invalid": "dsdsdsd"}
VALID_RESTAURANT_TITLE: Final = "Bistro Rudbeck"
SAMPLE_DISH_NAME: Final = "Inga måltider serveras"

ERROR_VALID_ID_MSG: Final = "Tip: Consider ensuring that provided RESTAURANT_ID is corresponds to a valid restaurant"
ERROR_REQUEST_ONE_RESTAURANT_MSG: Final = (
    "An error has occurred while requesting restaurant data:"
)
ERROR_REQUEST_MANY_RESTAURANTS_MSG: Final = (
    "An error has occurred while loading restaurants"
)
ERROR_PROCESSING_JSON_MSG: Final = "Couldn't process restaurant data:"
