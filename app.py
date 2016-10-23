from flask import Flask
from flask import jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/ph_db'
database = SQLAlchemy(app)

class ElementType(database.Model):
    __tablename__ = "element_types"
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(50), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<ElementType %r>' % self.name

class Element(database.Model):
    __tablename__ = "elements"
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(50), unique=True)
    element_type_id = database.Column(database.Integer)

    def __init__(self, name, id):
        self.name = name
        self.element_type_id = id

    def __repr__(self):
        return '<Element %r>' % self.name


class Test(database.Model):
    __tablename__ = "tests"
    id = database.Column(database.Integer, primary_key=True)
    data = database.Column(database.String(50))
    date = database.Column(database.DateTime)

    def __init__(self):
        pass

class ElementTest(database.Model):
    __tablename__ = "element_tests"
    id = database.Column(database.Integer, primary_key=True)
    test_id = database.Column(database.Integer)
    element_id = database.Column(database.Integer)


@app.route("/")
def root():
    return "This is flask"

@app.route("/regdata", methods=['POST'])
def regdata():
    name = None
    type_id = None
    if request.method == 'POST':
        name = request.args.get('name')
        type_id = request.args.get('tid')
        if not database.session.query(Element).filter(Element.name == name).count():
            element = Element(name,type_id)
            database.session.add(element)
            database.session.commit()
            return jsonify(status=200)

    return "This isn't a get request"

if __name__ == '__main__':
    app.run()