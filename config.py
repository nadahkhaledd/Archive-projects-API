import connexion
import os


basedir = os.path.abspath(os.path.dirname(__file__))

application = connexion.FlaskApp(__name__)
application.add_api("swagger.yaml")
app = application.app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# from components.models import db
# db.create_all()