import dotenv, requests

dotenv.load_dotenv()

url = dotenv.get('API_URL')

print(url)