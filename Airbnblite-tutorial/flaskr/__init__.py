from flask import Flask, Response, request, jsonify
from flask_pymongo import pymongo
from flaskr.database import DatabaseConnection
import datetime
import flaskr.auth
import flaskr.properties
import os

# app = Flask(__name__)
#db = DatabaseConnection()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    db = DatabaseConnection()

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    app.config['SECRET_KEY'] = os.urandom(12).hex()
    # a simple page that says hello
    @app.route('/hello')
    def hi():
        return 'Hello, World!'

    @app.route("/addNewProperty", methods=["POST"])
    def addNewProperty():
        document = {
            "name": request.form['name'],
            "propertyType": request.form['type'],
            "price": request.form['price']
        }
        db.insert("properties", document)
        return Response("Property successfully added", status=200, content_type="text/html")

    @app.route("/properties", methods=["GET"])
    def getproperties():
        properties = db.findMany("properties", {})
        return jsonify(properties)

    @app.route("/", methods=["GET"])
    def hello():
        return Response("<h1> Hey There </h1>", status=200, content_type="text/html")

    @app.route("/greeting", methods=["POST"])
    def greeting():
        name = request.form["name"]
        hourofday = datetime.datetime.now().time().hour
        greeting = ""
        if not name:
            return Response(Status=404)
        if hourofday < 12:
            greeting = "Good Morning"
        elif hourofday > 12 and hourofday < 18:
            greeting = "Good Afternoon"
        else:
            greeting = "Good Evening"
        response = greeting + " " + name + "!"
        return Response(response, status=200, content_type="text/html")

    app.register_blueprint(auth.bp)

    from . import properties
    app.register_blueprint(properties.bp)
    app.add_url_rule('/', endpoint='properties.index')

    return app


# if __name__ == "__main__":
#     app.run(host="127.0.0.1", port=4000, debug=True)
