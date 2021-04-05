from typer.testing import CliRunner

from main import app
import constants

runner = CliRunner()


def test_valid_restaurant_id():
    result = runner.invoke(app, [constants.RESTAURANT_ID["valid"]])
    assert result.exit_code == 0
    assert constants.VALID_RESTAURANT_TITLE in result.stdout
    assert constants.SAMPLE_DISH_NAME in result.stdout


def test_invalid_restaurant_id():
    result = runner.invoke(app, [constants.RESTAURANT_ID["invalid"]])
    assert result.exit_code == 1
    assert constants.ERROR_REQUEST_ONE_RESTAURANT_MSG in result.stdout


def test_successful_load_of_all_restaurants():
    result = runner.invoke(app, input="0\n")
    assert result.exit_code == 0
    assert "0)" in result.stdout


# TODO: Add failing tests for many restaurants and invalid JSONs
