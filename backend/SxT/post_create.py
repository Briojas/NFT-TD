import dotenv, os, requests

dotenv.load_dotenv('../.env')

ddl_url = os.environ.get('API_URL') + '/v1/sql/ddl'

headers = {
    'accept': 'application/json',
    'authorization': 'Bearer ' + os.environ.get('SXT_ACCESS_TOKEN'),
    'biscuit': os.environ.get('SXT_BISCUIT'),
    'Content-Type': 'application/json',
}

sqlText = 'CREATE TABLE BRIOJAS_TESTING.TEST (ID INT, NAME VARCHAR, PRIMARY KEY (ID)) WITH '
auth = "\'public_key=' + os.environ.get('SXT_BISCUIT_PUBLIC_KEY') + ',access_type=public_write\'"
sqlText = sqlText + auth

# sqlText = 'CREATE SCHEMA BRIOJAS_TESTING'

data = {
    'sqlText': sqlText,
}

print (data)
response = requests.post(ddl_url, headers=headers, json=data)
# print(response.json())
print(response.status_code)
print(response.text)