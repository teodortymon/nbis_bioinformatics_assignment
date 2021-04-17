import yaml
from locust import HttpUser, between, task  # type: ignore

config = yaml.safe_load(open("config.yml"))

restaurants = ["haga", "rudbeck", "hjulet", "jons"]


class LoadTest(HttpUser):
    wait_time = between(1, 2.5)

    @task()
    def query_all_restaurants(self):
        self.client.get(f"/{config['RESTAURANTS_PATH']}/")

    @task()
    def query_restaurants_one_by_one(self):
        for restaurant_id in restaurants:
            self.client.get(
                f"/{config['RESTAURANTS_PATH']}/{restaurant_id}",
            )
