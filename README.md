# Vehicle Routing 

This repo contains setup instructions and some code to get a Vehicle Routing (VRP) solver up and running on your machine. I have only implemented the [Clarke-Wright Savings and Sweep Algorithm](https://web.mit.edu/urban_or_book/www/book/chapter6/6.4.12.html) which are run sequentially to find a semi-optimal trip plan.

Setup involves downloading and processing OSRM data which may require a lot of RAM for maps larger than a US state. Follow the instructions [here](https://github.com/Project-OSRM/osrm-backend) to self-host the OSRM backend. If you do not want to do that, you can replace `HOST_IP` with the official OSRM API. It is preferred to download the map locally since the OSRM API is slow and you may want to add or remove points.

# Licensing

All works made here are licensed under GPL 3.
