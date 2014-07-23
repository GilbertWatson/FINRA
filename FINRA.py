# -*- coding: utf-8 -*-

# load packages
import requests as r
import json
import csv

# open session and set "I agree" cookie
s = r.session()
s.post("https://ats.finra.org/Agreement/Submit", data="agree=True", verify=False)

# function that returns main table by date, type and page number
def GetTradingSymbols(date,Type,pgnum):
    base = "https://ats.finra.org/TradingSymbols/TradingSymbolsJson?"
    Filter = "filter=SettleDate~" + date + "_reportType~" + Type
    rest = "&sort=SymbolCD~asc&pgnum=" + pgnum + "&sEcho=1&iColumns=6&sColumns=&iDisplayStart=0&iDisplayLength=-1&mDataProp_0=SymbolCD&mDataProp_1=IssueDescription&mDataProp_2=TotalShareAmount&mDataProp_3=TotalTradeAmount&mDataProp_4=LatestUpdatedDate&mDataProp_5=null&iSortCol_0=0&sSortDir_0=asc&iSortingCols=1&bSortable_0=true&bSortable_1=true&bSortable_2=true&bSortable_3=true&bSortable_4=true&bSortable_5=false&_=1403280831743"
    return s.get(base + Filter + rest, verify=False)

# function that returns detail tables by trading symbol
def GetTradingSymbolDetail(ID):
    url = "https://ats.finra.org/TradingSymbols/DetailsJSON?filter=TrdgSymID~" + ID + "&_=1403640582444"
    return s.get(url, verify=False)

# list all types and dates
Types = ["T1", "T2", "OC"]
# Dates = ["1401062400", "1401667200", "1400457600", "1399852800"]
# Dates = ["1402272000"]
# Dates = ["1402272000","1401062400", "1401667200", "1400457600"]
Dates = ["1402272000","1402876800", "1401667200", "1403481600"]

# grab the big tables for each date
BigDataTables = []
for t in Types:
    for d in Dates:
        p = 1
        cont = GetTradingSymbols(d,t,str(p))
        while json.loads(cont.content)['iTotalDisplayedRecords'] > 0:
            BigDataTables.extend(json.loads(cont.content)['aaData'])
            p = p + 1
            cont = GetTradingSymbols(d,t,str(p))

# grab the detail tables by iterating through the big table
DetailDataTables = []
for symbol in range(len(BigDataTables)):
    DetailDataTables.extend(json.loads(GetTradingSymbolDetail(str(BigDataTables[symbol]['TradingSymbolID'])).content)['aaData'])

# write BigDataTables to json file
with open('C:/Users/gwatson/Desktop/BigDataTables.json', 'w') as outfile:
  json.dump(BigDataTables, outfile)

# write DetailDataTables to json file
with open('C:/Users/gwatson/Desktop/DetailDataTables.json', 'w') as outfile:
  json.dump(DetailDataTables, outfile)

