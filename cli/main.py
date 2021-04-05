import requests
import typer
from typing import Optional
from yaspin import yaspin
import constants

# Temporary install instructions:
# pip3 install typing typer yaspin requests or pip3 install -r requirements.txt
# python3 main.py

app = typer.Typer()


@app.command()
def main(
    restaurant_id: Optional[str] = typer.Argument(
        None, help="ID of the restaurant to do a direct query"
    )
):
    """
    Query teodortymon.lunch to see the latest lunches.

    Provide RESTAURANT_ID to query the restaurant directly
    or run without any arguments to see all the available restaurants.
    """

    if restaurant_id is None:
        chosen_restaurant = list_all_and_pick_one_restaurant_id()
        show_menu(chosen_restaurant)
    else:
        show_menu(restaurant_id)


def list_all_and_pick_one_restaurant_id():

    restaurants = decode_all_restaurants(request_all_restaurants())

    for index, restaurant in enumerate(restaurants):
        typer.echo(f'{index}) {restaurant["name"]} {restaurant["campus"]}')

    # TODO: Allow users to choose a number range e.g 1-3 or 1,2,3
    chosen_restaurant_index = int(typer.prompt("Choose a restaurant [number]"))
    restaurant_id = restaurants[chosen_restaurant_index]["identifier"]
    return restaurant_id


def request_all_restaurants():
    with yaspin(text="Loading all restaurants", color="yellow") as spinner:
        try:
            response = requests.get(constants.URL)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            spinner.write(
                f"{constants.ERROR_REQUEST_MANY_RESTAURANTS_MSG} \n  {repr(e)}"
            )
            spinner.fail("[Failed]")
            raise typer.Exit(code=1)
        else:
            spinner.ok("[Success]")
    return response


def decode_all_restaurants(data):
    try:
        restaurants = data.json()["restaurants"]
    except ValueError as e:
        typer.echo(f"{constants.ERROR_PROCESSING_JSON_MSG}\n {repr(e)}")
        raise typer.Exit(code=1)
    else:
        return restaurants


def request_restaurant(restaurant_id: str):
    with yaspin(text=f"Loading {restaurant_id}", color="yellow") as spinner:
        try:
            response = requests.get(constants.URL + restaurant_id)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            spinner.write(
                f"\n{constants.ERROR_REQUEST_ONE_RESTAURANT_MSG}"
                f"\n  {repr(e)}"
                f"\n{constants.ERROR_VALID_ID_MSG}"
            )
            spinner.fail("[Failed]")
            raise typer.Exit(code=1)
        else:
            spinner.ok("[Success]")
    return response


def decode_restaurant(data):
    try:
        # TODO: Implement data validation provided by Pydantic
        restaurant = data.json()["restaurant"]
    except ValueError as e:
        typer.echo(
            f"{constants.ERROR_PROCESSING_JSON_MSG}"
            f"\n{repr(e)}"
            f"\n{constants.ERROR_VALID_ID_MSG}"
        )
        raise typer.Exit(code=1)
    else:
        return restaurant


def show_menu(restaurant_id: str):
    restaurant = decode_restaurant(request_restaurant(restaurant_id))

    typer.echo(f'\n{restaurant["title"]}' f"\n---")

    menu_list = restaurant["menu"]
    if not menu_list:
        typer.echo("No menu published for today")
    else:
        for i in menu_list:
            typer.echo(f'{i["dish"]}')

    typer.echo(
        f"---"
        f'\nWebsite: {restaurant["url"]}'
        f'\nDirections: {restaurant["map_url"]}'
        f"\nID: {restaurant_id} (You can use this ID to query the restaurant directly"
        f' e.g. "lunch-scifi {restaurant_id}")'
    )


if __name__ == "__main__":
    typer.run(app())
