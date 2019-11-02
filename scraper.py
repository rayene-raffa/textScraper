import sys
import re
import os
import pandas as pd
from pandas import ExcelWriter
import urllib.request
from bs4 import BeautifulSoup
from extractVendors import ExtractVendors
from extractProducts import ExtractProducts
from extractCategories import ExtractCategories
from extractIndustries import ExtractIndustries
from postProcess import PostProcess



base_url = 'https://dir.indiamart.com'

def scrape(base_url,out_dir='./out',log_dir=None):

    industries = ExtractIndustries(base_url)
    g_categories = pd.DataFrame(columns={'Name','URL','Industry'})
    for industry in industries.itertuples():
        categories = ExtractCategories(base_url, industry)
        g_categories = g_categories.append(categories,ignore_index=True,sort=False)
    
    g_products = pd.DataFrame(columns={'Name','URL','subCategory','Category','Industry'})
    for category in g_categories.itertuples():
        products   = ExtractProducts(base_url, category)
        g_product = g_products.append(products,ignore_index=True,sort=False)

    prod_found = len(g_products.index)
    print(f"##########\n#########\nFound {prod_found} products TOTAL\nFetching vendors ...\n##############\n##############\n")
    i=1
    for product in g_products.itertuples():
        vendors    = ExtractVendors(base_url, product)
        print(f'\n~~~~~~~~~~\n{i*100/prod_found}\n~~~~~~~~~~~~~~\n')
        i += 1
    return 0



scrape(base_url)


# categories = pd.DataFrame(columns={'Name', 'URL','Industry'})
# industries = pd.DataFrame(columns={'Name', 'URL'})
# sellers = pd.DataFrame(columns=['Name', 'URL', 'Phone', 'Address','Category','Industry'])
# sellers, categories, industries =  scrape(sellers, categories, industries)
# PostProcess()