from urllib.request import urlopen
from bs4 import BeautifulSoup
from bs4 import Comment
import re
import pprint
import yaml
import pandas as pd
import sys
from Internal import modOne

def main(asin):

    with open("C:\\Users\\User\\AppData\\Local\\Programs\\Python\\Python37-32\\Lib\\site-packages\\Internal\\yml4Amazon.yml", 'r') as ymlFile:
        PARAMS = yaml.load(ymlFile)

    asinsDict = {}
    # for asin in PARAMS['PARAMETERS']['ASINS']:
        # print(asin)
    # asin = sys.argv[1]
    print(asin)
    dictBuyBox = modOne.buyBox(asin)
    dictSellersInfo = modOne.sellersInfo(asin)
    dictCompetitiors = modOne.findCompetitors(dictSellersInfo)

    asinsDict[asin] = {
        'Name': dictBuyBox['productNameShort']
    ,'BuyBoxP':dictBuyBox['buyBoxPrice']
    ,'Rank':dictBuyBox['rank']
    ,'Cat':dictBuyBox['cat']
    ,'Min': dictCompetitiors['minHolder']
    ,'MinFul': dictCompetitiors['MinFul']
    # ,'MAX': dictSellersInfo[key_maxPriceFulFillOrAmazon]['price']
    ,'COMP': dictCompetitiors['COMP']
    }

    # pd.set_option('display.width', 1000)
    pd.set_option('display.expand_frame_repr', False)
    pd.set_option('display.colheader_justify', 'left')
    df = pd.DataFrame.from_dict(asinsDict, orient='index')

    return(df.to_html())