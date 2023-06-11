import requests
import sys
import json
import logging
from dotenv import dotenv_values

config = dotenv_values()
logging.basicConfig(level=logging.INFO)
headers = {"accept": "application/json"}

try:
    access_token = config['ACCESS_TOKEN']
except:
    logging.error('This script requires an SxT access_token: python create.py <your-access-token-here>')
    sys.exit() 

try: 
    biscuit = config['BISCUIT']
except:
    logging.error('A biscuit token is required to create a table with this script. Please set BISCUIT in .env')
    sys.exit()

try: 
    biscuit_public_key = config['BISCUIT_PUBLIC_KEY']
except:
    logging.error('A biscuit public key is required to create a table with this script. Please set BISCUIT_PUB_KEY in .env')
    sys.exit()
 
try: 
    api_url = config['API_URL']
except:
    logging.error('Please make sure you set the SxT API_URL value in your .env file!')
    sys.exit() 

def main():
    # https://docs.spaceandtime.io/reference/modify-data-dml
    url = api_url + "sql/dml"
    
    schema_table = "PRIME_CRUSADERS.CARDS"

    tower = {
        "name":"PrimeCrusaders Tower",
        "description":"Used in the PrimeCrusaders TD game",
        "properties":{
            "card1":{"id":"bafybeifs45dm2rqb2wpt4iif2ts6btgoajnmmu7i3zsa7ef74xtgohuu3u","teir":1,"priority":1,"operator":0,"data1":2,"data2":11,"data3":5},
            "card2":{"id":"bafybeifjxcixtagebbxu3mptujnvggi6mifmcocnkb3cqycjtzwvqws5ui","teir":1,"priority":2,"operator":1,"data1":2,"data2":11,"data3":5},
            "card3":{"id":"bafybeiagf36kcskkydiza5z6cwkkmeu4czb2tckwqik7otjxwcrea7nqaq","teir":2,"priority":3,"operator":2,"data1":2,"data2":11,"data3":5},
            "card4":{"id":"bafybeihvup7eoznp5thrmhld6qqu3xxjmnnl6dyqwocp4zcjuimx2u237u","teir":2,"priority":4,"operator":3,"data1":2,"data2":11,"data3":5},
            "card5":{"id":"bafybeifoz4hztzq7shggpn6wed2jetolxm62fzqowwdiqsafwrtnwrbgmu","teir":2,"priority":5,"operator":2,"data1":2,"data2":11,"data3":5},
            "card6":{"id":"bafybeicbmrksl25k2rauirc7fulhezlznn2algdfm4gzxkfosz4lwb3wtm","teir":3,"priority":6,"operator":1,"data1":2,"data2":11,"data3":5},
            "card7":{"id":"bafybeifebfq4mdik2n3xocthr7vxiiswyyp7ceqgudnworbzacuisg4w6q","teir":3,"priority":7,"operator":0,"data1":2,"data2":11,"data3":5}
        }
    }
    
    sqlText = f"INSERT INTO {schema_table} (card, teir, priority, operator, data1, data2, data3) VALUES "
    
    for card in tower['properties']:
        data = tower['properties'][card]
        sqlText = sqlText + f"(\'{data['id']}\', {data['teir']}, {data['priority']}, {data['operator']}, {data['data1']}, {data['data2']}, {data['data3']}),"
    sqlText = sqlText[:-1] #remove the last comma

    payload = {
        "resourceId": schema_table,
        "sqlText": sqlText
    }

    headers = {
        "accept": "application/json",
        "biscuit": biscuit,
        "content-type": "application/json",
        "authorization": f"Bearer {access_token}"
    }
    logging.info(f"\nRequest Headers:{headers}\n\nRequest Payload: {payload}")
    resp = requests.post(url, json=payload, headers=headers)
    
    try: 
        json_resp = json.loads(resp.text)
        api_resposne = json.dumps(json_resp, indent=2)
    except:
        # if we don't get valid json response from the API
        api_resposne = resp.text
    
    logging.info(f"SxT API response code: {resp.status_code}\nSxT API Response text: {api_resposne}")
    

if __name__ == "__main__":
    main()
