import urllib.request
from urllib.error import HTTPError, URLError
url='http://127.0.0.1:5000/api/health'
try:
    r=urllib.request.urlopen(url, timeout=10)
    print('Status', r.status)
    print(r.read().decode())
except HTTPError as e:
    print('HTTPError', e.code)
    try:
        print(e.read().decode())
    except Exception as ex:
        print('No body or error reading body:', ex)
except Exception as e:
    print('Error', e)
