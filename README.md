# Assignment

For the position as system developer with operational responsibility.

With reference number: AN 2.2.1-283-21

A pull request will automatically be created on your repository that you can use for questions and to request feedback.

## Task 0

Please update this readme by:
- deleting this section
- adding your name

Example: **Kalle Kråka**

## Task 1

There is an API for [lunch menus at restaurants close to Scilifelab](https://menu.dckube.scilifelab.se/) available at
https://menu.dckube.scilifelab.se/api/.


*The restaurants are closed on weekends, so it is best to test it on weekdays.*

**Note that the API has a rate limit and might be slow.**

Write a http server in Python 3 to provide an API relay,
i.e. a web server that relays queries to the backend. That is, a
request to URI `/URI` will result in a query to
`https://menu.dckube.scilifelab.se/api/URI` and the response will
be copied from there.

Please provide not only working but acceptable code. In this case that
includes an appropiate level of documentation, testing, and so on.

You do not need to write your server from scratch but are free to
build on libraries included with Python as well as other frameworks.

We expect to be able to deploy your solution by following the
instructions provided by you.


## Task 2

Build a container for the server provided (free choice of container
engine). Provide appropiate files for building/running the container
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
