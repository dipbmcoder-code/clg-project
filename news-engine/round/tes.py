import requests
import json
import base64
from bs4 import BeautifulSoup
from requests.auth import HTTPProxyAuth
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
}
proxies = {'http': 'http://url',
                 'https': 'http://url'}

auth = HTTPProxyAuth('login', 'pass')
def get_loc(url):
    response = requests.get(url=url, headers = headers, proxies=proxies)
    soup = BeautifulSoup(response.text, 'lxml')

    ip = soup.find('div', class_='ip').text
    location = soup.find('div', class_='value-country').text
    print(location)
    user = "name"
    password = "pass"
    url2 = "https://url/wp-json/wp/v2/posts"

    payload = json.dumps({
        "title": "title",
        "status": "draft",
        "content": "text_all",
        "categories": [
            1
        ],
        "tags": []
        })
    credentials = user + ':' + password
    token = base64.b64encode(credentials.encode())
    headers2 = {'Authorization': 'Basic ' + token.decode('utf-8') ,
        'Content-Type': 'application/json'}

    response = requests.request("POST", url2, headers=headers2, data=payload)
    print(response.text)

    print(f"[INFO]  posted")


def main():
    get_loc(url="https:/url/.")

if __name__ == '__main__':
    main()
