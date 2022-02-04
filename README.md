# geo_encoder_google
Application to get the lat and lon values of an adress via the google maps api.

# How to use
1. Add your csv file into the folder input_data, the csv file needs the columns street, zip_code, lat and lon. If you want to get the data for a street/zip_code combination
 add the value 'no data' for the lat and lon column.<br/>
2. Change the command in the run.bat.<br/>
3. Add your API key to the config.properties file.<br/>
4. Run the bat file.<br/>

# Libraries
Pandas, jproperties
