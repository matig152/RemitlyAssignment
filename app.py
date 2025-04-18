from flask import Flask
from routes import swift_codes_blueprint
from parse_data import load_data


# Initialize the database from .xlsx file
load_data()

# Create flask app
app = Flask(__name__)

# Register blueprints (modularize routes)
app.register_blueprint(swift_codes_blueprint)

if __name__ == '__main__':
    app.run(debug=True, port=8080)