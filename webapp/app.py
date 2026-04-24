import os
import sys
from pathlib import Path
from flask import Flask

# Ensure leakseeker package is importable
sys.path.insert(0, str(Path(__file__).parent))

from webapp.routes import register_routes


def create_app():
    app = Flask(
        __name__,
        template_folder='webapp/templates',
        static_folder='webapp/static'
    )

    # Use environment variable (important for production)
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "dev-secret")
    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB

    register_routes(app)
    return app


# 👇 THIS LINE IS CRITICAL FOR GUNICORN
app = create_app()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)