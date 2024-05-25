from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from .db_config import DB_CONFIG
from flask_marshmallow import Marshmallow

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONFIG

# Create the SQLAlchemy db instance
db = SQLAlchemy(app)
ma = Marshmallow(app)

if __name__ == "__main__":
    app.run(debug=True)