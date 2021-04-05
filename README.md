# Assignment

For the position as system developer with operational responsibility.

With reference number: AN 2.2.1-283-21

A pull request will automatically be created on your repository that you can use for questions and to request feedback.

## Task 0

Teodor Wojcik

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

### Solution

Relay server is based on [FastAPI](https://fastapi.tiangolo.com). Since operations will be mostly I/O bound, using ASGI stack with full asyncrosity could provide a siginificant speedup compared to standard WSGI (ex. Flask).

Server can be accessed at a small GoogleCloudEngine instance at [http://34.67.173.3](http://34.67.173.3)

Interactive api schema documentation can be accessed at [http://34.67.173.3/docs ](http://34.67.173.3/docs) (thanks to [Swagger U](https://github.com/swagger-api/swagger-ui)) or if run locally at `localhost/docs`

Redis insights can be accessed at [here](http://34.67.173.3:8001/instance/b9c013d1-8b76-41ec-a233-60622c2584d6/browser/?db=0&search=%2A)

There are three endpoints:

1. `/relay_anything/{query}` which accepts any type of path string and simply relays the response from the menu.dckube server. It is the simplest implemementation in 10 lines (but if I haven't used `black` formatter, then it could probably 3)

Other two endpoints are implemented with OpenAPI schema definitions, type validation & type hints:

2. `/restaurant` which lists all the available restaurants
3. `/restaurant/{restaurant_id}` which lists queried restaurants menu & detailed information

Surely it's an overkill, but it was fun to implement.

Code is formatted by `black` & statically type checked by `mypy`.

### Instructions

It is recommended to run `docker compose up` as that will also spin up the redis cache which the code relies on, but if someone would wish to run just the server with a single worker and reload on code change:

```
pip install -r requirements.txt
uvicorn main:app --reload
```

## Task 2

Build a container for the server provided (free choice of container
engine). Provide appropriate files for building/running the container
as well as instructions intended for a developer for how to build and run.

### Solution

Docker compose is used to orchestrate the:
* relay server as `relay` on port: `80`
* redis cache as `redis` on port: `6379`
* redis insights as `redis-insights`: on port `8001` for easy cache monitoring

### Instructions

* For production:
```
docker compose up
```

* For development:
```
docker compose -f docker-compose-dev.yml up
```
This will enable reload on code change and will mount `/app` as a volume to allow direct development on the running container

## Task 3

Provide a shell tool in your favourite language (shell solutions are
acceptible) that takes a restaurant as argument and lists current dishes
available there. Feel free to design the listing however you wish but
it should be clear where to go to eat a certain dish.

### Solutions

There are two ways to interact with the API from the shell:
* First one is a small bash script `./cli/simple_lunch [restaurant_id OR no argument for restaurant listing]` which strives to maximize compatibility with any OS by using only curl for API calls and inlined python json.load for formatting.
* Second one is running a full fledged Typer shell app by

```
cd cli/
pip3 install typing typer yaspin requests
python main.py
```

## Optional tasks

If you want more, there are some optional tasks below. It is not required to solve these,
but providing solutions is meritorious.

### Optional: Enable threading

Make sure the server is multi-threaded, i.e. it can accept and
process additional requests while working to fulfill
other requests (e.g. by waiting for a request to the back end).

### Solutions

By implementing only `async` methods (e.g. redis cache interface is based on [aioredis](https://aioredis.readthedocs.io/en/v1.3.1/) and using an ASGI stack ([Uvicorn](https://www.uvicorn.org), [Starlette](https://www.starlette.io) and [FastAPI](https://fastapi.tiangolo.com)), there are no blocking methods and a decent speedup with low developer effort is achieved compared to WSGI stacks [(benchmarks)](https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=v2qiv3-db&a=2)


### Optional: Provide caching

Enable caching.

### Solutions

Caching provided by redis.

### Optional: Run load tests and provide a capacity estimate

**Make sure you have already implemented caching, as you may otherwise use up all the CPU credit for the API.**

Run load tests (using a single URI) and provide an estimate of how
many requests your relay can handle in a given time frame. Also
provide any analysis done and any thoughts on scaling you may have.

### Solutions

Load tests are orchestrated by Locust and the server can fault free handle up to ~600 RPS/instance until it becomes
throttled down. GCE enforces every 100 seconds a maximum rate per project of 
[20 requests/second](https://cloud.google.com/compute/docs/api-rate-limits)
which means that around every 1,5min relays server could get throttled if it would go beyond the limit.
Picture below illustrates that it could be the case:
![Throttling](https://i.imgur.com/UjVfQZ2.png)

Also, the less expensive CPU units are allowed to "burst" ([docs](https://cloud.google.com/compute/docs/machine-types#machine_types))
to increase the processing for a short period of time. 

That could contribute to a certain vulnerability in cases of sudden spikes in requests, especially on cold boot & empty cache.
Indeed Locus tests confirm this. Running a concentrated swarm of 1000 users through 20 workers and 
spinning RPS from 0 to ~500 results in a server worker crash. I guess that the next step would be attaching 
some log & crash reporting service to the server to get rudimentary observability and chipping out money for 
private instances. It would also be worth the investing other factors such as the number of open connections, maybe memory and disk I/O, bandwidth of the instance and API quotas.



## How to submit

Add and commit as you go. For this assignment it's fine to push to
master or work in branches with PRs/merges.

Please don't forget to push to the repository at GitHub. Also please
tag with completed (if you work with the GitHub web, you will need to
create a release for this, which can be done from the repository main
page).

```

```

```

```
