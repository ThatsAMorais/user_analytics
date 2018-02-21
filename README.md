# User Analytics API
A basic user analytics API backed by TimescaleDB / PostgreSQL

## Overview

As storing high volume time series data has become more prevalant in tech, it has become dogma to use NoSQL databases due to the discovery that write throughput can drop significantly with traditional relational databases as the dataset grows. Because writes are done as a batch update to the tree, NoSQL improves on throughput. However, it increases memory requirements, and poor secondary index support.

I discovered TimescaleDB, an open-source time-series database, through research of the topic of time series storage. My experience was with using DynamoDB, so I was fascinated to get a second opinion. By chunking out ranges of timestamped data, the concerns over write time are
drastically reduced. The functionality is abstracted via a PostgreSQL extension so writes and queries feel like writing to one big table.

## Installation

I presume you have Docker installed, but if not, you'll need docker and docker-compose support to pull, build, and run the software containers

1. Clone the repo: https://github.com/ThatsAMorais/user_analytics
1. `docker-compose up --build`

Everything else will be arranged for you. Once the flask app has started you can send requests.

## Backend

The API is written as a simple flask application with two endpoints. Flask was chosen because of the small size of this project.

The data store is a TimescaleDB which is uniquely suited for storing time series data.

local development was containerized via Docker for ease of sharing and maintenance.

## API

Testing the API can be done via Postman, cURL, or even a request lib of your choice in a repl shell.

The following are some cURL commands exported from Postman to make testing easier. If `localhost` for some reason does not work due to how docker is setup on your machine, try `192.168.99.100`, or whatever your docker VM's IP is.

### POST

**Click**
```
curl -X POST \
  'http://localhost:8080/analytics?timestamp=1224567997&user=3&event=click' \
  -H 'cache-control: no-cache' \
  -H 'postman-token: 0c01e981-587b-af2a-17ba-8f635354b076'
```


**Impression**
```
curl -X POST \
  'http://localhost:8080/analytics?timestamp=1224567998&user=1&event=impression' \
  -H 'cache-control: no-cache' \
  -H 'postman-token: 0c01e981-587b-af2a-17ba-8f635354b076'
```

If the user does not exist, one is added by the ID provided. Then, the event is stored
associated to that user.

The endpoint always returns 204, no matter what is given to it, invalid or otherwise, as the design requested. Error codes for those cases can be added in the future.


### GET

curl -X GET \
  'http://localhost:8080/analytics?timestamp=1224567999' \
  -H 'cache-control: no-cache' \
  -H 'postman-token: 1a236642-247e-bcec-fd63-c9d1e685540e'

Response:
```
unique_users,2
clicks,1
impressions,1
```

A query for a timestamp will retrieve data from that time stamp, going back an hour. The response includes all clicks and impressions from that range, and the number of unique users responsible for those particular rows.

## Future Work

 * Report a more robust set of fields in queries. 
 * Use JSON so the responses are more easily digestable by clients.
 * Test coverage - TDD would be my usual approach
 * Deploy to scalable infrastructure where clients may begin posting analytics
 * Tap into a broader Identity system where this data collection can be mapped to existing profiles
 