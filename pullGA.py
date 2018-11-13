# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 13:55:11 2018

@author: Mathu_Gopalan
"""


import argparse, csv
import pandas as pd
from pandas.io.json import json_normalize

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

import httplib2
from oauth2client import client
from oauth2client import file
from oauth2client import tools


SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
DISCOVERY_URI = ('https://analyticsreporting.googleapis.com/$discovery/rest')
KEY_FILE_LOCATION = '.\My Project 26766-ae554bd965b7.p12'
SERVICE_ACCOUNT_EMAIL = 'gatest@valid-progress-217020.iam.gserviceaccount.com'
VIEW_ID = '172386207'
#'174803979'


def initialize_analyticsreporting():
  """Initializes an analyticsreporting service object.

  Returns:
    analytics an authorized analyticsreporting service object.
  """
  global response

  credentials = ServiceAccountCredentials.from_p12_keyfile(
    SERVICE_ACCOUNT_EMAIL, KEY_FILE_LOCATION, scopes=SCOPES)

  http = credentials.authorize(httplib2.Http())

  # Build the service object.
  analytics = build('analytics', 'v4', http=http, discoveryServiceUrl=DISCOVERY_URI)

  return analytics


def get_report(analytics):
  # Use the Analytics Service Object to query the Analytics Reporting API V4.
  return analytics.reports().batchGet(
        # Get sessions number from the last 7 days
#       body={
#         'reportRequests': [
#         {
#           'viewId': VIEW_ID,
#           'dateRanges': [{'startDate': '7daysAgo', 'endDate': 'today'}],
#           'metrics': [{'expression': 'ga:sessions'}]
#         }]
#       }
      # Get posts from last 7 days
      body={
          'reportRequests': [
              {
                  'viewId': VIEW_ID,
                  'dateRanges': [{'startDate': '7daysAgo', 'endDate': 'today'}],
                  'metrics': [
                      {'expression': 'ga:pageviews'},
                      {'expression': 'ga:uniquePageviews'},
                      {'expression': 'ga:timeOnPage'},
                      {'expression': 'ga:bounces'},
                      {'expression': 'ga:entrances'},
                      {'expression': 'ga:exits'}
                  ],
                  "dimensions": [
                      {"name": "ga:pagePath"}
                  ],
                  "orderBys": [
                      {"fieldName": "ga:pageviews", "sortOrder": "DESCENDING"}
                  ]
              }
          ]
      }
  ).execute()


def print_response(response):
  """Parses and prints the Analytics Reporting API V4 response"""

  for report in response.get('reports', []):
    columnHeader = report.get('columnHeader', {})
    dimensionHeaders = columnHeader.get('dimensions', [])
    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
    rows = report.get('data', {}).get('rows', [])

    for row in rows:
      dimensions = row.get('dimensions', [])
      dateRangeValues = row.get('metrics', [])

      for header, dimension in zip(dimensionHeaders, dimensions):
        print ( header + ': ' + dimension )

      for i, values in enumerate(dateRangeValues):
        print ('Date range (' + str(i) + ')' )
        for metricHeader, value in zip(metricHeaders, values.get('values')):
          print ( metricHeader.get('name') + ': ' + value )

def parse_data(response):

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

def write_dict_csv(response):
    
    with open('response.csv', 'w') as f:  # Just use 'w' mode in 3.x
        w = csv.DictWriter(f, response.keys())
        w.writeheader()
        w.writerow(response)

def main():
    analytics = initialize_analyticsreporting()
    response = get_report(analytics)
    result,columnHeader,metricHeader,columns = parse_data(response)
    df = pd.DataFrame(data = result)
    df.columns=columnHeader
    print(df.head())
    print("columnHeader :", columnHeader)
    print("metricHeader :", metricHeader)
    result.to_csv('result2.csv')
    #write_dict_csv(response)
    
if __name__ == '__main__':
  main()
