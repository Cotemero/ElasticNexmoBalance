"""
Fetch Nexmo Balance and push it to ElasticSearch
"""
import os
import time
import string
import random
from datetime import datetime
from elasticsearch import Elasticsearch
import requests
from dotenv import load_dotenv
load_dotenv()

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    """
    Generate Random ID
    """
    return ''.join(random.choice(chars) for _ in range(size))

def main():
    """
    Main Function
    """
    url = 'https://rest.nexmo.com/account/get-balance/'
    url = url + os.getenv("NEXMO_API_ID") + '/' + os.getenv("NEXMO_API_SECRET")
    headers = {'content-type': 'application/json', 'accept': 'application/json'}
    elastic = Elasticsearch(
        [os.getenv("ELASTIC_HOST")],
        http_auth=(os.getenv("ELASTIC_USER"), os.getenv("ELASTIC_PASS")),
        scheme=os.getenv("ELASTIC_SCHEME"),
        port=os.getenv("ELASTIC_PORT")
    )
    nexmo_api_id = os.getenv("NEXMO_API_ID")
    sleep_seconds = os.getenv("SLEEP_SECONDS")
    while True:
        req = requests.get(url, headers=headers)
        balance = req.json()["value"]
        doc = {
            'balance': balance,
            'timestamp': datetime.now(),
        }
        index = nexmo_api_id+'-'+id_generator()
        elastic.index(index="nexmo-balance", doc_type='balance', id=index, body=doc)
        print("Pushed")
        time.sleep(int(sleep_seconds))

if __name__ == "__main__":
    main()
