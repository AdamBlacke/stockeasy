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
            tables = re.findall(r'(?:etf_holdings.formatted_data.*?=.*?\[)(.*?)(?:\n)', r.text)
            for table in tables:
                rows = re.findall(r'(?:\[)(.*?)(?:\])', table)
                for row in rows:
                    print('\n')
                    row = str.replace(row, '\\"', "%22")
                    fields = re.findall(r'(?:\")(.*?)(?:\")', row)
                    for field in fields:
                        field_cleaners = [
                            r'(?:<span class=%22truncated_text_single%22.*?>)(.*?)(?:</span)',
                            r'(?:<span class=%22hoverquote-symbol%22>)(.*?)(?:<span)',
                        ]
                        for cleaner in field_cleaners:
                            field_search = re.findall(cleaner, field)
                            if len(field_search) > 0:
                                field = field_search[0]
                        print(field)


main("https://www.zacks.com/funds/mutual-fund/quote/{}/holding")
main("https://www.zacks.com/funds/etf/{}/holding")
