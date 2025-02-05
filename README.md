# Vehicle Routing 

This repo contains setup instructions and some code to get a Vehicle Routing (VRP) solver up and running on your machine. I have only implemented the [Clarke-Wright Savings and Sweep Algorithm](https://web.mit.edu/urban_or_book/www/book/chapter6/6.4.12.html) which are run sequentially to find a semi-optimal trip plan. Additionally, I have included the PyVRP package in case it can come up with something better than the existing implemented methods. This is done because VRP is NP-Hard and it's not clear if there's one perfect solution, but none of these are.

Currently, this repository only supports modifying the maximum trip distance and maximum trip length. The motivation for this is personal since I only wrote this to optimize visiting multiple trails in one day for the smallest distance which I thought would put the least wear on my car.

For some reason, the Sweep algorithm tends to give the best results. However, sometimes it does worse for larger `max stops` values, so the program will consider maximum stops from the provided value to 1. In the event where the maximum trip distance is too low and makes Sweep and PyVRP ineffective (since they won't consider invalid routes), Clarke-Wright was considered "optimal" which has now been changed by removing those points before analysis and re-adding them later.

Setup involves downloading and processing OSRM data which may require a lot of RAM for maps larger than a US state. Follow the instructions [here](https://github.com/Project-OSRM/osrm-backend) to self-host the OSRM backend. If you do not want to do that, you can replace `HOST_IP` with the official OSRM API. It is preferred to download the map locally since the OSRM API is slow and you may want to add or remove points, but if you are just testing the program the API is fine.

# Usage

Create a file `coords.txt` and fill each line with a latitude-longitude pair in the format `lat, lon`. The first coordinate must be the depot. The indices into `coords.txt` are used extensively by this program and that is what the integers represent in the output. You can have a file named `names.txt` (or whatever you prefer) and each name must correspond to each respective coordinate in the file.

On Debian, you will want to create a virtual environment with `python3 -m venv venv` and then install the requirements with `venv/bin/pip3 install -r requirements.txt`. On Windows, just do `pip install -r requirements.txt`.

To create the distance matrix, run `scripts/distance_matrix.py` and pass the coordinate file path to it as argument. This may take a while if you are using the API. Once this has been generated, pass the file path to calls to `vrp.py` and it will use the calculated route distances.

Here's how you run the program if you did everything aforementioned:

```
venv/bin/python3 src/vrp.py coords.txt distance_matrix.txt 45.0 3
```

Where 45.0 is the maximum roundtrip distance and 3 is the maximum number of stops on the route excluding the depot. Additionally, add `-h names.txt` if you want it to print the result in a human-readable format.

# Licensing

All works made here are licensed under GPL v3.
