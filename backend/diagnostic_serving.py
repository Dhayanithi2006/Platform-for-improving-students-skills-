import os
os.environ['DATABASE_URL'] = 'sqlite:///skilltwin.db'
from app import app
build_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'build'))
print('build_dir=', build_dir)
print('index exists=', os.path.exists(os.path.join(build_dir,'index.html')))
print('files sample=', sorted(os.listdir(build_dir))[:20])

with app.test_client() as c:
    r = c.get('/')
    print('\nGET / status:', r.status_code)
    print('GET / body (first 500 chars):', r.get_data(as_text=True)[:500])

    r = c.get('/index.html')
    print('\nGET /index.html status:', r.status_code)
    print('GET /index.html body starts with:', r.get_data(as_text=True)[:200])

    # Try serving a static asset
    r = c.get('/static/js/main.f8eff99c.js')
    print('\nGET asset status:', r.status_code)
    print('asset length:', len(r.get_data()))
