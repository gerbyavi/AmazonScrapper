from urllib.request import urlopen, Request
from bs4 import BeautifulSoup, NavigableString
from bs4 import Comment
import re
import pprint
import yaml
import pandas as pd
from collections import defaultdict
import requests
import lxml
from selenium import webdriver

with open("C:\\Users\\User\\AppData\\Local\\Programs\\Python\\Python37-32\\Lib\\site-packages\\Internal\\yml4Amazon.yml", 'r') as ymlFile:
    PARAMS = yaml.load(ymlFile)

def buyBox(asin):
    rank = None
    cat = None
    browser = webdriver.Chrome("C:\\Users\\User\\Downloads\\chromedriver.exe")
    url = "https://www.amazon.com/Panasonic-Electric-ES-LV65-S-Flexible-Pivoting/dp/" + asin + "/"
    # browser.get(url)
    try:
        browser.get(url)
    except urllib.request.HTTPError as e:
        if e.code==404:
            print(f"{url} is not found")
        elif e.code==503:
            print(f'{url} base webservices are not available')
            ## can add authentication here 
        else:
            print('http error',e)
    buyBoxPage = browser.page_source
    browser.close()
    # print(url)
    soup4buyBoxPage = BeautifulSoup(buyBoxPage,'lxml')
    buyBoxSeller = soup4buyBoxPage.find("span", {"id": "merchant-info"})
    print(buyBoxSeller.get_text(" ", strip=True).split("\n")[0])
    buyBoxPrice = re.sub(r'\$','',soup4buyBoxPage.find("span", {"id": "priceblock_ourprice"}).get_text())
    # print("buyBoxPrice:",buyBoxPrice)
    productName = soup4buyBoxPage.find("span",{"id":"productTitle"}).get_text()
    productNameTmp = re.sub(r'\s{2,}',' ', productName)
    productNameNeat = re.sub(r'^\s+','', productNameTmp, flags=re.M)
    # productNameStripped = productNameNeat.lstrip('\t\s')
    # print(productNameStripped)
    match_productNameNeat = re.search(r'^((:?\w+\s+){2}\w+)',productNameNeat)
    productNameShort = match_productNameNeat.group(1)
    # print(productNameNeat)
    tableDiv = soup4buyBoxPage.find("li",{"id":"SalesRank"})

    for elem in tableDiv:
        if isinstance(elem, NavigableString):
            text = str(elem).strip()
            if text is not None:
                cleanText = re.sub(r'^[\s\t\r]+','',re.sub(r'\s{2,}','',re.sub(r'[\r\t\n]+','',text, flags=re.M), flags=re.M), flags=re.M)
                # print(cleanText)
                moRankCategory = re.search(r'([,\d]+)\sin\s(.*)\s\(',cleanText)
                if moRankCategory is not None:
                    rank = moRankCategory.group(1)
                    cat = moRankCategory.group(2)
                    # print('Rank:',rank,' cat:',cat)
    return {'buyBoxPrice':buyBoxPrice,'productNameShort':productNameShort, 'rank':rank,'cat':cat}


def sellersInfo(asin):
    browser = webdriver.Chrome("C:\\Users\\User\\Downloads\\chromedriver.exe")
    url = "https://www.amazon.com/gp/offer-listing/" + asin + "/ref=dp_olp_new_mbc?ie=UTF8&condition=new"
    browser.get(url)
    sellersPage = browser.page_source
    browser.close()
    # sellersPage = urlopen(url)
    soup4SellerPage = BeautifulSoup(sellersPage,features="html.parser")
    hsh = {}
    for row in soup4SellerPage.find_all('div', class_=re.compile(r"a-row\sa-spacing-mini\solpOffer")):

        seller = row.find('div', class_=re.compile(r"olpSellerColumn")).get_text(" ", strip=True)
        sellerRaw = row.find('div', class_=re.compile(r"olpSellerColumn"))
        price = row.find('div', class_=re.compile(r"olpPriceColumn")).get_text(" ", strip=True)
        delivery = row.find('div', class_=re.compile(r"olpDeliveryColumn")).get_text(" ", strip=True)
        matchObject = re.search(r'\$([\d\.]+)\s\+\s\$([\d\.]+)',price)
        flagChargesShipping = 0
        if matchObject is not None:
            flagChargesShipping = 1
            price = float(matchObject.group(1)) + float(matchObject.group(2))
        else:
            matchPriceNoShippingObject = re.search(r'\$([\d\.]+)',price)
            price = float(matchPriceNoShippingObject.group(1))
        if re.search(r'Shipped\sby\sAmazon',delivery):
            delivery = 'Fulfilled By Amazon'
        img = sellerRaw.find('img') 
        if img is not None:
            seller = img.attrs['alt']
            delivery = 'Amazon'
        else:
            seller =  sellerRaw.find('a').string
        hsh[seller] = {'price':price, 'delivery':delivery, 'chargesShipping': flagChargesShipping}
    return hsh

def findCompetitors(dictSellersInfo):
    copyOfDict = dict(dictSellersInfo)
    key_minimumPrice = min(copyOfDict.keys(), key=(lambda k: float(copyOfDict[k]['price'])))
    # key_maxPriceFulFillOrAmazon = max(dictSellersInfo.keys(), key=(lambda k: float(dictSellersInfo[k]['price'])))
    comptitor = 0
    minHolder = dictSellersInfo[key_minimumPrice]['price']
    # loop to remove non fulfilled sellers
    for (key, value) in copyOfDict.items():
        if ( copyOfDict[key]['delivery'] not in ['Fulfilled By Amazon', 'Amazon'] ):
            del dictSellersInfo[key]
    key_minimumPriceFulFillOrAmazon = min(dictSellersInfo.keys(), key=(lambda k: float(dictSellersInfo[k]['price'])))
    # loop to find competitors
    for (key, value) in copyOfDict.items():
        if (copyOfDict[key]['delivery'] not in ['Fulfilled By Amazon', 'Amazon'] 
        and copyOfDict[key]['price'] < copyOfDict[key_minimumPriceFulFillOrAmazon]['price'] * PARAMS['PARAMETERS']['MULTIPY'] ):
            comptitor += 1
        if ( copyOfDict[key]['delivery'] in ['Fulfilled By Amazon', 'Amazon']
            and copyOfDict[key]['price'] < copyOfDict[key_minimumPriceFulFillOrAmazon]['price'] * PARAMS['PARAMETERS']['MULTIPYFULFILL'] ):
            # MayBe Increase the multipyer for Amazon cause the MADAFAKA can put a higher price
            comptitor += 1   
    return {'COMP': comptitor, 'minHolder':minHolder,'MinFul': copyOfDict[key_minimumPriceFulFillOrAmazon]['price'], 'KeyMinFul': key_minimumPriceFulFillOrAmazon}
            
