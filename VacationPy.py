import os
import pandas as pd
import matplotlib.pyplot as plt
from api_keys import api_keys
from os.path import exists
import requests
pd.set_option('display.max_columns', None)

if not exists("Resources/Hotel_Data.csv"):
    keys = api_keys()

    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
    # location=-33.8670522,151.1957362&    #(lat, long)#
    # radius=5000&
    # type=lodging&
    # keyword=hotel&
    # key=keys.get_google thinhhhe

    raw_data = pd.read_csv("Resources/Weather_Data.csv")

    # Filter the data to only get cities with 60-80 degrees, wind speed less than 10, 0 cloudiness
    data = raw_data[(raw_data["Temperature (Fahrenheit)"] >= 60) & (raw_data["Temperature (Fahrenheit)"] <= 80)]
    data = data[data["Wind Speed (mph)"] <= 10]
    data = data[data["Cloudiness"] == 0]
    plt.scatter(raw_data["Longitude"], raw_data["Latitude"])
    # plt.show() Todo undo comment here
    print(data.head(26))
    hotel_name = []
    hotel_city = []
    hotel_country = []
    bad_cities = []
    for x in range(len(data)):
        try:
            lat = data["Latitude"].tolist()[x]
            long = data["Longitude"].tolist()[x]
            request = requests.get(
                f'{url}location={lat},{long}&radius=5000&type=lodging&keyword=hotel&key={keys.get_google_key()}'
            ).json()
            hotel_country.append(request["results"][0]["plus_code"]["compound_code"].split(",")[1])
            hotel_city.append(data["City"].tolist()[x])
            hotel_name.append(request["results"][0]["name"])
        except Exception as e:
            print(f'{x} index gives Foogle an issue! Will not be adding in a hotel for {data["City"].tolist()[x]}')
            bad_cities.append(x)

    print(f'Hotel_Name length = {len(hotel_name)}')
    print(f'Hotel_City length = {len(hotel_city)}')
    print(f'Hotel_Country length = {len(hotel_country)}')

    hotel_df = pd.DataFrame({
        "Hotel Name": hotel_name,
        "Hotel City": hotel_city,
        "Hotel Country": hotel_country
    })
    hotel_df.to_csv("Resources/Hotel_Data.csv", index=False)


