import os
from flask import Flask

def configure_deployment(app: Flask):
    """Configure app for deployment (e.g., Heroku)."""
    port = int(os.environ.get('PORT', 5000))
    app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False') == 'True'
    return app.run(host='0.0.0.0', port=port)