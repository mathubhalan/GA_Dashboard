# -*- coding: utf-8 -*-
"""
Created on Mon Oct  1 15:30:18 2018

@author: Mathu_Gopalan
"""
import configparser, httplib2, datetime
import pandas as pd


from pandas.io.json import json_normalize
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from oauth2client import client
from oauth2client import file
from oauth2client import tools


def read_config(config):
    '''
    Function to read the .ini configurations file and store the details
    Input: configuration file name
    Output: parse the data and store it as dictionary
    '''
    global cfg_dict
    cfg_dict={}
    cfg = configparser.ConfigParser()
    cfg.read(config)
    cfg_dict["Folder"] = cfg['GA_config']['folder']
    cfg_dict["Scopes"] = cfg['GA_config']['SCOPES']
    cfg_dict["Discovery_URT"] = cfg['GA_config']['DISCOVERY_URI']
    cfg_dict["key_file_loc"] = cfg['GA_config']['KEY_FILE_LOCATION']
    cfg_dict["service_acc_email"] = cfg['GA_config']['SERVICE_ACCOUNT_EMAIL']
    
    return cfg_dict

def initialize_analyticsreporting(cfg_dict):
    """
    Initializes an analyticsreporting service object.
    Input: NA
    Output: returns an authorized analyticsreporting service object.
    """
    global response
    
    credentials = ServiceAccountCredentials.from_p12_keyfile(
    cfg_dict["service_acc_email"], cfg_dict["key_file_loc"], scopes=cfg_dict["Scopes"])
    http = credentials.authorize(httplib2.Http())
    
      # Build the service object.
    analytics = build('analytics', 'v4', http=http, discoveryServiceUrl=cfg_dict["Discovery_URT"])
    return analytics

def parse_data(response):
    
    '''
    Parse the response data into columns and rows
    Input: response object
    Output: parsed data in a more structured format
    '''
    
    reports = response['reports'][0]
    columnHeader = reports['columnHeader']['dimensions']
    metricHeader = reports['columnHeader']['metricHeader']['metricHeaderEntries']
    
    columns = columnHeader
    for metric in metricHeader:
        columns.append(metric['name'])
    
    data = json_normalize(reports['data']['rows'])
    data_dimensions = pd.DataFrame(data['dimensions'].tolist())
    data_metrics = pd.DataFrame(data['metrics'].tolist())
    data_metrics = data_metrics.applymap(lambda x: x['values'])
    data_metrics = pd.DataFrame(data_metrics[0].tolist())
    result = pd.concat([data_dimensions, data_metrics], axis=1, ignore_index=True)
    
    return result,columnHeader,metricHeader,columns

def get_report(analytics,View_id,Dimensions,Metrics,Date_range):
    # Use the Analytics Service Object to query the Analytics Reporting API V4.
    return analytics.reports().batchGet(
            body={
                'reportRequests': [
                    {'viewId': View_id,
                     'dateRanges': Date_range,
                     'metrics': Metrics,
                     "dimensions": Dimensions}
                            ]}).execute()
"""
def write_dict_csv(response):
    '''
    Function to export the data set in csv format
    Input: GA response object
    Output: Load the CSV file in local folder
    '''
    
    with open('response.csv', 'w') as f:  # Just use 'w' mode in 3.x
        w = csv.DictWriter(f, response.keys())
        w.writeheader()
        w.writerow(response)
   """     
        
def pull_data(views,dimensions,metrics,date_range):
    '''
    Function to fetch the report
    Input: The list objects for View, dimensions and metrics along with date range for which data to be extracted
    Output: The data would be loaded in SFTP site as a csv file    
    '''
    cfg_dict = read_config("config.ini")
    analytics = initialize_analyticsreporting(cfg_dict)
    response = get_report(analytics,views,dimensions,metrics,date_range)
    result,columnHeader,metricHeader,columns = parse_data(response)
    df = pd.DataFrame(data = result)
    df.columns=columnHeader
    now=datetime.datetime.now()
    timestamp = str(now.strftime("%Y%m%d_%H-%M-%S"))
    file_name = "Result"+timestamp+".csv"
    #result.to_csv('result3.csv')
    #print(df.head())
    #print(result.head())
    df.to_csv(file_name)
    print(f"Loaded the data with filename as {file_name}")
    #print("Data Loaded successfully and filename is {}".format(file_name))
    
    
    
    
    
    

