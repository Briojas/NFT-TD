import dotenv, os, requests

dotenv.load_dotenv('../.env')

dql_url = os.environ.get('API_URL') + '/v1/sql/dql'

headers = {
    'accept': 'application/json',
    'authorization': 'Bearer ' + os.environ.get('SXT_ACCESS_TOKEN'),
    'Content-Type': 'application/json',
}

sqlText = 'SELECT COUNT(*) FROM ETHEREUM.ERC721_TRANSFER WHERE CONTRACT_ADDRESS = \'0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D\' AND CAST(TIME_STAMP AS DATE) = \'2023-03-09\''


data = {
    'resourceId': 'ETHEREUM.ERC721_TRANSFER',
    'sqlText': sqlText
}

# print (data)
response = requests.post(dql_url, headers=headers, json=data)
print(response.text)