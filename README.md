# Njuskalo GPU API

This is API, that fetches GPUs, from [Njuskalo](https://www.njuskalo.hr/), njuskalo is second hand marketplace for everything, but this is program made to specifically fetch GPUs, that can be used for mining, this started as simple project to fetch data for price analysis of GPUs around Croatia.

## Running API
To run API for yourself run:
```
pip3 install -r requirements.txt
python3 api.py
```

This will open API on localhost on port 5000, you can see it [here](http://localhost:5000/)

## Endpoints

These are endpoints for API

### http://localhost:5000/

This is root of API, calling this will return all GPUs on njuskalo, API automatically filters for GPUs capable of mining, if you want to see all GPUs, whether they can or can't mine, pass `?filter=false`, this endpoint has cache because of it's size and time needed to find all results.


### http://localhost:5000/locations

This will always return same data, this returns names of locations and their IDs, purpose of this endpoint is to help with integration, so you can easily see what location responds to what ID

### http://localhost:5000/api

This is endpoint that is used most, params are next:
```
min : minimum price in Kn, type: int
max : maximum price in Kn, type: int
locationID : location id that can be gotten from locations endpoint, type: int
filter: should program filter GPUs for ones that can mine, type: bool
search: GPU to search for, type: str
```
