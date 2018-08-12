# McDonald's Restaurant Finder
Python Script designed to find McDonald's restaurants within Spain.

Consider the store network of McDonald’s in Spain.
You can find the relevant page here:
https://www.mcdonalds.es/restaurante/buscador

Customizable parameters (settings.py):

- city
- radius 
- CHROME_PATH

This script currently supports the Google Chrome web browser exclusively.
You can download its driver here:
http://chromedriver.chromium.org/

In this exercise, we extract all McDonalds restaurants within 50 km around
Madrid. 
For each store, we extract the attributes:

- Name
- Address
- Coordinates (latitude/longitude)
- Phone number

We then save the information in a structured way; using a CSV file to do so. 

The geolocation coordinates are obtained using the Goggle Geolocation API.
You can find it here:
https://developers.google.com/maps/documentation/geolocation/intro

