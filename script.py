import os
import requests

from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
SECRET_TOKEN = os.getenv("SECRET_TOKEN")

auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_TOKEN)

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

data = {'grant_type': 'password',
        'username': USERNAME,
        'password': PASSWORD}

headers = {'User-Agent': 'LazyPhotographer/0.0.1'}

res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth,
                    data=data,
                    headers=headers)

TOKEN = res.json()['access_token']

headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}
requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)

res = requests.get("https://oauth.reddit.com/r/EarthPorn/top",
                   headers=headers,
                   params={'limit':'10'})

for post in res.json()['data']['children']:
    title = post['data']['title']
    img_url = post['data']['url_overridden_by_dest']

    img_name = os.path.basename(urlparse(img_url).path)
    img_data = requests.get(img_url).content

    # Download with requests
    with open(img_name, 'wb') as handler:
        handler.write(img_data)
