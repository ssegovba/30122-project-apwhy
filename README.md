# Evictions and Deprivation in Chicago

### Team Members
[Andrew Dunn](https://github.com/andrewjtdunn), [Gregory Ho](https://github.com/GregoryHo88), [Santiago Segovia](https://github.com/ssegovba), [Stephania Tello Zamudio](https://github.com/stephatz)

## Project Summary
This project conducts data analysis to understand the relationship between a deprivation index, constructed using socioeconomic data from a variety of sources, and instances of eviction in the city of Chicago. The python application creates an interactive dashboard which summarizes the relationship betwen the the different factors. Follow the steps below to launch the dashboard.

## To Launch the Application

1. Clone the repository.
```
git clone https://github.com/uchicago-capp122-spring23/30122-project-apwhy
```
2. Navigate to the repository.
```
cd ./30122-project-apwhy
```
3. Install Poetry, which will allow the user to run the application in a virtual environment.
```
poetry install
```
4. Activate the virtual environment in poetry.
```
poetry shell
```
5. [OPTIONAL] Pull data from API's and clean it -- this will take about 10 minutes.
Note that two of the API's need keys to access. We recommend requesting API keys from the Chicago Data Portal and Google Maps API to complete this step.
If you have your own API tokens, navigate to deprivation_evictions, create a constants.py file:
```
cd deprivation_evictions
code constants.py
```
 5b. and paste your API keys in constants.py as follows:
```
GOOGLE_TOKEN = "Your_Google_Token_Here"
API_TOKEN = "Your_Chicago_Data_Portal_Token_Here"
```
 5c. Then, navigate back to the repository and run the following to pull data from the API's and clean it.
```
cd ./30122-project-apwhy
python3 -m deprivation_evictions.data_bases.clean_data.cleaning_data
```
6. Launch the Application.
```
python3 -m deprivation_evictions
```

The IDE may automatically launch a new web browser tab, or may provide a local URL. If the latter, paste it into your browser to view the interactive dashboard.

## For further information on the project:

[Click here for a summary of the project](https://github.com/uchicago-capp122-spring23/30122-project-apwhy/blob/main/proj-paper.pdf)

[Click here for an in-depth description of the methodology](https://github.com/uchicago-capp122-spring23/30122-project-apwhy/blob/main/Methodology.pdf)

## Acknowledgments

Professor: James Turk

Teaching Assistant: Norah Griffin

Data Sources:
- American Community Survey
- Google Maps API
- Chicago Data Portal
- Zillow Real Estate Metrics API
- Law Center for Better Housing Eviction Data for the city of Chicago
