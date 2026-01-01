"""
Start the Flask app with waitress.
Run: python serve_with_waitress.py
"""
import os
from waitress import serve
from app import app

# Use SQLite for local testing if not configured
if not os.getenv('DATABASE_URL'):
    os.environ['DATABASE_URL'] = 'sqlite:///skilltwin.db'

if __name__ == '__main__':
    port = int(os.getenv('PORT', '5000'))
    print(f'Starting app with waitress on http://0.0.0.0:{port}')
    try:
        serve(app, host='0.0.0.0', port=port)
    except Exception as e:
        import traceback
        traceback.print_exc()
        print('Waitress failed to start:', e)
        raise
