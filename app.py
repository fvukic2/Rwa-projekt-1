from flask import Flask
from flask_restplus import Api
from controller import api 
from model import db 

app = Flask(__name__)

# load application configuration from config.py
app.config.from_object('config.DevelopmentConfig')

# initialize database via flask-sqlalchemy
db.init_app(app)

# initialize rest api via flask-restplus
api.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)




