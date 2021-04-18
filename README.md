# Assignment - relay server with a cache

For the position as system developer with operational responsibility.

With reference number: AN 2.2.1-283-21

Submission by Teodor Wojcik

<details>
<summary>Instructions for the required tasks</summary>
<p>

## Task 1

There is an API for [lunch menus at restaurants close to Scilifelab](https://menu.dckube.scilifelab.se/) available at
https://menu.dckube.scilifelab.se/api/.

_The restaurants are closed on weekends, so it is best to test it on weekdays._

**Note that the API has a rate limit and might be slow.**

Write a http server in Python 3 to provide an API relay,
i.e. a web server that relays queries to the backend. That is, a
request to URI `/URI` will result in a query to
`https://menu.dckube.scilifelab.se/api/URI` and the response will
be copied from there.

Please provide not only working but acceptable code. In this case that
includes an appropriate level of documentation, testing, and so on.

You do not need to write your server from scratch but are free to
build on libraries included with Python as well as other frameworks.

We expect to be able to deploy your solution by following the
instructions provided by you.

## Task 2

Build a container for the server provided (free choice of container
engine). Provide appropriate files for building/running the container
as well as instructions intended for a developer for how to build and run.

## Task 3

Provide a shell tool in your favourite language (shell solutions are
acceptible) that takes a restaurant as argument and lists current dishes
available there. Feel free to design the listing however you wish but
it should be clear where to go to eat a certain dish.

## Optional tasks

If you want more, there are some optional tasks below. It is not required to solve these,
but providing solutions is meritorious.

### Optional: Enable threading

Make sure the server is multi-threaded, i.e. it can accept and
process additional requests while working to fulfill
other requests (e.g. by waiting for a request to the back end).

### Optional: Provide caching

Enable caching.

### Optional: Run load tests and provide a capacity estimate

**Make sure you have already implemented caching, as you may otherwise use up all the CPU credit for the API.**

Run load tests (using a single URI) and provide an estimate of how
many requests your relay can handle in a given time frame. Also
provide any analysis done and any thoughts on scaling you may have.

## How to submit

Add and commit as you go. For this assignment it's fine to push to
master or work in branches with PRs/merges.

Please don't forget to push to the repository at GitHub. Also please
tag with completed (if you work with the GitHub web, you will need to
create a release for this, which can be done from the repository main
page).

</p>
</details>

## Quick overview

To spin up the relay server, redis cache and redis insights do:

```sh
git clone git@github.com:NBISweden/devops-umu-teodortymon.git
cd devops-umu-teodortymon
make run-dev
```

Then open [http://localhost:80/docs](http://localhost:80/docs) to access the api documentation.

<p align='center'>
<img src='https://gist.githubusercontent.com/teodortymon/ca06a50eaf7f58b6316bed5477a21ee6/raw/fe4b6c2b5a2709fa827fd34c4d5b1bd789cbb458/NBIS_cast.svg' width='600' alt='make run-dev'>
</p>

## Relay server

Relay server is based on [FastAPI](https://fastapi.tiangolo.com).

<details>
<summary>Reasoning</summary>
<p>

- Since operations will be mostly I/O bound, leveraging asyncronity could provide a siginificant speedup compared to a standard WSGI (ex. Flask). [(Benchmarks)](https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=v2qiv3-db&a=2)

- Great documentation that hints at a nice level of conventions and sensible defaults, but also a possibility to dig deeper in the stack by directly calling the underlying [Starlette](https://www.starlette.io).

- Auto generated interactive api schema documentation can be accessed at thanks to [Swagger U](https://github.com/swagger-api/swagger-ui)

- Since this assignment is at its' core quite straightforward, I though it would be a great opportunity to try something new and hyped by the Python community.
</p>
</details>

### Live versions

- Server can be accessed at a small GoogleCloudEngine instance at: [http://34.67.173.3](http://34.67.173.3)
- API schema docs at: [http://34.67.173.3/docs ](http://34.67.173.3/docs)
- Redis insights at: [here](http://34.67.173.3:8001/instance/b9c013d1-8b76-41ec-a233-60622c2584d6/browser/?db=0&search=%2A)

#### Code structure

```
.
├── Dockerfile              -> Used to create the relay image
├── README.md
├── app
│   ├── __init__.py
│   ├── main.py             -> Server entrypoint code
│   └── models.py           -> Used for validating data and creating API docs
├── cli
│   ├── __init__.py
│   ├── error_msgs.py
│   ├── main.py             -> Typer App with bells & whistles
│   ├── requirements.txt
│   └── simple_lunch.sh     -> Maximizes OS compability without dependencies
├── config.yml              -> Holds URL, PATHs and cache TTL configs
├── docker-compose-dev.yml  -> Live reload with mounted local volume
├── docker-compose.yml      -> Production ready with auto thread scaling
├── makefile                -> Holds useful container management macros
├── requirements.txt
└── tests
    ├── __init__.py
    ├── app
    │   ├── __init__.py
    │   └── test_main.py
    ├── cli
    │   ├── __init__.py
    │   └── test_main.py
    ├── locustfile.py
    └── test_constants.py
```

### Endpoints

There are three endpoints:

1. `/relay_anything/{query}` which accepts any type of path string and relays the response from the menu.dckube server. It is the simplest implemementation in 10 lines of code and it satisfies the assignment requirements (although for simiplicity I opted for always returning responses in a "text" format)

As a warm up & exercise in using type hints, type validations and Pydantic two other endpoints were implemented. There's a considerate amount of code overhead for such a small project and in a production scenario for a simple relay option 1. would be completely sufficient.

2. `/restaurant` which lists all the available restaurants
3. `/restaurant/{restaurant_id}` which lists queried restaurants menu & detailed information

Code is formatted by [`black`](https://black.readthedocs.io/en/stable/) & statically type checked by [`mypy`](http://mypy-lang.org).

### Docker containers

Docker compose is used to orchestrate the:

- relay server as `relay` on `:80`
- redis cache as `redis` on `:6379`
- redis insights as `redis-insights` on `:8001` for easy cache monitoring

### Running

There is a `makefile` that contains commands for interacting with the server.

```
run-prod: ## Run containers with worker count optimized to available CPUs
	docker compose up

run-dev: ## Run containers in development mode with code reloading and /app volume mounted in local workspace for active development
	docker compose -f docker-compose-dev.yml up

test: ## Run mypy & pytests. Spin up all the containers in dev mode first as integration tests rely on redis cache and local test files
	docker compose exec web pytest
	docker compose exec web mypy */*.py

shell: ## Atttach a bash shell to the relay container
	docker exec -it relay /bin/bash

rebuild: ## Rebuild all containers
	docker compose build --force-rm --no-cache
```

If you want to modify relay code, execute `make run-dev` as it will mount the the current directory in the container allowing you to run new code directly in the container.

### Testing

Based on FastAPI documentation recommendations and my own past experience I've chosen [Pytest](https://docs.pytest.org/en/6.2.x/) for the testing framework. Easiest way to run tests is to:

1. `make run-dev` to first spin the containers in dev mode as integrations tests rely on redis
2. `make test` which will execute `pytest` inside the containers testing the relay, cache & cli. Type checking by Mypy is also a part of the command.

### Running manually

It is recommended to run `docker compose -f docker-compose-dev.yml` or `make run-dev` as that will also spin up the redis cache which the relay relies on but if you'd would wish to run just the server with a single worker and reload on code change:

```

pip install -r requirements.txt
uvicorn main:app --reload

```

## CLI

There are two ways to interact with the API from the shell:

1. By using `./cli/simple_lunch [restaurant_id OR no argument for restaurant listing]` which strives to maximize compatibility with any OS by using only curl for API calls and inlined python json.load for formatting.
2. By running a full fledged Typer shell app:

   ```

   pip3 install cli/requirements.txt
   python3 -m cli.main

   ```

## Extra tasks & rationales

### Cache

For caching I chose [Redis](https://redis.io) as it's one of the most popular production caching solutions. I could have went with simpler solutions that would have resulted in a slightly easier implementation (like [memcached](https://memcached.org) or some in memory solutions).

I used a simple layer on top of [aioredis](https://aioredis.readthedocs.io/en/v1.3.1/) (important for using only async methods and preserving async performance) for FastAPI provided by [fastapi-cache](https://pypi.org/project/fastapi-cache/) that mostly just abstracts an easier to use cache object for FastAPI routes. I made sure to check that package had quite good test coverage, clean code and was actively maintained.

### Multi threading

By implementing only `async` methods and using an ASGI stack ([Uvicorn](https://www.uvicorn.org), [Starlette](https://www.starlette.io) and [FastAPI](https://fastapi.tiangolo.com)), there are no blocking methods and a decent speedup with low developer effort is achieved compared to WSGI stacks [(benchmarks)](https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=v2qiv3-db&a=2). Production image will start the relay with the same amount of workers as available CPU cores. More information in [documentation](https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker#workers_per_core).

### Load tests

Load tests are orchestrated by [Locust](https://docs.locust.io/en/stable/) from `tests/locustfile.py`.

1. Consistently increasing 0->500RPS in ~10RPS intervals.

   The server can fault free handle up to ~600 RPS/instance until it becomes throttled down. My first guess would be that the external API is rate limiting the relay.
   ![Throttling](https://i.imgur.com/UjVfQZ2.png)

   Also it's worth noting that on GKE the less expensive CPU units are only allowed to "burst" ([docs](https://cloud.google.com/compute/docs/machine-types#machine_types)) to increase the processing for a short period of time. That could also contribute to throttling especially when compared to the CPU metrics which show ~300% usage spikes followed by rapid drops.

2. Cold boot, empty cache, high load

   Running a concentrated swarm of 1000 users through 20 workers and spinning RPS from 0 to ~500 results in a server worker crash. I guess that the next step would be attaching some log & crash reporting service to the server to get rudimentary observability. It would also be worth the investigating other factors such as the number of open connections, memory and disk I/O and bandwidth of the instance
