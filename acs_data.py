import requests
import csv

host = 'https://api.census.gov/data'
year = '/2021'
dataset_acronym = '/acs/acs5/subject'
g = '?get='
variables = 'NAME,S0601_C01_047E,S1901_C01_013E,S2301_C02_021E'
location = '&for=zip%20code%20tabulation%20area:*'

usr_key = '&key=1d3748d4ccd17dcf4b92ba12fc4689db8605193e'

query_url = f"{host}{year}{dataset_acronym}{g}{variables}{location}{usr_key}"

# Use requests package to call out to the API
response = requests.get(query_url)
# Convert the Response to text and print the result
print(response.text)

with open('acs_data.csv', 'w') as f:
        writer = csv.writer(f)
        for item in response:
            writer.writerow(item)

