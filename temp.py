from unittest import result
import requests
import pandas as pd
import re

keys = ['XLU']


headers = {}


def main(url):
    # results = list()
    with requests.Session() as req:
        req.headers.update({"User-Agent": "Mozilla/5.0 (compatible; Bot/0.1; )"})
        for key in keys:
            r = req.get(url.format(key))
            print(f"Extracting: {r.url}")
            # print(r.text)
            tables = re.findall(r'(?:document.table_data.*?=.*?\[)(.*?)(?:\n)', r.text)
            for table in tables:
                rows = re.findall(r'(?:\[)(.*?)(?:\])', table)
                for row in rows:
                    row = str.replace(row, '\\"', "%22")
                    fields = re.findall(r'(?:\")(.*?)(?:\")', row)
                    for field in fields:
                        field_search = re.findall(r'(?:<span class=%22hoverquote-symbol%22>)(.*?)(?:<span)', field)
                        if len(field_search) > 0:
                            print(f'{field_search[0]}')
                        else:
                            print(field)


main("https://www.zacks.com/funds/mutual-fund/quote/{}/holding")
main("https://www.zacks.com/funds/etf/{}/holding")
