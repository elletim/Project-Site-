from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd 
import requests as req
from io import StringIO


def index(request):
    url = "http://berkeleyearth.lbl.gov/air-quality/maps/cities/United_States/California/Los_Angeles.txt"
    page = req.get(url)
    page_df= pd.read_csv(StringIO(page.text),skiprows=10,sep='\t')
    page_df.columns= ['Year','Month','Day', 'UTC Hour','PM2.5','PM10_mask','Retrospective']     
    page_df = page_df[["Year","Month","PM2.5"]]
    page_df = page_df[(page_df["Year"].isin([2018,2019,2020,2021,2022])) & (page_df["Month"].isin([3,4,5]))]
    page_df = page_df.groupby(["Year","Month"])
    page_df = page_df["PM2.5"].mean()
    df = pd.DataFrame(data=page_df)
    pivot = df.pivot_table(columns="Year",index="Month",values="PM2.5")
    global data 
    data = pivot.to_html()
    return HttpResponse(data)