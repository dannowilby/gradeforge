from waitress import serve
from src import app

serve(app=app.app, host='0.0.0.0', port=5000)