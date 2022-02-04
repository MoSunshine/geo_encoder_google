# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 10:51:23 2022

@author: moritz.wegener1@gmail.com @TODO kommentare vervollständigen
"""
import pandas as pd
import requests
import logging
import traceback
import json
from jproperties import Properties

class geo_encoder_google():
    
    def __init__(self):
        """
        Standart constructor. Reads the api key from the config files for later use and sets the logger for this class.

        Returns
        -------
        None.

        """
        configs = Properties()
        with open('../config.properties', 'rb') as config_file:
            configs.load(config_file)
            self.api_key = configs.get("api_key").data
        self.logger = logging.Logger('Logging')
        fh = logging.FileHandler("../log/errors.log")
        fh.setLevel(logging.INFO)
        fh.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        self.logger.addHandler(fh)
    
    
    def read_dataset(self,file):
        """
        Reads the file that specified for this run.  

        Parameters
        ----------
        file : striung
            DESCRIPTION.

        Returns
        -------
        dataset : dataframe
            DESCRIPTION.

        """
        path = "../input_data/"+file
        try:
            dataset = pd.read_csv(path, sep=",", encoding="utf-8", dtype={"street":str,"zip_code":str,"country":str,"city":str})
            return dataset
        except Exception as e:
            self.logger.error('Error reading input data ' + file +".")
            self.logger.error(traceback.format_exc())
    
    
    def encode_location(self,file):
        """
        Uses the data from the dataset to build a request to the google maps api. The answere of the request is an json file with the lat and lon value of the location. 
        The methode adds the lat and lon values to the dataset and creats an output csv file.

        Parameters
        ----------
        file : str
            Name of the input file. Also used for the output file.

        Returns
        -------
        None.

        """
        
        dataset = self.read_dataset(file)
        print(dataset)
        dataset.reset_index(inplace=True)
        dataset_for_run = dataset[(dataset["lat"]=='no data') | (dataset["lon"]=='no data')]
        print(dataset_for_run)
        dataset_for_run["search_url"] = "https://maps.googleapis.com/maps/api/geocode/json?address=" + dataset_for_run["street"] + ";components=country:de|postal_code:" +  dataset_for_run["zip_code"] + "&key=" + self.api_key
        url_list = dataset_for_run["search_url"].tolist()
        result_list_lat = []
        result_list_lon= []
        i = 0
        for url in url_list:
            i +=1
            print("Encode "+ str(i) + " of "+ str(len(url_list)))
            try:
                page = requests.get(url).text
                json_object = json.loads(page)
                lat = json_object["results"][0]["geometry"]["location"]["lat"]
                lon = json_object["results"][0]["geometry"]["location"]["lng"]
                result_list_lat.append(lat)
                result_list_lon.append(lon)
            except Exception as e:
                self.logger.error('Error reading url '+url + " of file "+ file)
                self.logger.error(traceback.format_exc())
                result_list_lat.append('no data')
                result_list_lon.append('no data')
        dataset_for_run["lat"] = result_list_lat
        dataset_for_run["lon"] = result_list_lon
        dataset_for_run.drop(["search_url"],axis=1,inplace=True)
        dataset_for_run.to_csv("../result/" +file.replace(".csv","")+"_google_scraped.csv",encoding="utf-8",sep=",",index=False)
        ###merge data###
        dataset_return = pd.merge(dataset,dataset_for_run.drop(["street","zip_code","city"],axis=1),how="left",on=["index"])
        dataset_return.loc[(dataset_return["lat_x"] == "no data") & (dataset_return["lat_y"].notna()),"lat_x"] = dataset_return["lat_y"]
        dataset_return.loc[(dataset_return["lon_x"] == "no data") & (dataset_return["lon_y"].notna()),"lon_x"] = dataset_return["lon_y"]
        dataset_return.drop(["lat_y","lon_y"],axis=1,inplace=True)
        dataset_return.rename(columns={"lat_x":"lat","lon_x":"lon"},inplace=True)
        dataset_return.to_csv("../result/" +file.replace(".csv","")+"_final.csv",encoding="utf-8",sep=",",index=False)