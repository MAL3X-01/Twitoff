from flask import Flask, render_template
#from .models import DB


def create_app():
    '''Create and configure an instance of the Flask application'''
    app = Flask(__name__)
    #app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///db.sqlite3'
    # DB.init_app(app)

    @app.route('/')
    def root():
        return 'Welcome to TwitOff!'

    return app
