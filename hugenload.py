__author__ = 'jschpp'
__version__ = '0.0.1'

import requests
import sys
import json

USERAGENT = 'hugenload.jschpp.de/' + __version__


def upload_file(username, password, filename):

    # Proxy definitions for burpsuite
    proxies = {
        "http": "http://127.0.0.1:8080",
        "https": "http://127.0.0.1:8080",
    }
    redirect = r"https%3A%2F%2Fwebreader.hugendubel.de%2Flibrary%2Findex.html"
    # Custom useragent
    hugen_headers = {'user-agent': USERAGENT}

    # params for this url were found by sniffing
    url = r"https://www.hugendubel.de/oauth/authorize?client_id=" \
          "4c20de744aa8b83b79b692524c7ec6ae&response_type=code&" \
          "scope=ebook_library&redirect_uri=" + redirect
    data = {'username': username, 'password': password, 'login': ''}
    # from this request just the code in the 302 location url is needed
    req = requests.post(url, data, allow_redirects=False, headers=hugen_headers,
                        proxies=proxies, verify=False)
    code = req.headers['location'].split('=')[-1]

    # let's do oauth manually till I find the time to fix this
    # TODO use oauth lib
    url = r"https://api.hugendubel.de/rest/oauth2/token"
    data = {'client_id': '4c20de744aa8b83b79b692524c7ec6ae',
            'grant_type': 'authorization_code', 'code': code,
            'scope': 'ebook_library', 'redirect_uri': redirect}
    req = requests.post(url, data, headers=hugen_headers, proxies=proxies,
                        verify=False)
    oauth = json.loads(req.text)

    bosh_header = {'user-agent': USERAGENT, 'm_id': 13,
                   't_auth_token': oauth['access_token'],
                   'origin': r'http://www.hugendubel.de',
                   'X-Audiobook-Enabled': 1,
                   'hardware_id': '',  # TODO how to generate this
                   'Referer': 'http://www.hugendubel.de/library/library.html'}
    url = r"https://bosh.pageplace.de/bosh/rest/upload"
    file = {'file': (filename, open(filename, 'rb'), 'application/epub+zip')}
    req = requests.post(url, headers=bosh_header, files=file,
                        proxies=proxies, verify=False)
    print(req.text + "\n" + req.headers.__str__())


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("usage: hugenload.py username password filename")
    else:
        upload_file(sys.argv[1], sys.argv[2], sys.argv[3])

#upload_file()