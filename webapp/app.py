import os
import sys
from pathlib import Path
from flask import Flask

# Make sure leakseeker package is importable
sys.path.insert(0, str(Path(__file__).parent.parent))

from webapp.routes import register_routes

def create_app():
    app = Flask(__name__,
                template_folder='templates',
                static_folder='static')

    app.config['SECRET_KEY'] = os.urandom(24)
    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB upload limit

    register_routes(app)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
