# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 14:53:08 2018

@author: Mathu_Gopalan
"""

import helper as h

#enter the viewid to get data
Views = '172386207'
#Enter the metrics
Metrics = [{'expression': 'ga:pageviews'},
           {'expression': 'ga:uniquePageviews'},
           {'expression': 'ga:timeOnPage'},
           {'expression': 'ga:bounces'},
           {'expression': 'ga:entrances'},
           {'expression': 'ga:exits'}]
#Enter the Dimension
Dimenson = [{"name": "ga:pagePath"}
            ]

#Enter the date Range - update the date field in yyy-mm-dd format
DateRange = [{'startDate': '7daysAgo', 'endDate': 'today'}]

h.pull_data(Views,Dimenson,Metrics,DateRange)