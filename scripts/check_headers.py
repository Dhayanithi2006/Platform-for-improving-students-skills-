import urllib.request

url = 'http://127.0.0.1:8000/static/js/main.f8eff99c.js'
req = urllib.request.Request(url, method='HEAD')
try:
    r = urllib.request.urlopen(req, timeout=5)
    print('Status:', r.status)
    print('Content-Type:', r.getheader('Content-Type'))
except Exception as e:
    print('Error:', e)