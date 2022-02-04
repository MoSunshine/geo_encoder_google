# -*- coding: utf-8 -*-
"""
Created on Wed Jan 12 14:07:32 2022

@author: DE001E02544
"""
from geo_encoder_google import geo_encoder_google
import sys

def main(file):
    geo_encoder_object = geo_encoder_google()
    geo_encoder_object.encode_location(file)
    
if __name__ == '__main__':
    main(sys.argv[1])
    
