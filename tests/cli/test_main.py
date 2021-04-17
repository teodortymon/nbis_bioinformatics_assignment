from typer.testing import CliRunner

from cli.main import app
from tests import test_constants

runner = CliRunner()


def test_valid_restaurant_id():
    result = runner.invoke(app, [test_constants.VALID_RESTAURANT_ID])
    assert result.exit_code == 0
    assert test_constants.VALID_RESTAURANT_TITLE in result.stdout


def test_invalid_restaurant_id():
    result = runner.invoke(app, [test_constants.INVALID_RESTAURANT_ID])
    assert result.exit_code == 1


def test_successful_load_of_all_restaurants():
    result = runner.invoke(app, input="0\n")
    assert result.exit_code == 0
    assert "0)" in result.stdout
