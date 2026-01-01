from app import app
with app.test_client() as c:
    resp = c.get('/api/health')
    print('Status code:', resp.status_code)
    print('Data:', resp.data.decode())
    print('Headers:', resp.headers)
