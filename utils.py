# Note: this Utils file was for code testing and data cleaning purposes only
# Most of it is commented out for privacy of API keys
# Also commented for reduced API data fetching and the removal of original discord data which I did not want to share
# (Some messages may have contained private or sensitive information which I cannot share)
# - Samuel Sovi

import pandas as pd #used for pandas objects like DataFrames
import numpy as np # used for functions like finding mean
import matplotlib.pyplot as plt # used for graphing
import scipy as scipy # Not sure if every machine has scipy built in to python tbh
from scipy import stats # used for ttest
import json # used for reading json
import requests # used for handling requests for APIs (MapQuest)
from sklearn.model_selection import train_test_split 
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.tree import plot_tree

'''
data = pd.read_csv("messages.csv", index_col="ID")
data2 = data.dropna(how="any",subset=["Timestamp"])
data2 = data2.drop(columns=["Attachments"])
data2["Contents"] ="placeholder text"
data2["Timestamp"] = data["Timestamp"].str[:10]
data2["Timestamp"] = data["Timestamp"].str[:4] + data["Timestamp"].str[5:7] + data["Timestamp"].str[8:10]
#data2["Timestamp"]

data2.set_index("Timestamp")
data2.to_csv("messages_cleaned.csv")
#data2.sort_values(by=["Timestamp"], ascending=False)


data3 = data2.value_counts()
data2["Timestamp"] = data2["Timestamp"].str[:4] + "-" + data2["Timestamp"].str[4:6] + "-" + data2["Timestamp"].str[6:8]

data3 = pd.DataFrame(data3)
#data3 = data3.drop("Contents")

print(data3.head())

data3.sort_values(by=["Timestamp"], ascending=False)
data3.to_csv("counts.csv")
'''

'''
data = pd.read_csv("msg_counts.csv",index_col="Timestamp")
data2 = data.drop(columns=["Contents"])
#data2["Timestamp"] = data2["Timestamp"].astype(int)

#data2.sort_values(by=["Timestamp"])

#print(type(data2["Timestamp"][0]))

data2 = data2.sort_index()

data2.to_csv("msg_by_day.csv")
'''


'''
data2 = pd.read_csv("msg_by_day.csv", index_col="Count")
data3 = data2
data3 = data3.astype({"Timestamp": str})
#data3.dtypes()
#data3["Timestamp"].to_string()


data3["Timestamp"] = data3["Timestamp"].str[:4] + "-" + data3["Timestamp"].str[4:6] + "-" + data3["Timestamp"].str[6:8]

data3.set_index("Timestamp")
#data3 = data3.drop(1)

data3.to_csv("temp.csv")

data4 = pd.read_csv("temp.csv", index_col="Timestamp")
data4.to_csv("temp.csv")
'''

# Working with Meteostat

'''
req_string = "https://www.mapquestapi.com/geocoding/v1/address?key=<removed>&location=San+Jose"

# Using the user-entered city, make a request to MapQuest to get the city's latitude and longitude
# Use the API key we made in class for MapQuest

data_string = requests.get(req_string)

data = json.loads(data_string.text)

results_list = data["results"]
location = results_list[0]["locations"][0]

# Extract the city's latitude and longitude. Store these in variables.

latitude = str(location["latLng"]["lat"])

longitude = str(location["latLng"]["lng"])


# Using the latitude and longitude variables, make a request to MeteoStat to 
# get the coordinates' station ID
# Extract the city's weather station ID. Store this in a variable.

url = "https://meteostat.p.rapidapi.com/stations/nearby"
querystring = {"lat":latitude,"lon":longitude}

headers = {
    'x-rapidapi-host': "meteostat.p.rapidapi.com",
    'x-rapidapi-key': "N0_U51NG_MY_K3Y"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

data = json.loads(response.text)
id = data["data"][0]["id"]

# Using your weather station ID variable, get daily weather data for the 
# previous year (2021-02-21 through 2022-02-20)
# Set the units to be imperial to get Fahrenheit instead of Celsius

url = "https://meteostat.p.rapidapi.com/stations/daily"
querystring = {"station":id,"start":"2019-01-01","end":"2021-07-20", "units": "imperial"}


response = requests.request("GET", url, headers=headers, params=querystring)

data = json.loads(response.text)


# Structure this data nicely into a pandas' DataFrame
# Write the DataFrame to a csv file using the filename convention: 
# <city name>_daily_weather.csv

data_df = pd.DataFrame(data["data"])
data_df.set_index("date", inplace=True)

# Clean the DataFrame so there are no missing values
# Remove columns with more than 50% of data missing

data_df = data_df.dropna(axis=1, thresh=int(50/100*data_df.shape[1]+1))

# Fill the remaining missing values
# "Middle" values should be filled with linear interpolation (see interpolate())

data_df = data_df.interpolate(method = "linear")

# Since you can't interpolate the first or last values if they are missing, using 
# backfilling and forward filling appropriately (see fillna())

data_df = data_df.ffill().bfill()

# Write the cleaned DataFrame to a csv file using the filename convention: 
# <city name>_daily_weather_cleaned.csv
csv_name = "San_Jose_daily_weather_cleaned.csv"
data_df.to_csv(csv_name)
'''

