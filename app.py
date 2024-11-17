import os
from flask import Flask
from logging.config import dictConfig
from datetime import datetime, timedelta
from api.user_profiles import user_profiles_routes
from api.user_manager import user_manager_routes
from api.books import books_routes
from flask_jwt_extended import JWTManager
from api.user_manager import bcrypt
from flask_cors import CORS

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': os.environ.get('LOGGING_LEVEL'),
        'handlers': ['wsgi']
    }
})

# instantiate the app
app = Flask(__name__, instance_relative_config=True)


app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)


jwt = JWTManager(app)
bcrypt.init_app(app) 

# set config
app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)



# register API Endpoints
app.register_blueprint(user_profiles_routes, url_prefix='/api/profiles')
app.register_blueprint(user_manager_routes, url_prefix='/api/user')
app.register_blueprint(books_routes, url_prefix='/api/books')


CORS(app)


if __name__ == '__main__':
    app.run(debug=True)