__author__ = 'jschpp'
__version__ = '0.0.1'

import requests
import sys
import json


def upload_file(username, password, filename):
    # Proxy definitions for burpsuite
    proxies = {
        "http": "http://127.0.0.1:8080",
        "https": "http://127.0.0.1:8080",
    }
    # Custom useragent
    headers = {'user-agent': 'hugenload.jschpp.de/0.0.1'}

    # params for this url were found by sniffing
    url = r"https://www.hugendubel.de/oauth/authorize?client_id=4c20de744aa8b83b79b692524c7ec6ae&response_type=code&scope=ebook_library&redirect_uri=https%3A%2F%2Fwebreader.hugendubel.de%2Flibrary%2Findex.html"
    data = {'username': username, 'password': password, 'login':''}
    # from this request just the code in the 302 location url is needed
    req = requests.post(url, data, allow_redirects=False,headers=headers, proxies=proxies, verify=False)
    code = req.headers['location'].split('=')[-1]

    # let's do oauth manually till I find the time to fix this
    # TODO use oauth lib
    url = r"https://api.hugendubel.de/rest/oauth2/token"
    data = {'client_id':'4c20de744aa8b83b79b692524c7ec6ae', 'grant_type':'authorization_code','code': code,'scope':'ebook_library', 'redirect_uri': 'https%3A%2F%2Fwebreader.hugendubel.de%2Flibrary%2Findex.html'}
    req = requests.post(url, data, proxies=proxies, verify=False)
    oauth = json.loads(req.text)
    print(oauth['access_token'])
#    file = {'file':(filename, open(filename,'rb'),'application/epub+zip',{'t_auth_token':auth_token})}


if __name__ == "__main__":
    if len(sys.argv) != 4:
       print("usage: hugenload.py username password filename")
    else:
        r = upload_file(sys.argv[1], sys.argv[2], sys.argv[3])

#upload_file()