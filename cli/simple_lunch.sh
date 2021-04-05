#!/usr/bin/env bash

URL="https://menu.dckube.scilifelab.se/api/restaurant/"

if [ $# -eq 0 ]; then
  curl "$URL$1" | python -mjson.tool
else
  response=$(curl -s "$URL$1/")
  if [[ ${response:0:1} == "{" ]] ; then
    echo $response | python -c 'import sys, json
response=json.load(sys.stdin)["restaurant"]
print(response["title"])
for i in response["menu"]:
  print(i["dish"])
print(response["map_url"])
print(response["url"])'
  else
    echo "Sorry, I can't find any restaurant of that id";
  fi
fi